from fastapi import FastAPI 
from router import routing 

app = FastAPI()

app.include_router(routing.router)


