from pydantic import BaseModel 
from sqlalchemy import Column ,String

from database.db import Base

class User_credential(BaseModel):
    email : str 
    password :str

class User_credentialTable(Base):
    __tablename__ = "sign_up"

    email = Column(String,primary_key=True)
    passqord = Column(String)