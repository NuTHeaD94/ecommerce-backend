from fastapi import HTTPException, status
from app.core.security import verify_password, get_password_hash, create_access_token
from app.crud import user as user_crud
from sqlalchemy.orm import Session

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user and return user object if valid"""
    user = user_crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_user_token(username: str):
    """Create access token for user"""
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

def validate_user_registration(db: Session, username: str, email: str):
    """Validate user registration data"""
    # Check if username already exists
    if user_crud.get_user_by_username(db, username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if user_crud.get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return True