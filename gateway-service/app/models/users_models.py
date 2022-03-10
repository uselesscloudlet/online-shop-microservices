from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime

from .utils import PyObjectId


class UserIn(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    username: str = Field(...)
    email: str = Field(...)
    full_name: str = Field(...)
    user_type: str = "client"
    password: str = Field(...)
    created_at: str = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            'example': {
                'username': 'test',
                'email': 'test@ex.com',
                'full_name': 'T T T',
                'password': 'test',
            }
        }


class UserOut(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: str = Field(...)

class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)