import boto3
from botocore.client import BaseClient, Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, UnknownServiceError
from config.s3_settings import settings


def s3_auth() -> BaseClient:
    try:
        s3 = boto3.client(service_name='s3', aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
                          aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
                          region_name=settings.AWS_DEFAULT_REGION,
                          config=Config(signature_version='s3v4')
                          )

        return s3
    except NoCredentialsError:
        raise Exception("Error: Missing AWS credentials.")
    except PartialCredentialsError:
        raise Exception("Error: Incomplete AWS credentials.")
    except UnknownServiceError as e:
        raise Exception(f"Error: Unknown AWS service. {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
