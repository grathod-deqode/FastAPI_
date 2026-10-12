from pydantic import BaseModel 

class Product(BaseModel):
    name : str
    categorie : str 
    price : float
    