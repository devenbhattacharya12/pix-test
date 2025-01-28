import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

@app.route('/')
def home():
    return "Hello from Flask!"  # Just return a plain text response

# In-memory storage for demonstration
users = []
venues = []
photos = []
user_id_counter = 1
venue_id_counter = 1
photo_id_counter = 1

# Example route: Create a venue
@app.route('/venues', methods=['POST'])
def create_venue():
    global venue_id_counter
    data = request.json or {}
    if not data.get('name') or not data.get('streetAddress'):
        return jsonify({'error': 'Name and street address are required.'}), 400

    venue = {
        'id': venue_id_counter,
        'name': data['name'],
        'streetAddress': data['streetAddress']
    }
    venues.append(venue)
    venue_id_counter += 1
    return jsonify(venue), 201

# Example route: Get all venues
@app.route('/venues', methods=['GET'])
def get_venues():
    return jsonify(venues), 200

if __name__ == '__main__':
    # Render sets PORT as an environment variable. Default to 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
