import os
from dotenv import load_dotenv
from config.config_app import ENV_MODE
env_file_path = os.path.join('env', f'{ENV_MODE}.env')

load_dotenv(env_file_path)


def get_env_variable(name_env: str) -> str:
    value = os.getenv(name_env)
    if not value:
        raise Exception(f"Missing required environment variable: {name_env}")
    return value
