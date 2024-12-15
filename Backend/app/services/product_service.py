from typing import List, Tuple

from sqlalchemy import select, func

from app.core.context import ApplicationContext
from app.models.product import Product
from app.schemas.user import ProductDataSchema


class BasketService:

    async def create_product(
            self, context: ApplicationContext, data: ProductDataSchema
    ) -> None:
        async with context.database.session_context() as session:
            result = await session.execute(select(Product).where(Product.name == data.name))
            existent_product = result.scalar_one_or_none()
            if existent_product:
                existent_product.count += 1
                return

            product = Product(**data.model_dump(), count=1)
            session.add(product)

    async def get_products(self, context: ApplicationContext) -> Tuple[Product, int]:
        async with context.database.session_context() as session:
            result = await session.execute(select(Product))

            products = result.scalars().fetchall()
            price_result = await session.execute(select(func.SUM(Product.price)))
            total_price = price_result.scalar()
            return products, total_price
