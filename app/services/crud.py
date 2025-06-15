from sqlalchemy.orm import Session
from app.models import product
from app.schemas import product as product_schema

def create_product(db: Session, product_obj: product_schema.ProductCreate):
    db_product = product.Product(**product_obj.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(product.Product).offset(skip).limit(limit).all()
