from fastapi import APIRouter ,HTTPException ,Header ,Cookie

from models.schema import Product
router = APIRouter()


products = { 1 : {"name": "chai", "categorie": "bevrage" ,"price" : 10},
            
            2 :{"name": "coffee", "categorie": "bevrage" ,"price" : 150}
            }

@router.get("/")
def wel_come():
    return "Welcome you are learrning routing."


@router.post("/products")
def get_products(product : Product):
    return product



@router.get("/products")
def get_products(user_agent : str = Header()):
    return {
        "products" : products ,
        "user agent" : user_agent
    }


@router.get("/products/{id}")
def get_product_by_id(id : int):

    if id != 1:
        raise HTTPException (
            status_code= 404 ,
            detail="product is not found"

        )
    return {
        "product id " : id,
        "prodoct details " : products[id]
    }