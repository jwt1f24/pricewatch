from fastapi import FastAPI
from pydantic import BaseModel
from app.scraper.scraper import scrape
from app.database.database import insert_product, get_user_products, delete_product as db_del_product, get_history, insert_user
from datetime import datetime
import bcrypt

app = FastAPI()

# test if API is working
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
    bcrypt.hashpw(UserRequest.password.encode('utf-8'), bcrypt.gensalt())
    insert_user(request.email, request.password, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    return {"message": "User registered successfully"}


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
