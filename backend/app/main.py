from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

# API routes with /api prefix
@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from API!"})

# Register custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    # Return the 404.html page from your static folder
    return send_from_directory(app.static_folder, '404.html'), 404

# Serve static files for all other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)