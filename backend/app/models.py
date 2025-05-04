from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

print("Loading models.py module - ID:", id(Base))

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String)
    newsletter_signup = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    reservations = relationship("Reservation", back_populates="customer")

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    reservation_date = Column(DateTime, nullable=False)
    table_number = Column(Integer, nullable=False)
    guest_count = Column(Integer, nullable=False)
    status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    customer = relationship("Customer", back_populates="reservations")
    
    # Add uniqueness constraint to prevent double booking
    __table_args__ = (
        UniqueConstraint('table_number', 'reservation_date', name='uix_reservation_table_date'),
    )

class Newsletter(Base):
    __tablename__ = "newsletter"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True) 