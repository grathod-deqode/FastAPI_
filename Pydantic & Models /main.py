from fastapi import FastAPI 

app = FastAPI()

from pydantic import BaseModel 

class Product(BaseModel):
    name : str 
    categorie : str
    price : float 
    

products = [ 
    Product( 
        name = "chai",
        categorie = "bevrage",
        price = 10       
            ),
    Product( 
            name = "coffee",
            categorie = "bevrage",
            price = 150       
                )
            
            ]

@app.get("/")
def start():
    return "Welcome this is capter 2 ."


@app.post("/product")
def create_product( product : Product ):

    return product

       

@app.get("/products", response_model = list[Product])
def get_product():

    return products