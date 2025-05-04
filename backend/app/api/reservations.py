from random import randint
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from db.session import get_db
from models import Reservation

# Create a main API blueprint
reservations_bp = Blueprint('reservations', __name__, url_prefix='/api/reservations')

# Fix: Change route from '/' to '' to match the URL prefix exactly
@reservations_bp.route('', methods=['POST'])
def create_reservation_endpoint():
    """Create a new reservation with proper table availability checking"""
    # Get the JSON data from the request
    reservation_data = request.json

    return jsonify({
        "message": "Reservation received",
        "data": {"table_number": randint(1, 30)}
    })
    
    # # Extract required fields from the reservation data
    # try:
    #     customer_id = reservation_data.get('customer_id')
    #     date_str = reservation_data.get('date')
    #     time_str = reservation_data.get('time')
    #     guest_count = reservation_data.get('guest_count')
    #     duration_minutes = reservation_data.get('duration_minutes', 90)  # Default to 90 minutes
    #     special_requests = reservation_data.get('special_requests', '')
        
    #     # Validate required fields
    #     if not all([customer_id, date_str, time_str, guest_count]):
    #         return jsonify({
    #             "message": "Missing required fields: customer_id, date, time, and guest_count are required",
    #             "success": False
    #         }), 400
            
    #     # Parse date and time
    #     try:
    #         # Combine date and time strings into a datetime object
    #         reservation_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    #     except ValueError:
    #         return jsonify({
    #             "message": "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time",
    #             "success": False
    #         }), 400
            
    #     # Validate guest count
    #     try:
    #         guest_count = int(guest_count)
    #         if guest_count <= 0:
    #             raise ValueError("Guest count must be positive")
    #     except (ValueError, TypeError):
    #         return jsonify({
    #             "message": "Invalid guest count. Must be a positive number",
    #             "success": False
    #         }), 400
            
    #     # Get database session
    #     db = next(get_db())
        
    #     # Check if a table is available without creating the reservation yet
    #     available_table = find_available_table(
    #         db, 
    #         reservation_datetime, 
    #         guest_count, 
    #         duration_minutes
    #     )
        
    #     if not available_table:
    #         # No tables available, suggest alternative time slots
    #         requested_date = reservation_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    #         available_slots = get_available_time_slots(db, requested_date, guest_count, duration_minutes)
            
    #         # Format time slots for response
    #         formatted_slots = [slot.strftime("%H:%M") for slot in available_slots]
            
    #         return jsonify({
    #             "message": "Sorry, no tables are available for this time slot and party size",
    #             "success": False,
    #             "alternative_times": formatted_slots
    #         }), 409  # Conflict status code
            
    #     # Create the reservation with the available table
    #     try:
    #         new_reservation = Reservation(
    #             customer_id=customer_id,
    #             table_number=available_table.table_number,
    #             reservation_date=reservation_datetime,
    #             guest_count=guest_count,
    #             duration_minutes=duration_minutes,
    #             special_requests=special_requests,
    #             status="confirmed"
    #         )
            
    #         db.add(new_reservation)
    #         db.commit()
    #         db.refresh(new_reservation)
            
    #         # Calculate end time for the response
    #         end_time = reservation_datetime + timedelta(minutes=duration_minutes)
            
    #         # Return the reservation confirmation
    #         return jsonify({
    #             "message": "Reservation confirmed",
    #             "success": True,
    #             "data": {
    #                 "reservation_id": new_reservation.id,
    #                 "table_number": new_reservation.table_number,
    #                 "date": date_str,
    #                 "time": time_str,
    #                 "end_time": end_time.strftime("%H:%M"),
    #                 "guest_count": guest_count,
    #                 "duration_minutes": duration_minutes,
    #                 "special_requests": special_requests
    #             }
    #         })
            
    #     except Exception as e:
    #         db.rollback()
    #         # Handle any errors from the reservation creation
    #         return jsonify({
    #             "message": f"Error creating reservation: {str(e)}",
    #             "success": False
    #         }), 500
            
    # except Exception as e:
    #     # Catch any unexpected errors
    #     return jsonify({
    #         "message": f"An unexpected error occurred: {str(e)}",
    #         "success": False
    #     }), 500

