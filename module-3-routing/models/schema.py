from pydantic import BaseModel 

class Product(BaseModel):
    id : int
    name : str
    categorie : str 
    price : float
    