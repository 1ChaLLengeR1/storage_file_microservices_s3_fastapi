import os
from dotenv import load_dotenv
from config.config_app import ENV_MODE, BASE_DIR
import uuid

env_file_path = os.path.join(BASE_DIR, "env", f"{ENV_MODE}.env")
load_dotenv(env_file_path)


def is_valid_uuid(val: str) -> bool:
    try:
        uuid.UUID(val)  # Próbujemy zamienić na UUID
        return True
    except ValueError:
        return False


def get_env_variable(name_env: str) -> str:
    value = os.getenv(name_env)
    if not value:
        raise Exception(f"Missing required environment variable: {name_env}")
    return value
