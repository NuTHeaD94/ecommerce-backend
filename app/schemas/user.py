from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    email: str

    class Config:
        orm_mode = True