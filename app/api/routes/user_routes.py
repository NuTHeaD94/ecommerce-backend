from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.crud import user as user_crud
from app.core import security
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=user_schema.UserOut)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return user_crud.create_user(db, user.username, user.email, user.password)

@router.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = security.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
