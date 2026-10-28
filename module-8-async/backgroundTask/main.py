
import os
import ssl
import smtplib

from email.message import EmailMessage
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from database.db import get_db, engine
from models.model import Base, UserTable
from models.schema import UserRegister, UserResponse
from middleware.logging import request_logging

from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

app.middleware("http")(request_logging)

Base.metadata.create_all(bind=engine)

password_hash = PasswordHash.recommended()


def send_email(email, name):
    try:
        sender_email = os.getenv("SMTP_EMAIL")
        app_password = os.getenv("SMTP_PASSWORD")

        if not sender_email or not app_password:
            print("Email error: SMTP credentials are missing")
            return

        msg = EmailMessage()
        msg["Subject"] = "Welcome to Our Application"
        msg["From"] = sender_email
        msg["To"] = email

        msg.set_content(
            f"Hello {name},\n\n"
            "Your registration is successful.\n"
            "Welcome to our application.\n\n"
            "Thank you!"
        )

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            context=context,
            timeout=20
        ) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

        print("Email sent successfully")

    except Exception as e:
        print(f"Email error: {type(e).__name__}: {e}")


@app.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    existing_user = db.query(UserTable).filter(
        UserTable.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = password_hash.hash(user.password)

    new_user = UserTable(
        name=user.name,
        email=user.email,
        password=hashed_password,
        address=user.address
    )

    db.add(new_user)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    db.refresh(new_user)

    background_tasks.add_task(
        send_email,
        new_user.email,
        new_user.name
    )

    return new_user
