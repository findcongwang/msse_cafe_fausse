from sqlalchemy.orm import Session
from typing import Optional
from app.models.models import Customer

async def create_customer(db: Session, name: str, email: str, phone: Optional[str] = None, 
                        newsletter_signup: bool = False) -> Customer:
    customer = Customer(
        name=name,
        email=email,
        phone=phone,
        newsletter_signup=newsletter_signup
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer

async def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    return await db.query(Customer).filter(Customer.email == email).first() 