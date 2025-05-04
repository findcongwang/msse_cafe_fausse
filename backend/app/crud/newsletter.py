from sqlalchemy.orm import Session
from app.models import Newsletter

async def subscribe_to_newsletter(db: Session, email: str) -> Newsletter:
    subscriber = Newsletter(email=email)
    db.add(subscriber)
    await db.commit()
    await db.refresh(subscriber)
    return subscriber

async def unsubscribe_from_newsletter(db: Session, email: str) -> bool:
    subscriber = await db.query(Newsletter)\
        .filter(Newsletter.email == email)\
        .first()
    if subscriber:
        subscriber.is_active = False
        await db.commit()
        return True
    return False 