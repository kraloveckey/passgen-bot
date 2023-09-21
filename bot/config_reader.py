from typing import Optional

from pydantic import BaseModel, BaseSettings, SecretStr, FilePath, validator


class CoreSettings(BaseModel):
    wordfile: FilePath
    min: int = 4
    max: int = 48
    default: int = 8
    prefixes_suffixes_by_default: bool = False
    separators_by_default: bool = True


class Redis(BaseModel):
    host: Optional[str]
    port: int = 6379
    db_num: int = 0


class Settings(BaseSettings):
    bot_token: SecretStr
    redis: Optional[Redis]
    storage_mode: str
    chars: CoreSettings

    @validator("storage_mode")
    def validate_storage_mode(cls, v: str, values):
        v = v.lower()
        if v not in {"memory", "redis"}:
            raise ValueError("Only 'memory' and 'redis' values are allowed.")
        if v == "redis" and (not values.get("redis") or not values["redis"].host):
            raise ValueError("Backend mode 'redis' selected, but no host is provided; set it via REDIS__HOST variable.")
        return v

    class Config:
        env_file = 'config/.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

settings = Settings()
