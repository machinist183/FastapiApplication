from pydantic import BaseSettings
class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_name : str
    database_password : str
    database_username : str
    algorithms : str
    token_expirE_time : int
    secret_key :  str

    class Config:
        env_file = ".env"

settings = Settings()
