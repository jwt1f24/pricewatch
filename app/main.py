from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.scraper.scraper import scrape
from app.database.database import insert_product, get_user_products, delete_product as db_del_product, get_history, insert_user, get_user
from datetime import datetime, timedelta
from jose import jwt
import bcrypt
import os

# test if API is working (uvicorn app.main:app --reload)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "PriceWatch API"}

# user input endpoint
class ProductRequest(BaseModel):
    user_id: int
    url: str
    target_price: float

# register model
class UserRequest(BaseModel):
    email: str
    password: str

# register endpoint
@app.post("/register")
def register(request: UserRequest):
    hashpw = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    insert_user(request.email, hashpw, datetime.now())
    return {"message": "User registered successfully"}

# login endpoint
@app.post("/login")
def login(request: UserRequest):
    user = get_user(request.email)
    # raise an error if email or password is incorrect or does not exist
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    if not bcrypt.checkpw(request.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    return {"message": "Login successful", "token": token(user_id=user["user_id"])}

# login token endpoint
KEY = os.getenv("KEY")
def token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(days=1)
    }
    return jwt.encode(payload, KEY, algorithm="HS256")

# track product price & store data into database
@app.post("/products")
def add_product(request: ProductRequest):
    scr = scrape(request.url)
    insert_product(request.user_id, scr["name"], request.url, scr["price"], request.target_price, scr["stock"])
    return {"message": "Product added successfully"}

# return products tracked by specific user
@app.get("/products/{user_id}/products")
def get_product(user_id: int):
    return {"products": get_user_products(user_id)}

# delete a product from the database
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db_del_product(product_id)
    return {"message": "Product deleted successfully"}

# return tracking history of a product
@app.get("/products/{product_id}/history")
def history_product(product_id: int):
    return {"history": get_history(product_id)}
