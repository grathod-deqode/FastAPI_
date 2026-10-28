from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    address: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    address: str