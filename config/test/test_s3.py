from config.s3_deps import s3_auth
from botocore.client import BaseClient
from botocore.exceptions import ClientError
import pytest

def test_s3_connection():
    try:

        s3: BaseClient = s3_auth()
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])

        if not buckets:
            pytest.fail("S3 buckets list is empty")

    except ClientError as e:
        pytest.fail(f"S3 connection failed: {e}")
