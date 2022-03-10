from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

from .utils import PyObjectId

class Good(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(...)
    type: str = Field(...)
    description: str = Field(...)
    price: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            'example': {
                'name': 'Good name',
                'type': 'Good type',
                'description': 'Some description',
                'price': '1000',
            }
        }

class GoodUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    description: Optional[str]
    price: Optional[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            'example': {
                'name': 'Good name',
                'type': 'Good type',
                'description': 'Some description',
                'price': '1000',
            }
        }