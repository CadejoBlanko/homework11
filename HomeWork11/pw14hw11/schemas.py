from pydantic import BaseModel
from datetime import date

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    birthdate: date

class Contact(ContactCreate):
    id: int

    class Config:
        orm_mode = True