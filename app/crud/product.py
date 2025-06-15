from sqlalchemy.orm import Session
from app.models import product as product_model
from app.schemas import product as product_schema

# Create Product Function
def create_product(db: Session, product: product_schema.ProductCreate, image_path: str = None):
    db_product = product_model.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        # image_path=image_path  # since you removed image_path column
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Get Single Product Function (optional but useful)
def get_product(db: Session, product_id: int):
    return db.query(product_model.Product).filter(product_model.Product.id == product_id).first()

# ✅ Get All Products Function (THE MAIN FIX)
def get_all_products(db: Session):
    return db.query(product_model.Product).all()

