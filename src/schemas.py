from pydantic import BaseModel, Field
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_num: str
    birthday: date
   
class ContactResponse(ContactBase):
    id: int 

    class Config:
        orm_mode = True

class ContactUpdate(BaseModel):
    email: str
    phone_num: str