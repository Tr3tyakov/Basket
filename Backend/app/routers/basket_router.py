from fastapi import APIRouter, Depends, Response, status
from starlette.requests import Request

from app.core.context import ApplicationContext
from app.models.product import Product, GetProductResponse
from app.schemas.user import ProductDataSchema
from app.services.product_service import BasketService

basket_router = APIRouter(prefix="/api", tags=["product"])


@basket_router.post("/create_product", description="Создание продукта")
async def create_product(
        request: Request,
        data: ProductDataSchema,
        service: BasketService = Depends(),
        context: ApplicationContext = Depends(ApplicationContext.get_context),
) -> None:
    return await service.create_product(context, data=data)


@basket_router.get("/products", description="Получение продуктов", response_model=GetProductResponse)
async def get_products(
        service: BasketService = Depends(),
        context: ApplicationContext = Depends(ApplicationContext.get_context),
) -> GetProductResponse:
    cart, total_price = await service.get_products(context)
    return GetProductResponse(
        total_price=total_price,
        cart=cart
    )
