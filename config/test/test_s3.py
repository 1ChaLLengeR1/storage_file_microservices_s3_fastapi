import pytest
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from config.s3_deps import s3_auth


def test_s3_connection():
    s3: BaseClient = s3_auth()

    try:
        response = s3.list_buckets()
    except ClientError as e:
        pytest.fail(f"S3 connection failed: {e}")

    buckets = response.get('Buckets', [])

    assert response['ResponseMetadata']['HTTPStatusCode'] == 200, "S3 request did not succeed"
    assert isinstance(buckets, list), "Buckets should be a list"
    assert buckets, "S3 buckets list is empty"
