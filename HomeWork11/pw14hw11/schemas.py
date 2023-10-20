from pydantic import BaseModel, Field
from datetime import datetime, date


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


class UserModel(BaseModel):
    username: str
    email: str
    password: str = Field(min_length=6)

    
class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"