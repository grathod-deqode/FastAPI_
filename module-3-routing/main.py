from fastapi import FastAPI

from router import products

app = FastAPI()


app.include_router(products.router)