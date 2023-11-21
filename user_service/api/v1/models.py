from pydantic import BaseModel
from typing import Optional


# hard defined types to discouple api from db



class ContactDetailsData(BaseModel):
    address: str
    phoneNumber: str
    

class UserBasicInfo(BaseModel):
    email: str
    username: str

class UserInfo(UserBasicInfo):
    id: int
    active: bool

class UserInfoFull(UserInfo):
    contactDetails: Optional[ContactDetailsData]




