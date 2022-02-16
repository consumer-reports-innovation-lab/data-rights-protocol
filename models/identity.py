from .base import BaseModel
from typing import Optional
from pydantic import EmailStr,  validator


class IdentityPayload(BaseModel):
    iss: str
    aud: str
    sub: Optional[str]

    name: Optional[str]

    email: Optional[EmailStr]
    verified_email: Optional[bool] = False

    phone_number: Optional[str]
    verified_phone_number: Optional[bool] = False

    address: Optional[str]
    verified_address:Optional[bool] = False
    
    power_of_attorney: Optional[str]

    def dict(self, **kwargs):
        # construct base dict
        ret = dict(
            iss=self.iss,
            aud=self.aud,
            sub=self.sub,
            name=self.name,
            power_of_attorney=self.power_of_attorney
        )

        if self.verified_email:
            ret['email_verified'] = self.email
        elif self.email is None:
            pass
        else:
            ret['email'] = self.email

        if self.verified_phone_number:
            ret['phone_number_verified'] = self.phone_number
        elif self.phone_number is None:
            pass
        else:
            ret['phone_number'] = self.phone_number

        if self.verified_address:
            ret['address_verified'] = self.address
        elif self.address is None:
            pass
        else:
            ret['address'] = self.address

        return ret

    @validator('iss')
    def issuer_set(cls, v):
        if v is None:
            raise ValueError("Must set issuer claim")
        return v

    @validator('aud')
    def audience_set(cls, v):
        if v is None:
            raise ValueError("Must set audience claim")
        return v
