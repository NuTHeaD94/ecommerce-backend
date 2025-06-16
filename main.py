from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.schemas import user as user_schema
from app.crud import user as user_crud
from app.schemas import product as product_schema
from app.crud import product as product_crud
from app.core import security
from app.core.dependencies import get_current_user
from sqlalchemy import text
from sqlalchemy.engine import Row
from typing import List
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ecommerce Backend API",
    description="Production-ready Ecommerce API with authentication, user management, and product management.",
    version="1.0.0"
)

# CORS settings
origins = [
    "http://localhost:5173",  # your local frontend
    "https://your-production-frontend.com"  # later, when deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only, we can restrict it later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registration
@app.post("/register", response_model=user_schema.UserOut)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return user_crud.create_user(db, user.username, user.email, user.password)

# Login
@app.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = security.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# Create Product
@app.post("/products/")
def create_product(
    product: product_schema.ProductCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    return product_crud.create_product(db, product)

# Get Single Product
@app.get("/products/{product_id}", response_model=product_schema.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Get All Products
@app.get("/products", response_model=List[product_schema.ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    return product_crud.get_all_products(db)


# TEMPORARY DB CLEANUP ROUTE (for Render internal DB cleanup)

@app.post("/debug-cleanup")
def cleanup_database(db: Session = Depends(get_db)):
    try:
        sql = text("ALTER TABLE products DROP COLUMN IF EXISTS image_path;")
        db.execute(sql)
        db.commit()
        return {"message": "Cleanup successful. 'image_path' column dropped."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/debug-one-product")
def debug_one_product(db: Session = Depends(get_db)):
    try:
        sql = text("SELECT * FROM products LIMIT 1")
        result = db.execute(sql).fetchone()
        if result is None:
            return {"message": "No product found."}
        # Convert Row object to dict properly
        row_dict = dict(result._mapping)
        return {"raw_product": row_dict}
    except Exception as e:
        return {"error": str(e)}