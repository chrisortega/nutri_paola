from pydantic import BaseModel, EmailStr
from typing import Optional

class PatientBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class PatientCreate(PatientBase):
    password: str

class PatientResponse(PatientBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    scopes: list[str] = []
