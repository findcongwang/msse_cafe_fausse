from sqlalchemy.orm import Session
from typing import Optional
from app.models import Customer

async def create_customer(db: Session, name: str, email: str, phone: Optional[str] = None, 
                        newsletter_signup: bool = False) -> Customer:
    """
    Create a new customer in the database.
    
    Args:
        db: SQLAlchemy database session
        name: Customer's full name
        email: Customer's email address
        phone: Customer's phone number (optional)
        newsletter_signup: Whether customer opted into newsletter
        
    Returns:
        Customer: The newly created customer object
    """
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
    """
    Retrieve a customer by their email address.
    
    Args:
        db: SQLAlchemy database session
        email: Email address to search for
        
    Returns:
        Optional[Customer]: The customer object if found, None otherwise
    """
    return await db.query(Customer).filter(Customer.email == email).first() 