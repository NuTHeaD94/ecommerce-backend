from fastapi import APIRouter
from . import users, product, auth

router = APIRouter()

# Include individual routers
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(product.router, prefix="/products", tags=["Products"])
