import boto3
from dataflow.utils import execute
from . import logger

# TODO implement error handling
# TODO clean up of resources


class ECR(object):
    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        region: str = None,
    ):
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        if region is None:
            self.region = session.region_name

        self.client = session.client(service_name="ecr", region_name=self.region,)
        self.aws_account = session.client("sts").get_caller_identity().get("Account")
        self.docker_version = "1.39"

    def _create_repository(self, name):
        """
        aws ecr create-repository --repository-name twitterstream --region $REGION
        """
        try:
            response = self.client.create_repository(
                repositoryName=name, tags=[{"Key": "snark", "Value": "container"}]
            )
            return response
        except Exception as e:
            # handle RepositoryAlreadyExistsException
            logger.debug(f"Container Repository already exists {str(e)}")

    def _build_container(self, docker_name: str, dockerfile: str = "Dockerfile"):
        """
        Build docker
        """
        logger.info("Building docker...")
        cmd = [
            f"DOCKER_API_VERSION={self.docker_version}",
            "docker",
            "build",
            "-t",
            docker_name,
            "-f",
            dockerfile,
            ".",
        ]
        out = execute(cmd)
        logger.info(out)
        return out

    def _tag(self, docker_name, remote_docker_name):
        logger.info("Tagging docker...")
        cmd = [
            f"DOCKER_API_VERSION={self.docker_version}",
            "docker",
            "tag",
            docker_name,
            remote_docker_name,
        ]
        out = execute(cmd)
        logger.info(" ".join(cmd))
        logger.info(out)

    def _docker_auth(self,):
        """
        Authenticate with aws repository docker creds 
        """
        logger.info("Docker authenticating...")
        cmd = [
            f"DOCKER_API_VERSION={self.docker_version}",
            "$(",
            "aws",
            "ecr",
            "get-login",
            "--no-include-email",
            "--region",
            self.region,
            ")",
        ]
        logger.info(" ".join(cmd))
        out = execute(cmd)
        logger.info(out)
        return out

    def _push(self, remote_docker: str):
        cmd = [
            f"DOCKER_API_VERSION={self.docker_version}",
            "docker",
            "push",
            remote_docker,
        ]
        logger.info("Pushing to ECR...")
        logger.info(" ".join(cmd))
        out = execute(cmd)

        logger.debug(out)
        return out

    def push(self, docker_name: str, dockerfile: str = "Dockerfile", build=False):
        """
        Tag the local image with the following command:
        Grab an authorization token from AWS STS:
        Now, push the local image to the ECR repository that you just created:
        """
        logger.warning(
            "You will be automatically logged out from your current docker repository and switch to aws"
        )

        remote_docker = (
            f"{self.aws_account}.dkr.ecr.{self.region}.amazonaws.com/{docker_name}"
        )
        self._create_repository(docker_name.split(":")[0])
        if build:
            self._build_container(remote_docker)
        else:
            self._tag(docker_name, remote_docker)

        self._docker_auth()
        self._push(remote_docker)

    def delete_repository(self, parameter_list):
        """
        aws ecr delete-repository --region $REGION --repository-name twitterstream --force
        """
        pass
