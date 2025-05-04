import random
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Optional
from flask import abort
from app.models import Reservation, Customer
from sqlalchemy.exc import SQLAlchemyError


TABLE_COUNT = 30

def create_reservation(
    db: Session, 
    email: str,
    reservation_date: datetime,
    guest_count: int,
    name: str = None,
    phone: str = None,
) -> dict:
    """
    Create a reservation with automatic customer lookup/creation.
    
    Args:
        db: Database session
        email: Customer email
        reservation_date: Start time of the reservation
        guest_count: Number of guests
        name: Customer name (required for new customers)
        phone: Customer phone number (optional)
        
    Returns:
        Dictionary with reservation details and success status
    """
    try:
        # Validate reservation is within opening hours
        if not is_within_opening_hours(reservation_date):
            return {
                "message": "Reservation must be within opening hours",
                "success": False
            }

        # Look up existing customer
        customer = db.query(Customer).filter(Customer.email == email).first()
        
        # If customer doesn't exist, create a new one
        if not customer:
            if not name:
                return {
                    "message": "Name is required for new customers",
                    "success": False
                }
            
            customer = Customer(
                email=email,
                name=name,
                phone=phone
            )
            db.add(customer)
            db.flush()  # Get the ID without committing yet
        
        # Check if customer already has a reservation at this time
        existing_reservation = db.query(Reservation)\
            .filter(Reservation.customer_id == customer.id)\
            .filter(Reservation.status.in_(["confirmed", "seated"]))\
            .filter(Reservation.reservation_date == reservation_date)\
            .first()
            
        if existing_reservation:
            # Customer already has a reservation at this time
            if existing_reservation.guest_count != guest_count:
                # Update the guest count if it's different
                existing_reservation.guest_count = guest_count
                db.flush()
                return {
                    "message": "You already have a reservation at this time. We've updated your guest count.",
                    "success": True,
                    "data": {
                        "email": customer.email,
                        "name": customer.name,
                        "phone": customer.phone,
                        "table_number": existing_reservation.table_number,
                        "date": existing_reservation.reservation_date.strftime("%Y-%m-%d"),
                        "time": existing_reservation.reservation_date.strftime("%H:%M"),
                        "guest_count": guest_count,
                    }
                }
            else:
                return {
                    "message": "You already have a reservation at this time.",
                    "success": False,
                    "data": {
                        "email": customer.email,
                        "name": customer.name,
                        "table_number": existing_reservation.table_number,
                        "date": existing_reservation.reservation_date.strftime("%Y-%m-%d"),
                        "time": existing_reservation.reservation_date.strftime("%H:%M"),
                        "guest_count": existing_reservation.guest_count,
                    }
                }

        # Check if a table is available
        available_table = find_available_table(
            db, 
            reservation_date, 
            guest_count
        )
        
        if not available_table:
            return {
                "message": "Sorry, no tables are available for this time slot",
                "success": False,
            }
            
        # Create the reservation with the available table
        new_reservation = Reservation(
            customer_id=customer.id,
            table_number=available_table,
            reservation_date=reservation_date,
            guest_count=guest_count,
            status="confirmed"
        )
        
        db.add(new_reservation)
        db.flush()  # To get the ID and other generated values
        
        # Return the reservation confirmation
        return {
            "message": "Reservation confirmed",
            "success": True,
            "data": {
                "email": customer.email,
                "name": customer.name,
                "phone": customer.phone,
                "table_number": new_reservation.table_number,
                "date": reservation_date.strftime("%Y-%m-%d"),
                "time": reservation_date.strftime("%H:%M"),
                "guest_count": guest_count,
            }
        }
        
    except SQLAlchemyError as e:
        return {
            "message": f"Database error: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "message": f"Error creating reservation: {str(e)}",
            "success": False
        }

def is_within_opening_hours(reservation_date: datetime) -> bool:
    # Convert to local time for hour checking (assuming reservation_date is in UTC)
    weekday = reservation_date.weekday()  # Monday is 0, Sunday is 6
    hour = reservation_date.hour
    
    # Define opening hours (17:00/5PM) and closing hours
    opening_hour = 17
    closing_hour = 23 if weekday < 6 else 21  # 11PM Mon-Sat, 9PM Sunday
    
    # Check if reservation is within opening hours
    if hour < opening_hour or hour >= closing_hour:
        return False
        
    return True

def find_available_table(db: Session, reservation_date: datetime, 
                        guest_count: int) -> Optional[int]:
    """
    Find an available table for the given reservation parameters.
    Tables are considered unavailable if there's a reservation at the exact same time.
    All tables can accommodate any party size.
    
    Args:
        db: Database session
        reservation_date: Start time of the requested reservation
        guest_count: Number of guests
        
    Returns:
        An available table number (random) or None if no tables are available
    """
    # Get all tables that are already reserved for this time
    reserved_tables = db.query(Reservation.table_number)\
        .filter(
            and_(
                Reservation.reservation_date == reservation_date,
                Reservation.status == "confirmed"
            )
        ).all()
    
    # Convert to a set of table numbers
    reserved_table_numbers = {table[0] for table in reserved_tables}
    
    # Find available tables (all tables from 1 to TABLE_COUNT that aren't reserved)
    available_tables = [i for i in range(1, TABLE_COUNT + 1) 
                       if i not in reserved_table_numbers]
    
    # If no tables are available, return None
    if not available_tables:
        return None
        
    # Return the first available table
    return random.choice(available_tables)
