# main.py
from fastapi import FastAPI, Depends, HTTPException, Form, UploadFile, File # type: ignore
from pydantic import BaseModel, EmailStr, Field # type: ignore
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker, Session # type: ignore

app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate,db:Session=Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=UserResponse)
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.email = user.email if user.email is not None else db_user.email
    db.commit()
    db.refresh(db_user)
    return db_user


"""class User(BaseModel):
    name: str = Field(pattern='^[a-zA-Z0-9_.-]+$')
    email: EmailStr
    age: int = Field(gt=0)


 @app.post("/login/")
async def login(user_name: str = Form(...), password: str = Form(...)):
    return {"username": user_name, "message": "Login successful" }

@app.post("/uploadfile/")
async def create_uploadfile(file: UploadFile = File(...) ):
    return {"filename": file.filename}

@app.post("/uploadfiles/")
async def create_uploadfiles(files: List[UploadFile] = File(...) ):
    return {"filenames": [file.filename for file in files]}

@app.post("/savefile/")
async def save_uploadfile(file: UploadFile = File(...) ):
    with open(f'uploads/{file.filename}', "wb") as f:
        f.write(file.file.read())
    return {"message": f"file '{file.filename}' save successfully"}

@app.post("/register")
async def register_user(user: User):
    return user

@app.post("/user")
async def create_user(user: User):
    return {
        "sended user": user.name,
        "sended email": user.email,
        "sended age": user.age,
    }

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI Nimrod!"}

@app.get("/user/{id}", response_model= User)
async def get_user(id: int):
    return {"name": "pepe", "age": "18"}

@app.get("/user/{id}/details")
def details_user(id: int, include_email: bool=False):
    if include_email:
        return {"id": id, "include_email": "Included email"}
    else:
        return {"id": id, "include_email": "Not included email"}

@app.post("/item")
def create_item(name: str, price: float):
   return {"name": name, "price":price}

@app.put("/item/{id}")
def update_item(id: int ,name: str, price: float):
   return {"id": id, "name": name, "price":price}

@app.delete("/item/{id}")
def delete_item(id: int):
   return {"message": f"Item {id} deleted" }
"""
