import os
from os import path
from setuptools import find_packages, setup

project = "dataflow_gegham_test"
version = "0.4.0"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

with open(os.path.join(this_directory, "requirements.txt"), "r") as f:
    requirements = f.readlines()
# requirements = [
#     "awscli==1.18.32\n",
#     "botocore==1.15.32\n",
#     "boto3==1.12\n",
#     "cython\n",
#     "dask[complete]\n",
#     "dask-cloudprovider\n",
#     "tenacity>=5.1.1,<6\n",
#     "pandas\n",
#     "distributed\n",
#     "nap==2.0.0\n",
#     "opencv-python\n",
#     "opencv-contrib-python\n",
#     "tqdm\n",
#     "requests\n",
#     "cachey\n",
#     "fsspec\n",
#     "s3fs\n",
#     "scipy >= 1.4.1,<2\n",
#     "cryptography\n",
#     "ujson\n",
#     "pytest\n",
#     "flask\n",
#     "flask_cors\n",
#     "flask_httpauth\n",
#     "redis\n",
#     "graphviz==0.14",
# ]
# requirements = [x.replace("\n", "") for x in requirements]
setup(
    name=project,
    version=version,
    description="Snark Hub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Snark AI Inc.",
    author_email="support@snark.ai",
    url="https://github.com/snarkai/dataflow",
    packages=["dataflow.cloud", "dataflow.collections", "dataflow.creds"],
    py_modules=[
        "dataflow.config",
        "dataflow.hub_api",
        "dataflow.logger",
        "dataflow.utils",
    ],
    include_package_data=True,
    zip_safe=False,
    keywords="snark-hub",
    python_requires=">=3",
    install_requires=requirements,
    dependency_links=[],
    entry_points={},
)
