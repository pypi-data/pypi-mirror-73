import os
import base64
import requests
import pprint
from dataflow.config import Config
from . import logger

from configparser import ConfigParser
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .aws import AWSSecretsManager


class Creds:
    class __Creds:
        def __init__(
            self,
            name: str = None,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None,
            region: str = "us-east-1",
        ):
            self.data = {}
            self.key = self._setup_encryption()
            self.secret_manager = AWSSecretsManager(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region=region,
            )
            self.name = name
            if self.name is not None:
                self.data = self._get_cred_file(name)

        def _get_cred_file(self, name):
            creds = self.secret_manager.get(name)

            path_name = os.path.abspath(self.name)
            path_name_root = os.path.abspath(os.path.expanduser(self.name))
            if os.path.exists(path_name_root):
                path_name = path_name_root
            if creds is None and os.path.exists(path_name):
                with open(path_name) as configFile:
                    creds, _ = self.parse(configFile)

            if creds is None:
                return {}
                # raise Exception(f"Credential named {self.name} has not been found")
            return creds

        def _setup_encryption(self, salt=b"salt_"):
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend(),
            )
            try:
                secret = Config().get("SECRET_KEY")
            except KeyError:
                # if key not found set basic secret key
                secret = "basicSecret"

            secret_key = secret.encode()
            key = base64.urlsafe_b64encode(kdf.derive(secret_key))
            return key

        def remote(self, name: str, encrypted: bool = True):
            """
            remotely connect to hub and get credential
            """
            token = Config().get("cred_token")
            endpoint = Config().get("endpoint")
            cred_endpoint = Config().get("credential_endpoint")

            response = requests.request(
                "GET",
                "{}{}/{}".format(endpoint, cred_endpoint, name),
                headers={"Authorization": "Bearer {}".format(token)},
            )

            if response.status_code == 200:
                credential = response.json()["payload"]

                if encrypted:
                    f = Fernet(self.key)
                    credential = f.decrypt(credential.encode())

                if not os.path.exists(self.name):
                    os.makedirs(self.name)

                with open(f"{name}", "w") as f:
                    f.write(str(credential, "utf-8"))
                return True
            return False

        def parse(self, configFile):
            try:
                output = {}
                content = configFile.readlines()
                for line in content:
                    if "=" in line:
                        line = line.replace(" ", "").replace("\n", "")
                        key, value = line.split("=")
                        output[key] = value
                return output, "".join(content)
            except Exception:
                pass
            return {}, ""

        def __str__(self):
            pprint.pformat(self.data)

    instance = None

    def __init__(
        self,
        name: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        region: str = None,
        meta: dict = {},
        description: str = None,
        update: bool = False,
    ):
        """
        Finds the credentials in AWS Secret Manager, falls back on File system
        Should return Cred object with loaded secrets
        
        Parameters
        ----------
        name: the name of the key including path if local, if name is None it won't load on instantiation of the object
        aws_access_key_id: (optional) if not provided will be taken from environment variables
        aws_secret_access_key:  (optional) if not provided will be taken from environment variables
        region: (optional) if not provided will be taken from environment variables
        meta: dictionary of credentials to identify if they exists before requesting access
        description: the purpose of the keys
        update: interacvite update to execute
        """
        self.name = name
        self.instance = Creds.__Creds(name)

        valid = self.validate(meta)
        if not valid and not update:
            raise Exception(f"Credential {self.name} not found")
        if not valid and update:
            self.update(meta, description)
        self.instance = Creds.__Creds(name)

    def validate(self, meta):
        for key in meta.keys():
            if self.get(key) is None:
                return False
        return True

    def update(self, meta, description):
        """
        Should update keys
        
        Parameters
        ----------
        keys: dictionary of keys
        description: Description that should be used for keys
        """
        updates = {}
        print(f"Creating secret keys for {self.name} ({description}). Please specify")
        for key in meta.keys():
            if (meta[key] is None or meta[key] == "") and self.get(key) is None:
                value = input(f"{key}: ")
            else:
                or_value = self.get(key) or meta[key]
                le = len(or_value)
                val = or_value[-3:] if le > 3 else ""
                star = "*" * (le - 3 if le > 3 else 3)
                value = input(f"{key} [{star}{val}]: ")
                if value == "":
                    value = or_value
            updates[key] = value
        self.instance.secret_manager.create(self.name, updates, description)

    def show(self):
        pprint(self.instance)

    def get(self, key: str) -> str:
        """
        Should return string
        
        Parameters
        ----------
        key: the key for the value
        """
        if self.name is None:
            logger.error(
                "Please specify the name of the credential before accessing it"
            )
        if key not in self.instance.data:
            # logger.warning(f"No key found with name {key}, returning None")
            return None

        return self.instance.data[key]

    def create(
        self, name: str, secrets: dict = None, path: str = None, version="default"
    ):
        """
        Creates credentials either specified by a dictionary or file path
        
        Parameters
        ----------
        name: the key for the value
        secrets: dictionary of key value pairs for secrets
        path: path to the file for configuration
        version: the version that should be taken from the configuration
        """
        if secrets is None and path is None:
            raise Exception("Please specify secrets or path to the credentials")

        if path is not None:
            secrets = self._load_config_creds(path=path, version=version)

        self.instance.secret_manager.create(name, secrets)

    def get_file(self, encrypted=True):
        if encrypted:
            f = Fernet(self.instance.key)
            msg = str(self.instance.file).encode()
            return f.encrypt(msg)
        else:
            return self.instance.file

    def _load_config_creds(self, path: str, version: str):
        if not os.path.exists(path):
            raise Exception(f"Credentials file path not found at {path}")
        config = ConfigParser()
        config.read(path)
        return {s: dict(config.items(s)) for s in config.sections()}[version]
