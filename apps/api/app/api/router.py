from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.barcodes import router as barcodes_router
from app.api.routes.categories import router as categories_router
from app.api.routes.customers import router as customers_router
from app.api.routes.inventory import (
    router as inventory_router,
)
from app.api.routes.products import router as products_router
from app.api.routes.stores import (
    router as stores_router,
)
from app.api.routes.taxes import router as taxes_router
from app.api.routes.units import router as units_router


api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(
    auth_router
)

api_router.include_router(
    products_router
)

api_router.include_router(
    categories_router
)

api_router.include_router(
    units_router
)

api_router.include_router(
    taxes_router
)

api_router.include_router(
    barcodes_router
)

api_router.include_router(
    customers_router
)

api_router.include_router(
    inventory_router
)

api_router.include_router(
    stores_router
)
