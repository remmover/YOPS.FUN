import re
from typing import List

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
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


class ImageDb(BaseModel):
    id: int
    image: str
    small_image: str
    about: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CropImageDb(BaseModel):
    image_id: int
    width: int
    height: int


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


class CommentDb(BaseModel):
    id: int
    comment: str
    emo_joy: int
    emo_anger: int
    emo_sadness: int
    emo_surprise: int
    emo_disgust: int
    emo_fear: int
    created_at: datetime
    updated_at: datetime
    image_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class CommentCreateSchema(BaseModel):
    id: int
    text: str = Field(max_length=300)


class CommentShowSchema(BaseModel):
    comment: str


class CommentShowAllSchema(BaseModel):
    comments: List[CommentShowSchema]


class CommentUpdateSchema(BaseModel):
    comment_id: int
    image_id: int
    comment: str = Field(max_length=300)


class CommentDeleteSchema(BaseModel):
    comment_id: int
    image_id: int


class TagResponseSchema(BaseModel):
    name: str


class ReadTagResponseSchema(BaseModel):
    tags: list


class TagSchema(BaseModel):
    name: str = Field(min_length=3, max_length=24)

    @field_validator("name")
    @classmethod
    def adjust_name(cls, name: str):
        # delete first/last/duplicate spaces
        name = ' '.join(name.split())
        pattern = r"(^\d|^.*[/&!@`^%$#+])"
        if re.search(pattern, name):
            raise ValueError(f"Tag '{name}' cannot start with digit " \
                             "and cannot contain any special symbols.")
        return name
