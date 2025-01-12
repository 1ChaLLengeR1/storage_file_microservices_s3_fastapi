from pathlib import Path

# local, dev, prod
ENV_MODE = 'dev'

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_FOLDER = BASE_DIR / "download"
TMP_FOLDER = BASE_DIR / "tmp"
KEYS_SQL = BASE_DIR / "database" / "sql"

# Test Paths
IMG1 = BASE_DIR / "consumer" / "common" / "test1.jpg"
IMG2 = BASE_DIR / "consumer" / "common" / "test2.jpg"
IMG3 = BASE_DIR / "consumer" / "common" / "test3.jpg"
IMG4 = BASE_DIR / "consumer" / "common" / "test4.jpg"
ZIP1 = BASE_DIR / "consumer" / "common" / "test_download.rar"
