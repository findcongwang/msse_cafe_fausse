from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    newsletter_signup: bool = False

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    reservation_date: datetime
    guest_count: int

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    customer_id: int
    table_number: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class NewsletterSubscribe(BaseModel):
    email: EmailStr

class TableBase(BaseModel):
    table_number: int
    capacity: int

class Table(TableBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True 