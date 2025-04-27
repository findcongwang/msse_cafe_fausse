from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Optional
from flask import abort
from app.models import Reservation, Table

def create_reservation(db: Session, customer_id: int, reservation_date: datetime,
                      guest_count: int, duration_minutes: int) -> Reservation:
    # Validate reservation is within opening hours
    if not is_within_opening_hours(reservation_date, duration_minutes):
        abort(400, description="Reservation must be within opening hours")

    available_table = find_available_table(db, reservation_date, guest_count, duration_minutes)
    if not available_table:
        abort(400, description="No tables available for this time slot")
    
    reservation = Reservation(
        customer_id=customer_id,
        reservation_date=reservation_date,
        table_number=available_table.table_number,
        duration_minutes=duration_minutes,
        guest_count=guest_count
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def is_within_opening_hours(reservation_date: datetime, duration_minutes: int) -> bool:
    # Get reservation end time
    end_time = reservation_date + timedelta(minutes=duration_minutes)
    
    # Convert to local time for hour checking (assuming reservation_date is in UTC)
    weekday = reservation_date.weekday()  # Monday is 0, Sunday is 6
    hour = reservation_date.hour
    end_hour = end_time.hour
    
    # Define opening hours (17:00/5PM) and closing hours
    opening_hour = 17
    closing_hour = 23 if weekday < 6 else 21  # 11PM Mon-Sat, 9PM Sunday
    
    # Check if reservation starts and ends within opening hours
    if hour < opening_hour or hour >= closing_hour:
        return False
    if end_hour > closing_hour:
        return False
        
    return True

def find_available_table(db: Session, reservation_date: datetime, 
                        guest_count: int, duration_minutes: int) -> Optional[Table]:
    # Get reservation end time
    end_time = reservation_date + timedelta(minutes=duration_minutes)

    # Get all active tables that can accommodate the party size
    suitable_tables = db.query(Table)\
        .filter(Table.is_active == True)\
        .filter(Table.capacity >= guest_count)\
        .order_by(Table.capacity)\
        .all()

    if not suitable_tables:
        return None

    # Check each table's availability
    for table in suitable_tables:
        # Look for conflicting reservations
        conflicts = db.query(Reservation)\
            .filter(Reservation.table_number == table.table_number)\
            .filter(Reservation.status == "confirmed")\
            .filter(
                # New reservation starts during existing reservation
                ((Reservation.reservation_date <= reservation_date) &
                 (Reservation.reservation_date + timedelta(minutes=Reservation.duration_minutes) >= reservation_date)) |
                # New reservation ends during existing reservation
                ((Reservation.reservation_date <= end_time) &
                 (Reservation.reservation_date + timedelta(minutes=Reservation.duration_minutes) >= end_time)) |
                # New reservation completely encompasses existing reservation
                ((reservation_date <= Reservation.reservation_date) &
                 (end_time >= Reservation.reservation_date + timedelta(minutes=Reservation.duration_minutes)))
            ).first()
        
        if not conflicts:
            return table

    return None
