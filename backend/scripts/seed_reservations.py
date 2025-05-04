#!/usr/bin/env python
import random
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

# Update imports to use the package name as defined in pyproject.toml
from app.db.session import get_db
from app.models import Customer
from app.crud.reservation import create_reservation

# Reservation date and time
RESERVATION_DATE = "2025-05-07"
RESERVATION_TIME = "7:00 PM"
RESERVATION_DATETIME = datetime.strptime(f"{RESERVATION_DATE} {RESERVATION_TIME}", "%Y-%m-%d %I:%M %p")

def seed_reservations():
    """Create 30 reservations for May 9th at 7 PM with staggered times"""
    try:
        with get_db() as db:
            # Create a single customer for all reservations
            customer = Customer(
                email="test@example.com",
                name="Test Customer",
                phone="555-123-4567"
            )
            
            print(f"Creating 30 new reservations...")
            
            for i in range(30):
                try:
                    # Use the create_reservation function from crud module
                    reservation = create_reservation(
                        db=db,
                        email=customer.email,
                        name=customer.name,
                        phone=customer.phone,
                        reservation_date=RESERVATION_DATETIME,
                        guest_count=random.randint(1, 8),
                    )
                except Exception as e:
                    print(f"Failed to create reservation #{i+1}: {str(e)}")
            
            db.commit()
            print(f"Successfully created reservations for {RESERVATION_DATE}")
            
    except SQLAlchemyError as e:
        print(f"Database error occurred: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    seed_reservations() 