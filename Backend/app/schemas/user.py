from app.schemas.base import BaseSchema


class ProductDataSchema(BaseSchema):
    name: str
    price: int
