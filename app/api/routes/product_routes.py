from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from schemas import product as product_schema
from crud import product as product_crud
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "backend/app/uploads/products"

@router.post("/products/", response_model=product_schema.ProductOut)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: product_schema.User = Depends(get_current_user)
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    product_data = product_schema.ProductCreate(
        name=name,
        description=description,
        price=price,
        stock=stock
    )
    return product_crud.create_product(db, product_data, image_path=file_path)
