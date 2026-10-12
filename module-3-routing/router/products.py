from fastapi import APIRouter 

router = APIRouter()


@router.get("/products")
def wel_come():
    return "Welcome you are learrning routing."