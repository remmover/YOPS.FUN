from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date


class UserSchema(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    model_config = ConfigDict(from_attributes=True)


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    email: str
    number: str | None
    bd_date: date
    additional_data: str | None = Field(max_length=300)


class ContactResponseSchema(ContactSchema):
    id: int = 1
    user: UserResponseSchema | None
    model_config = ConfigDict(from_attributes=True)


class RequestEmail(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    new_password: str
    r_new_password: str