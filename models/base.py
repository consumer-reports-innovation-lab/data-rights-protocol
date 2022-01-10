from pydantic import BaseModel as PydBaseModel
import jwt
import os

JWT_SECRET=os.environ.get("JWT_SECRET", "lolchangeme")

def jwt_dumps(value):
    return jwt.encode(value.dict(), JWT_SECRET, "HS256")

class BaseModel(PydBaseModel):
    class Config:
        use_enum_values = True
        json_encoders = {
            'IdentityPayload': lambda v: jwt_dumps(v),
        }
