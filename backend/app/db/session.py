from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from contextlib import contextmanager

# Create sync engine for Flask
engine = create_engine(
    # If your connection string is currently using asyncpg, convert it to standard postgresql
    settings.SQLALCHEMY_DATABASE_URI.replace("postgresql+asyncpg://", "postgresql://"),
    echo=settings.DB_ECHO,
    future=True,
    pool_pre_ping=True,
)

# Create sync session factory
SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@contextmanager
def get_db():
    """Provides a synchronous database session as a context manager."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close() 