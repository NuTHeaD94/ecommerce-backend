from sqlalchemy.orm import Session
from app.models import product as product_model
from app.schemas import product as product_schema

def create_product(db: Session, product: product_schema.ProductCreate, image_path: str = None):
    db_product = product_model.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_path=image_path
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
