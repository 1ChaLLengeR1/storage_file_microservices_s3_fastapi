# catalog
COLLECTION_BUCKETS = "/collection/buckets"
COLLECTION_CATALOGS = "/collection/catalogs/{name_bucket}"
COLLECTION_ONE_CATALOG = "/collection/catalog/{id}"
DELETE_CATALOG = "/delete/catalog/{id}"
DOWNLOAD_CATALOG = "/download/catalog/{id}"
CREATE_CATALOG = "/catalog/create"
COLLECTION_ONE_FILES = "/collection/one/files"

# files
UPLOAD_FILES = "/files/upload/{name_bucket}"
COLLECTION_FILES = "/files/collection/{catalog_id}"
COLLECTION_ONE_FILE = "/files/collection/one/{file_id}"
DELETE_FILES = "/files/delete/{name_bucket}"
DOWNLOAD_FILE = "/download/file/{file_id}"

# task
TASK_ID = "/tasks/{task_id}"

# test
TEST_ROUTER = "/test"
