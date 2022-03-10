from bson import ObjectId
from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Optional
from enum import Enum
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


class OrderStatus(str, Enum):
    CREATED = 'created'
    ON_THE_WAY = 'on the way'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


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


class OrderIn(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: str = Field(...)
    goods: List[Good] = Field(...)
    delivery_addr: str = Field(...)
    status: OrderStatus = OrderStatus.CREATED
    created_at: str = datetime.now()

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            'example': {
                'user_id': 'random_id',
                'goods': [
                    {
                        'name': 'Good name',
                        'type': 'Good type',
                        'description': 'Some description',
                        'price': '1000',
                    },
                    {
                        'name': 'Good name',
                        'type': 'Good type',
                        'description': 'Some description',
                        'price': '1000',
                    }
                ],
                'delivery_addr': 'Some address'
            }
        }


class OrderOut(BaseModel):
    goods: List[Good] = Field(...)
    delivery_addr: str = Field(...)
    status: OrderStatus = Field(...)
    created_at: str = Field(...)

    class Config:
        use_enum_values = True

class OrderUpdate(BaseModel):
    goods: Optional[List[Good]]
    delivery_addr: Optional[str]
    status: Optional[OrderStatus]
    created_at: Optional[str]