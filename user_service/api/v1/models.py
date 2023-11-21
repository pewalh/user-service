from pydantic import BaseModel
from typing import Optional


# hard defined types to discouple api from db

class UserBasicInfo(BaseModel):
    email: str
    username: str


class ContactDetailsData(BaseModel):
    address: str
    phoneNumber: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    active: bool
    contactDetails: Optional[ContactDetailsData] = None




