
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database.db import Base


# Request model for CREATE and PUT
class Employee(BaseModel):
    name: str
    department: str
    city: str
    mobile_num: str
    gmail: str
    age: int


# Request model for PATCH
class EmployeePatch(BaseModel):
    name: str | None = None
    department: str | None = None
    city: str | None = None
    mobile_num: str | None = None
    gmail: str | None = None
    age: int | None = None


# Database table
class EmployeesTable(Base):
    __tablename__ = "Employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = Column(String)
    city = Column(String)
    mobile_num = Column(String)
    gmail = Column(String)
    age = Column(Integer)
