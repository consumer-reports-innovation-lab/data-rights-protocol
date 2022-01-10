from .base import BaseModel
from pydantic import EmailStr,  validator

class IdentityPayload(BaseModel):
    iss: str
    aud: str
    sub: str

    name: str

    email: EmailStr
    verified_email: bool = False

    phone_number: str
    verified_phone_number: bool = False

    address: str
    verified_address: bool = False
    
    power_of_attorney: str

    def dict(self):
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
        else:
            ret['email'] = self.email

        if self.verified_phone_number:
            ret['phone_number_verified'] = self.phone_number
        else:
            ret['phone_number'] = self.phone_number

        if self.verified_address:
            ret['address_verified'] = self.address
        else:
            ret['address'] = self.address

        return ret

    @validator('iss')
    def issuer_set(cls, v):
        if v is None:
            raise ValueError("Must set issuer claim")

    @validator('aud')
    def audience_set(cls, v):
        if v is None:
            raise ValueError("Must set audience claim")
