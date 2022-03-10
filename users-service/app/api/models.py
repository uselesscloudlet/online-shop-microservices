from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, PrivateAttr
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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
                'username': 'admin',
                'email': 'admin@ex.com',
                'full_name': 'Ad M In',
                'password': 'admin',
            }
        }


class UserOut(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: str = Field(...)

class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)