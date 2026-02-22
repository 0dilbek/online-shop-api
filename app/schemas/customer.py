# app/schemas/customer.py
from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    full_name: str
    phone: str
    default_address: Optional[str] = None


class CustomerCreate(CustomerBase):
    password: str


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    default_address: Optional[str] = None
    password: Optional[str] = None


class CustomerLogin(BaseModel):
    phone: str
    password: str


class CustomerOut(CustomerBase):
    id: int

    class Config:
        from_attributes = True
