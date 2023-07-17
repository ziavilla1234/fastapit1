from pydantic_settings import BaseSettings, SettingsConfigDict



class SettingsModel(BaseSettings):
    database_name: str
    secret_key:str
    access_token_expire_mins:int

    model_config = SettingsConfigDict(env_file="envvars")



envvars = SettingsModel()