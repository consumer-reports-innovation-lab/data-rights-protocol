from pydantic import BaseSettings
from pydantic import BaseModel as PydBaseModel
import jwt
import os

class Settings(BaseSettings):
    jwt_algo: str = "HS256"
    jwt_secret: str = "lolchangeme"

settings = Settings()

def jwt_dumps(value: 'IdentityPayload',
              secret: str = settings.jwt_secret,
              algo: str = settings.jwt_algo) -> str:
    """
    Serialize a JWT to a compact encoding
    """
    return jwt.encode(
        value.dict(),
        secret,
        algo
    )

class BaseModel(PydBaseModel):
    class Config:
        use_enum_values = True
        json_encoders = {
            'IdentityPayload': jwt_dumps,
        }
