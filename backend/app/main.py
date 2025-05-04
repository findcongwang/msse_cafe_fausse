from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from api.reservations import reservations_bp
from api.newsletter import newsletter_bp
app = Flask(__name__, static_folder='static', static_url_path='/')

# Register the API controllers
app.register_blueprint(reservations_bp)
app.register_blueprint(newsletter_bp)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    # Return the 404.html page from your static folder
    return send_from_directory(app.static_folder, '404.html'), 404

# Serve static files for all other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    # Don't handle API routes here to avoid redirection
    if path.startswith('api/'):
        return jsonify({"error": "API endpoint not found"}), 404
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)