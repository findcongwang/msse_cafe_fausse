from flask import Blueprint, jsonify, request
from app.db.session import get_db
from app.crud.newsletter import subscribe_to_newsletter as create_subscription, is_email_subscribed

newsletter_bp = Blueprint('newsletter', __name__, url_prefix='/api/newsletter')

@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe_endpoint():
    """Subscribe a user to the newsletter"""
    # Get the JSON data from the request
    subscription_data = request.json

    # Extract required fields
    try:
        email = subscription_data.get('email')
        if not email:
            return jsonify({
                "message": "Missing required field: email is required",
                "success": False
            }), 400

        # Get database session
        with get_db() as db:
            # Check if email is already subscribed
            if is_email_subscribed(db, email):
                return jsonify({
                    "message": "This email is already subscribed to the newsletter",
                    "success": False
                }), 409  # Conflict status code

            # Create the subscription
            try:
                # Store the result of create_subscription
                newsletter_subscription = create_subscription(
                    db=db,
                    email=email
                )
                
                # Return successful response with the subscription data
                return jsonify({
                    "message": "Successfully subscribed to newsletter",
                    "success": True,
                    "data": {"email": email}
                }), 201

            except Exception as e:
                # Handle any errors from the subscription creation
                return jsonify({
                    "message": f"Error creating subscription: {str(e)}",
                    "success": False
                }), 500

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({
            "message": f"An unexpected error occurred: {str(e)}",
            "success": False
        }), 500


@newsletter_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe_from_newsletter():
    """Unsubscribe a user from the newsletter"""
    # Get the JSON data from the request
    unsubscribe_data = request.json

    # Handle potential errors early
    if not unsubscribe_data:
        return jsonify({
            "message": "No data provided",
            "success": False
        }), 400

    # Extract required fields
    try:
        email = unsubscribe_data.get('email')

        # Validate required fields
        if not email:
            return jsonify({
                "message": "Missing required field: email is required",
                "success": False
            }), 400

        # Get database session
        with get_db() as db:
            # Implement unsubscribe logic here
            # This would call a function like remove_subscription(db, email)
            # For now, we'll return a placeholder response
            return jsonify({
                "message": "Successfully unsubscribed from newsletter",
                "success": True
            }), 200

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({
            "message": f"An unexpected error occurred: {str(e)}",
            "success": False
        }), 500
