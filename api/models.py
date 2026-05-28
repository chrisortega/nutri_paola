from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
