import os
from pydantic.v1 import BaseSettings
from consumer.helper.validators import get_env_variable
from config.config_app import ENV_MODE

aws_server_public_key = get_env_variable("AWS_ACCESS_KEY_ID")
aws_server_secret_key = get_env_variable("AWS_SECRET_ACCESS_KEY")
aws_default_region = get_env_variable("AWS_DEFAULT_REGION")

env_file_path = os.path.join('env', f'{ENV_MODE}.env')


class Settings(BaseSettings):
    AWS_SERVER_PUBLIC_KEY: str = aws_server_public_key
    AWS_SERVER_SECRET_KEY: str = aws_server_secret_key
    AWS_DEFAULT_REGION: str = aws_default_region

    class Config:
        env_file = env_file_path
        env_file_encoding = 'utf-8'


settings = Settings(_env_file=env_file_path, _env_file_encoding='utf-8')
