from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def home():
    return  "Welcome Gaurav, you fastAPI journey start now ."