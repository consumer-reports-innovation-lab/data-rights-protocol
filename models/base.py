from pydantic import BaseModel as PydBaseModel
import jwt
import os
from tools.genjwts import dumps as jwt_dumps

class BaseModel(PydBaseModel):
    class Config:
        use_enum_values = True
        json_encoders = {
            'IdentityPayload': jwt_dumps,
        }
