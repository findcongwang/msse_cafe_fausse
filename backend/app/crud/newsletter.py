from sqlalchemy.orm import Session
from app.models import Newsletter

def subscribe_to_newsletter(db: Session, email: str) -> Newsletter:
    subscriber = Newsletter(email=email)
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber

def unsubscribe_from_newsletter(db: Session, email: str) -> bool:
    subscriber = db.query(Newsletter)\
        .filter(Newsletter.email == email)\
        .first()
    if subscriber:
        subscriber.is_active = False
        db.commit()
        return True
    return False 

def is_email_subscribed(db: Session, email: str) -> bool:
    subscriber = db.query(Newsletter)\
        .filter(Newsletter.email == email)\
        .first()
    return subscriber is not None and subscriber.is_active