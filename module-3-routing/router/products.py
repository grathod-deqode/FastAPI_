from fastapi import APIRouter 

from models.schema import Product
router = APIRouter()


products = [{"name": "chai", "categorie": "bevrage" ,"price" : 10},
            {"name": "coffee", "categorie": "bevrage" ,"price" : 150}]

@router.get("/")
def wel_come():
    return "Welcome you are learrning routing."


@router.post("/products")
def get_products(product : Product):
    return product



@router.get("/products")
def get_products():
    return products