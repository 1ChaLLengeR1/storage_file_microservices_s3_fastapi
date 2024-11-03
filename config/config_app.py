from pathlib import Path

# local, dev, prod
ENV_MODE = 'local'

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_FOLDER = BASE_DIR / "download"
