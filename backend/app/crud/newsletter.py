from sqlalchemy.orm import Session
from app.models import Newsletter

def subscribe_to_newsletter(db: Session, email: str) -> Newsletter:
    """
    Subscribe an email address to the newsletter.
    
    Args:
        db: SQLAlchemy database session
        email: Email address to subscribe
        
    Returns:
        Newsletter: The created newsletter subscription object
    """
    subscriber = Newsletter(email=email)
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber

def unsubscribe_from_newsletter(db: Session, email: str) -> bool:
    """
    Unsubscribe an email address from the newsletter by setting is_active to False.
    
    Args:
        db: SQLAlchemy database session
        email: Email address to unsubscribe
        
    Returns:
        bool: True if unsubscription was successful, False if email not found
    """
    subscriber = db.query(Newsletter)\
        .filter(Newsletter.email == email)\
        .first()
    if subscriber:
        subscriber.is_active = False
        db.commit()
        return True
    return False 

def is_email_subscribed(db: Session, email: str) -> bool:
    """
    Check if an email address is currently subscribed to the newsletter.
    
    Args:
        db: SQLAlchemy database session
        email: Email address to check
        
    Returns:
        bool: True if email is subscribed and active, False otherwise
    """
    subscriber = db.query(Newsletter)\
        .filter(Newsletter.email == email)\
        .first()
    return subscriber is not None and subscriber.is_active