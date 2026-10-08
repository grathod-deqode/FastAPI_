from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def home():
    return  "Welcome Gaurav, you fastAPI journey start now ."

@app.get("/items/{item_id}")
def get_item(item_id : int):
    return {"item id " : item_id }



@app.get("/search")
def search(item : str = ""):
    return {"item is " : item}


