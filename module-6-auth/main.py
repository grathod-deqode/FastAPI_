
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.db import engine, get_db
from models.schema import User_credential, User_credentialTable
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
import os

app = FastAPI()

password_hash = PasswordHash.recommended()

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# Development-only token blocklist
blacklisted_tokens = set()


def create_access_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": email,
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


@app.get("/db-check")
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"message": "Database connected successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )


@app.get("/")
def welcome():
    return "Now you are learning Authentication and Authorization."


@app.post("/user_signup")
def sign_up(
    user_credential: User_credential,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User_credentialTable).filter(
        User_credentialTable.email == user_credential.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = password_hash.hash(user_credential.password)

    new_user = User_credentialTable(
        email=user_credential.email,
        passqord=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Signup Successfully",
        "email": new_user.email
    }


@app.post("/login")
def login(
    user_credential: User_credential,
    db: Session = Depends(get_db)
):
    user = db.query(User_credentialTable).filter(
        User_credentialTable.email == user_credential.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not password_hash.verify(
        user_credential.password,
        user.passqord
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.email)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    if token in blacklisted_tokens:
        raise HTTPException(
            status_code=401,
            detail="Token has been invalidated. Please login again."
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return email

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@app.get("/profile")
def profile(
    email: str = Depends(get_current_user)
):
    return {
        "message": "You are authenticated",
        "email": email
    }


@app.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    # Validate token before invalidating it
    email = get_current_user(credentials)

    blacklisted_tokens.add(token)

    return {
        "message": "Logout successful",
        "email": email
    }
