from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime


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


class RequestEmail(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    new_password: str
    r_new_password: str


#{{{ Image

class ImageDb(BaseModel):
    id: int
    image: str
    small_image: str
    about: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ImageAboutUpdateSchema(BaseModel):
    image_id: int
    about: str


class ImageAboutUpdateResponseSchema(BaseModel):
    image_id: int
    message: str


class ReturnMessageResponseSchema(BaseModel):
    message: str


class SmallImageReadResponseSchema(BaseModel):
    image_id: int
    small_image_url: str
    short_about: str
    model_config = ConfigDict(from_attributes=True)


class ImageReadResponseSchema(BaseModel):
    image_id: int
    image_url: str
    about: str
    model_config = ConfigDict(from_attributes=True)
#}}}
