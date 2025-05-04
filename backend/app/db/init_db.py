from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.core.config import settings

async def init_db(db: AsyncSession) -> None:
    """Initialize database with default data."""
    try:
        # Create default admin user
        admin_user = UserCreate(
            email=settings.FIRST_ADMIN_EMAIL,
            password=settings.FIRST_ADMIN_PASSWORD,
            full_name="Admin User",
            is_admin=True
        )
        await create_user(db, admin_user)
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise 