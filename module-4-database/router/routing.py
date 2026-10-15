from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from db.database import get_db

router = APIRouter()


@router.get("/")
def welcome():
    return {"message": "Welcome, you are doing well."}


@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "message": "Database connection successful"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )
