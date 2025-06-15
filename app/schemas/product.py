from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    image_path: str | None = None

    class Config:
        orm_mode = True
