import boto3
import ujson as json
from botocore.exceptions import ClientError
from . import logger


class AWSSecretsManager(object):
    """
    Simple wrapper for AWS secrets manager
    """

    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        region: str = None,
        prefix: str = "snark_",
    ):
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region,
        )
        if region is None:
            region = session.region_name
        self.prefix = prefix
        self.client = session.client(service_name="secretsmanager", region_name=region,)

    def create(self, name: str, secret: dict, description: str = "Secret for Snark"):
        try:
            self.client.create_secret(
                Name=self.prefix + name,
                Description=description,
                # KmsKeyId="string",
                # SecretBinary=b"bytes",
                SecretString=json.dumps(secret),
                # Tags=[{"Key": "string", "Value": "string"},],
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceExistsException":
                logger.warning(f"Couldn't create new secret: '{name}' already existed.")
                self.update(name, secret)

    def update(self, name: str, secret: dict):
        logger.info(f"Updating secrets '{name}'")
        self.client.update_secret(
            SecretId=self.prefix + name,
            # ClientRequestToken="string",
            Description=f"Secret for {name}",
            # KmsKeyId="string",
            # SecretBinary=b"bytes",
            SecretString=json.dumps(secret),
        )

    def _get(self, name: str) -> dict:
        try:
            return self.client.get_secret_value(SecretId=self.prefix + name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                logger.debug("The requested secret " + name + " was not found on AWS")
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                logger.debug("The request was invalid due to:", e)
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                logger.debug("The request had invalid params:", e)
            return None

    def get(self, name: str) -> dict:
        resp = self._get(name)
        if resp:
            # Secrets Manager decrypts the secret value using the associated KMS CMK
            # Depending on whether the secret was a string or binary, only one of these fields will be populated
            if "SecretString" in resp:
                text_secret_data = resp["SecretString"]
            else:
                logger.error("No binary secret support")
                # TODO add later binary_secret_data = get_secret_value_response["SecretBinary"]
            return json.loads(text_secret_data)
        return None

    def get_arn(self, name: str) -> dict:
        resp = self._get(name)
        if resp:
            if "ARN" in resp:
                return resp["ARN"]
        return None

    def delete(self, name: str):
        """
        Deleting a secret will take 7 days and its difficult to recreate
        """
        return self.client.delete_secret(SecretId=name, ForceDeleteWithoutRecovery=True)
