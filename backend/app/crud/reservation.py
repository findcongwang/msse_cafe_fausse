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
                        guest_count: int, duration_minutes: int = 90) -> Optional[Table]:
    """
    Find an available table for the given reservation parameters.
    Tables are considered unavailable if there's an overlapping reservation.
    
    Args:
        db: Database session
        reservation_date: Start time of the requested reservation
        guest_count: Number of guests
        duration_minutes: Duration of the reservation (default: 90 minutes)
        
    Returns:
        An available table or None if no tables are available
    """
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
            .filter(Reservation.status.in_(["confirmed", "seated"]))\
            .filter(
                # Check for any overlap between the requested time slot and existing reservations
                and_(
                    # Start of existing reservation is before end of requested reservation
                    Reservation.reservation_date < end_time,
                    # End of existing reservation is after start of requested reservation
                    Reservation.reservation_date + timedelta(minutes=90) > reservation_date
                )
            ).first()
        
        if not conflicts:
            return table

    return None

def get_available_time_slots(db: Session, requested_date: datetime, guest_count: int, 
                            duration_minutes: int = 90) -> List[datetime]:
    """
    Find available time slots for a given date and party size.
    
    Args:
        db: Database session
        requested_date: The date to check (datetime with time set to 00:00:00)
        guest_count: Number of guests
        duration_minutes: Duration of the reservation (default: 90 minutes)
        
    Returns:
        List of available time slots (datetime objects)
    """
    # Define restaurant hours
    weekday = requested_date.weekday()
    opening_hour = 17  # 5 PM
    closing_hour = 23 if weekday < 6 else 21  # 11 PM Mon-Sat, 9 PM Sunday
    
    # Generate potential time slots every 30 minutes
    time_slots = []
    current_time = requested_date.replace(hour=opening_hour, minute=0, second=0, microsecond=0)
    end_time = requested_date.replace(hour=closing_hour, minute=0, second=0, microsecond=0)
    
    # Last reservation should be at least duration_minutes before closing
    last_reservation_time = end_time - timedelta(minutes=duration_minutes)
    
    while current_time <= last_reservation_time:
        time_slots.append(current_time)
        current_time += timedelta(minutes=30)
    
    # Get all active tables that can accommodate the party size
    suitable_tables = db.query(Table)\
        .filter(Table.is_active == True)\
        .filter(Table.capacity >= guest_count)\
        .all()
    
    if not suitable_tables:
        return []
    
    # For each time slot, check if at least one table is available
    available_slots = []
    for slot in time_slots:
        for table in suitable_tables:
            # Check if this table is available at this time slot
            conflicts = db.query(Reservation)\
                .filter(Reservation.table_number == table.table_number)\
                .filter(Reservation.status.in_(["confirmed", "seated"]))\
                .filter(
                    and_(
                        # Start of existing reservation is before end of requested reservation
                        Reservation.reservation_date < slot + timedelta(minutes=duration_minutes),
                        # End of existing reservation is after start of requested reservation
                        Reservation.reservation_date + timedelta(minutes=90) > slot
                    )
                ).first()
            
            if not conflicts:
                available_slots.append(slot)
                break  # Found an available table for this slot, move to next slot
    
    return available_slots
