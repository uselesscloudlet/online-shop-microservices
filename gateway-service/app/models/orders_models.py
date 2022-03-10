from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from bson import ObjectId
from datetime import datetime

from .utils import PyObjectId
from .goods_models import Good


class OrderStatus(str, Enum):
    CREATED = 'created'
    ON_THE_WAY = 'on the way'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


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
