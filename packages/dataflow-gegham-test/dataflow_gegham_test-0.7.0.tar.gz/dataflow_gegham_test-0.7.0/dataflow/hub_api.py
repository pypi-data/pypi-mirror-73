import os
import math
from typing import Union, Iterable
import time
import boto3
import dask
import numpy as np

from scipy import ndimage
from threading import RLock

from dataflow.creds.creds import Creds
from dataflow.logger import logger
import hub
from dask.cache import Cache
from dask.distributed import Client
from dataflow.cloud.cluster import Cluster
import dataflow.utils as utils
from dataflow.cloud.iam_blocked_check import check_arns

local_dir = "data/preprocess_nova"
bucket2obj = {}
botolock = RLock()
_client = None


def get_client():
    global _client
    if _client is None:
        _client = init()
    return _client


def init(
    token: str = "",
    cache=2e9,
    cloud=False,
    n_workers=4,
    image="snarkai/hub:dataflow-prod",
):
    """Initializes cluster either local or on the cloud
        
        Parameters
        ----------
        token: str
            token provided by snark
        cache: float
            Amount on local memory to cache locally, default 2e9 (2GB)
        cloud: bool
            Should be run locally or on the cloud
        n_workers: int
            number of concurrent workers, default 5
        image: str
            default (snarkai/hub:dataflow-prod)
            change to snarkai/hub:dataflow-prod

    """
    if cloud:
        check_arns()
        logger.info("Starting Cloud Cluster, it will take 5 mins")

        # TODO simplify container login
        t1 = time.time()
        cluster = Cluster(n_workers=n_workers, image=image,)
        client = Client(cluster)
        t2 = time.time()
        logger.info(f"Cluster started in {t2-t1}s: {cluster.dashboard_link}")
    else:
        client = Client(n_workers=n_workers, processes=True, memory_limit=50e9,)
    cache = Cache(cache)
    cache.register()
    global _client
    _client = client
    return client


def open(url: str, creds: str = None, path="./data/hub"):
    """Load preprocessed data into dataset
        For now opens arrays from data/hub directory
        
        Parameters
        ----------
        url: str
            Represents the url where data is stored
        creds: str
            Represents the url where credentials are stored to access the url 
    """
    if not url.startswith("s3://"):
        bucket = hub.fs(path).connect()
        return bucket.dataset_open(url)
    elif url.startswith("s3://"):
        file_path = "/".join(url.split("/")[3:])
        bucket_name = url.split("/")[2]
        bucket = hub.s3(bucket_name, aws_creds_filepath=creds).connect()
        return bucket.dataset_open(file_path)


@dask.delayed
def _download_file(storage: str, bucket_name: str, path: str) -> str:
    bucket = _get_bucket(storage, bucket_name)
    local_path = os.path.join(local_dir, path)
    # print(f'Path to save the file: {local_path}')
    folder = os.path.split(local_path)[0]
    os.makedirs(folder, exist_ok=True)
    try:
        bucket.download_file(path, local_path)
    except Exception as err:
        logger.exception(err)
        return None
    return local_path


def _get_bucket(storage: str, bucket_name: str):
    # TODO: ipdate creds part, maybe move it into init
    creds = {
        "snark-intelinair-export": "snarkai",
        "intelinair-processing-agmri": "intelinair",
    }
    # TODO: why we don't take preprocess/ ?
    if bucket_name in bucket2obj:
        bucket = bucket2obj[bucket_name]
    else:
        bucket = boto3.resource(
            storage,
            aws_access_key_id=Creds(creds[bucket_name]).get("aws_access_key_id"),
            aws_secret_access_key=Creds(creds[bucket_name]).get(
                "aws_secret_access_key"
            ),
        ).Bucket(bucket_name)
        bucket2obj[bucket_name] = bucket
    return bucket


def _setup_dataset(ds, name, path, hb, clear, cloud):
    special = ds["__special__"]
    del ds["__special__"]
    bucket = hb.connect()

    if clear:
        if cloud and not os.path.exists(os.path.join(path, name)):
            # print("oops")
            return special, bucket
        try:
            # , ignore_errors=True)
            # print("Here it goes")
            bucket.delete(name)
            if os.path.exists(os.path.join(path, name)):
                print("Bad news it still exists")
                exit()
            # shutil.rmtree(os.path.join(path, name), ignore_errors=False)
            # bucket.delete(name
        except Exception as ex:
            # print(ex)
            logger.warn(ex)
    return special, bucket


def _create_dataset(name, bucket, ds, special, chunksize):
    dataset = {}
    for el in ds:
        if el.startswith("__"):
            continue
        shape = ds[el].shape
        dsplit = None
        dtype = ds[el].dtype
        if el in special:
            dsplit = len(shape)
            dtype = special[el][0]
            shape = shape + special[el][1]
        csize = utils.compute_chunk_size(dtype, shape)
        csize = min(csize, chunksize)
        chunk = [csize] + list(shape[1:])
        arr_name = os.path.join(name, el)
        if shape[0] == 0:
            raise Exception("No samples in the dataset")
        # print(el, shape, chunk)
        images = bucket.array_create(
            arr_name, shape=shape, chunk=chunk, dtype=dtype, dsplit=dsplit
        )
        dataset[el] = images

    dataset = bucket.dataset_create(name, dataset)
    return dataset, shape


def _cache(start, stop, el, data, special, path, cloud, name):
    t1 = time.time()
    with botolock:
        if cloud:
            bucket = hub.s3(path).connect()
        else:
            bucket = hub.fs(path).connect()
    try:
        dataset = bucket.dataset_open(name)
        if el in special:
            dataset[el].darray[start:stop] = np.array([el.shape for el in data])
            shape = dataset[el][start:stop].shape

            arr = np.zeros(shape)
            for i, element in enumerate(data):
                dshape = tuple(slice(None, eli) for eli in element.shape)
                arr[(i,) + dshape] = element
            dataset[el][start:stop] = arr
        else:
            dataset[el][start:stop] = data
    except Exception as e:
        # FIXME issue refers to multiple workers writing to the same chunk
        logger.error(f"Error while writing {el}[{start}:{stop}]: {str(e)}")
    t2 = time.time()
    logger.debug(f"task done in {t2-t1}")
    if t2 - t1 > 100.0:
        logger.debug([start, stop, el, data, special, path, cloud, name])


def cache(
    ds, url, path: str = "./data/hub/", clear=True, chunksize=500,
):
    """Caches dataset/array into local directory
        By default caches into ./data/hub
        Parameters
        ----------
        ds: dataset
        url: str
            Represents the url where data is stored (could be S3)
        name: str
            Datasets name by which it will be saved
        path: str
            Default caching directory
        clear: bool
            Clear already existing dataset or try to override

    """
    logger.info("Storing in local cache...")

    # Create meta arrays
    if url.startswith("s3://"):
        name = "/".join(url.split("/")[3:])
        path = url.split("/")[2]
        hb = hub.s3(path)
        cloud = True
    else:
        name = url
        hb = hub.fs(path)
        cloud = False

    special, bucket = _setup_dataset(ds, name, path, hb, clear, cloud)
    dataset, shape = _create_dataset(name, bucket, ds, special, chunksize)

    # print("box", dataset["box"].chunk, dataset["box"].darray.chunk)

    sample_count = chunksize
    for start in range(0, shape[0], sample_count):
        tasks = []
        stop = min(start + sample_count, shape[0])
        logger.info(f"Completing from {start} to {stop} out of {shape[0]} samples")
        t1 = time.time()
        for el in ds:
            if el.startswith("__"):
                continue

            if stop - start <= dataset[el].chunk[0]:
                # When chunk of array is bigger than chunksize, we write in one go
                delay = ds[el][start:stop]
                tasks += [
                    dask.delayed(_cache)(
                        start, stop, el, delay, special, path, cloud, name
                    )
                ]
            else:
                # Otherwise split into chunks and push everything

                def add_task(start, end):
                    delay = ds[el][start:end]
                    return [
                        dask.delayed(_cache)(
                            start, end, el, delay, special, path, cloud, name
                        )
                    ]

                # Consider the case when there is overlap between large chunksizes
                leftover = start % dataset[el].chunk[0]
                jump = 0
                if leftover != 0:
                    jump = dataset[el].chunk[0] - leftover
                    tasks += add_task(start, start + jump)

                for sub_start in range(start + jump, stop, dataset[el].chunk[0]):
                    sub_stop = min(sub_start + dataset[el].chunk[0], stop)
                    tasks += add_task(sub_start, sub_stop)

        dask.compute(*tasks)
        t2 = time.time()
        logger.info(
            f"Completed from {start} to {stop} in {t2-t1}s out of {shape[0]} samples and {len(tasks)} tasks"
        )

    return dataset


def slice_ds(ds: dict, start: int, stop: int, step: int = 1):
    """Slicing dataset according to the given range. This function must be used
    to slice sampler dataset as it takes care of some special keys.

    Parameters
    ----------
    ds: Dict
        Representing dataset as dictionary.
    start: int
        Starting integer where the slicing of the object starts. 
    stop: int
        Integer until which the slicing takes place. The slicing stops at index stop -1 (last element).
    step (optional) : int
        Integer value which determines the increment between each index for slicing. Defaults to 1.

    Returns
    -------
    dict
        Dictionary dataset where each key is sliced by given range

    Examples
    --------
    >>> train = hub_api.slice_ds(ds, 0, 10)
    >>> val = hub_api.slice_ds(ds, 10, -1)
    """
    key = sorted(ds.keys())[-1]
    dslen = ds[key].shape[0]
    if stop == -1:
        stop = dslen
    if stop > dslen:
        raise Exception(
            f"stop is larger than dataset size, stop: {stop}, dataset len: {dslen}"
        )
    if start >= stop:
        raise Exception(f"start >= stop start: {start}, stop: {stop}")
    interval = slice(start, stop, step)
    new_ds = {k: v[interval] for k, v in ds.items() if k != "__special__"}
    if "__special__" in ds:
        new_ds["__special__"] = ds["__special__"]
    return new_ds


def slicep_ds(ds: dict, start: float, end: float):
    """Slicing dataset according to the given range. This function must be used
    to slice sampler dataset as it takes care of some special keys
    Parameters
    ----------
    ds: Dict
        Representing dataset as dictionary.
    start: float
        Starting percentile where the slicing of the object starts
    end: int
        Ending percentile until which the slicing takes place. The slicing stops at index stop 100 (last element)

    Returns
    ----------
    Dictionary dataset where each key is sliced by given range

    Examples
    --------
    >>> train = hub_api.slice_ds(ds, 0, 40)
    >>> val = hub_api.slice_ds(ds, 40, 100)
    """
    key = sorted(list(ds.keys()))[-1]
    cnt = ds[key].shape[0]
    start = int(math.floor(start * cnt / 100.0))
    end = int(math.ceil(end * cnt / 100.0))
    return slice_ds(ds, start, end, 1)


def zoom(
    ds,
    zoom: Union[float, Iterable[float]],
    order: int = 0,
    mode: str = "constant",
    cval: float = 0.0,
    prefilter: bool = True,
):
    """Zooms every component in dict or list (uses scipy zoom)
    Parameters
    ----------
    zoom: List[float] or float
        Zoom on each axis of image by ratio
        Example: zoom = [2, 0.7]
    order: int
    mode: str
        zooming mode(from scipy), default: constant
    cval: float
    prefilter: bool
    Returns
    ----------
    dict or list of zoomed elements
    """
    if isinstance(ds, list):
        ds_new = []
        for el in ds:
            if len(el.shape) not in [3, 4]:
                zoom_arr = dask.delayed(zoom_box)(el, zoom)
                ds_new.append(
                    dask.array.from_delayed(
                        zoom_arr, shape=(el.shape[0],), dtype="object"
                    )
                )
            else:
                zoom_arr = zoom_array(
                    el, zoom, order=order, mode=mode, cval=cval, prefilter=prefilter
                )
                ds_new.append(dask.array.stack(zoom_arr, axis=0))
        return ds_new
    elif isinstance(ds, dict):
        ds_new = {}
        for el in ds:
            if el.startswith("__"):
                continue
            if el == "boxes":
                zoom_arr = dask.delayed(zoom_box)(ds[el], zoom)
                ds_new[el] = dask.array.from_delayed(
                    zoom_arr, shape=(ds[el].shape[0],), dtype="object"
                )
            else:
                zoom_arr = zoom_array(
                    ds[el], zoom, order=order, mode=mode, cval=cval, prefilter=prefilter
                )
                ds_new[el] = dask.array.stack(zoom_arr, axis=0)
        return ds_new
    return dask.array.stack(
        zoom_array(ds, zoom, order=order, mode=mode, cval=cval, prefilter=prefilter),
        axis=0,
    )


def zoom_box(box_arr, zoom):
    if isinstance(zoom, (float, int)):
        zoom = [zoom, zoom]
    new_box = []
    for box in box_arr:
        new_box.append(np.floor(box * (zoom[::-1] * 2)).astype("int32"))
    boxes = np.empty(len(new_box), object)
    boxes[:] = new_box
    return boxes


def zoom_array(
    arr,
    zoom: Union[float, Iterable[float]],
    order: int = 0,
    mode: str = "constant",
    cval: float = 0.0,
    prefilter: bool = True,
):
    if isinstance(zoom, (float, int)):
        zoom = [zoom, zoom]
    assert len(arr.shape) in [3, 4]
    delayed_list = []
    for i in range(0, arr.shape[0]):
        zoom_func = zoom_image if len(arr.shape) == 4 else zoom_bool_arr
        delayed_obj = dask.delayed(zoom_func)(
            arr[i], zoom, order=order, mode=mode, cval=cval, prefilter=prefilter
        )
        delayed_list.append(delayed_obj)
    shape = list(arr.shape[1:])
    shape[0] = int(shape[0] * zoom[0])
    shape[1] = int(shape[1] * zoom[1])
    return [
        dask.array.from_delayed(a, shape=shape, dtype=arr.dtype) for a in delayed_list
    ]


def zoom_bool_arr(
    arr,
    zoom: Union[float, Iterable[float]],
    order: int,
    mode: str,
    cval: float,
    prefilter: bool,
):
    arr = arr.astype("int8")
    arr = ndimage.zoom(
        arr, zoom, order=order, mode=mode, cval=cval, prefilter=prefilter
    )
    return arr.astype("bool")


def zoom_image(
    arr,
    zoom: Union[float, Iterable[float]],
    order: int,
    mode: str,
    cval: float,
    prefilter: bool,
) -> list:
    zarr = [
        ndimage.zoom(
            arr[ch, :, :], zoom, order=order, mode=mode, cval=cval, prefilter=prefilter
        )
        for ch in range(arr.shape[0])
    ]
    return np.stack(zarr, axis=0)
