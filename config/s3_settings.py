from pydantic.v1 import BaseSettings
from decouple import config


aws_server_public_key = config("AWS_ACCESS_KEY_ID")
aws_server_secret_key = config("AWS_SECRET_ACCESS_KEY")
aws_default_region = config("AWS_DEFAULT_REGION")

class Settings(BaseSettings):
    AWS_SERVER_PUBLIC_KEY: str = aws_server_public_key
    AWS_SERVER_SECRET_KEY: str = aws_server_secret_key
    AWS_DEFAULT_REGION: str = aws_default_region


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')