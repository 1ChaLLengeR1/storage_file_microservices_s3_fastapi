from config.celery_config import app
from config.s3_deps import s3_auth
from urllib.parse import quote_plus


@app.task
def collection_one(bucket_name: str, name_file: str) -> str:
    s3 = s3_auth()
    object_key = name_file
    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': bucket_name, 'Key': object_key},
                                    ExpiresIn=3600)

    return url


@app.task
def collection_buckets():
    s3 = s3_auth()
    response = s3.list_buckets()
    return response['Buckets']


@app.task
def collection_catalogs(bucket_name: str, prefix: str):
    s3 = s3_auth()
    paginator = s3.get_paginator('list_objects_v2')

    folder_details = {
        'folder_url': f"https://{bucket_name}.s3.amazonaws.com/{quote_plus(prefix)}",
        'total_size': 0,
        'objects': [],
        'subfolders': []
    }

    # Lista obiektów w katalogu
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, Delimiter='/'):
        for obj in page.get('Contents', []):
            object_info = {
                'key': obj['Key'],
                'size': obj['Size'],
                'url': f"https://{bucket_name}.s3.amazonaws.com/{quote_plus(obj['Key'])}"
            }
            folder_details['objects'].append(object_info)
            folder_details['total_size'] += obj['Size']

        # Lista podfolderów w katalogu
        for common_prefix in page.get('CommonPrefixes', []):
            subfolder_prefix = common_prefix['Prefix']
            subfolder_details = collection_catalogs(bucket_name, subfolder_prefix)
            folder_details['subfolders'].append(subfolder_details)

    return folder_details
