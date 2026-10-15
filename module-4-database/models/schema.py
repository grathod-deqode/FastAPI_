from pydantic import BaseModel
from db.database import Base 
from sqlalchemy import Column ,Integer , String 
class Users(BaseModel):
    name : str 
    city : str 
    gmail : str 
    password : str 


class UserTable(Base):

    __tablename__ = "User"

    id = Column(Integer , primary_key= True ,index= True)
    name = Column (String , nullable=False)
    city = Column (String ,nullable=False)
    email = Column (String , nullable=False,unique=True)
    password = Column (String, nullable=False)
