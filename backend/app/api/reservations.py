from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from crud.reservation import create_reservation
from app.db.session import get_db


reservations_bp = Blueprint('reservations', __name__, url_prefix='/api/reservations')

@reservations_bp.route('', methods=['POST'])
def create_reservation_endpoint():
    """Create a new reservation with proper table availability checking"""
    # Get the JSON data from the request
    reservation_data = request.json

    # Extract required fields from the reservation data
    try:
        # Extract fields from the frontend payload
        email = reservation_data.get('email')
        date_str = reservation_data.get('date')
        time_str = reservation_data.get('time')
        guest_count = reservation_data.get('guests')
        
        # Get customer information
        name = reservation_data.get('name', '')
        phone = reservation_data.get('phone', '')
        
        # Validate required fields
        if not all([email, date_str, time_str, guest_count, name]):
            return jsonify({
                "message": "Missing required fields: email, date, time, guests, and name are required",
                "success": False
            }), 400
            
        try:
            # Combine date and time strings into a datetime object
            reservation_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
        except ValueError:
            return jsonify({
                "message": "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time",
                "success": False
            }), 400
            
        # Validate guest count
        try:
            guest_count = int(guest_count)
            if guest_count <= 0:
                raise ValueError("Guest count must be positive")
        except (ValueError, TypeError):
            return jsonify({
                "message": "Invalid guest count. Must be a positive number",
                "success": False
            }), 400
            
        # Get database session - use the session yielded by the context manager
        with get_db() as db:                
            # Create the reservation with the available table
            try:
                response = create_reservation(
                    db=db,
                    email=email,
                    name=name,
                    phone=phone,
                    reservation_date=reservation_datetime,
                    guest_count=guest_count,
                )

                # Check response status and return appropriate error code
                if not response.get("success"):
                    return jsonify(response), 400

                # Return successful response
                return jsonify(response), 201
                
            except Exception as e:
                # Handle any errors from the reservation creation
                return jsonify({
                    "message": f"Error creating reservation: {str(e)}",
                    "success": False
                }), 500
            
    except Exception as e:
        # Catch any unexpected errors
        return jsonify({
            "message": f"An unexpected error occurred: {str(e)}",
            "success": False
        }), 500

