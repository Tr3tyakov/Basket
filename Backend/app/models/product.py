from typing import List

from sqlalchemy import Column, Integer, String

from app.models.base.base import BaseModel
from app.schemas.base import BaseSchema


class Product(BaseModel):
    """Продукт"""

    name = Column(String, nullable=False, comment="Наименование продукта")
    price = Column(Integer, nullable=False, comment="Стоимость продукта")
    count = Column(Integer, nullable=False, comment="Количество продуктов")


class ProductSchema(BaseSchema):
    name: str
    price: int
    count: int


class GetProductResponse(BaseSchema):
    cart: List[ProductSchema]
    total_price: int
