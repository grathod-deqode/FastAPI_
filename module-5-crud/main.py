from fastapi import FastAPI 
from router import rout
app = FastAPI()

app.include_router(rout.router)