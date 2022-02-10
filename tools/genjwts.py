from pydantic import BaseSettings
import jwt

class Settings(BaseSettings):
    jwt_algo: str = "HS256"
    jwt_secret: str = "lolchangeme"

settings = Settings()

def dumps(value: 'IdentityPayload') -> str:
    """
    Serialize a JWT to a compact encoding
    """
    return jwt.encode(
        value.dict(),
        settings.jwt_secret,
        settings.jwt_algo
    )
