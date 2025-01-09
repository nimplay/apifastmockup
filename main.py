# main.py
from fastapi import FastAPI, Form, UploadFile, File # type: ignore
from pydantic import BaseModel, EmailStr, Field # type: ignore
from typing import List

app = FastAPI()

class User(BaseModel):
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
