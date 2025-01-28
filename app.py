import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes and origins

# In-memory storage
users = []
venues = []
photos = []
user_id_counter = 1
venue_id_counter = 1
photo_id_counter = 1

# Serve index.html from the 'static' folder
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Create a user
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required.'}), 400

    user = {
        'id': user_id_counter,
        'username': data['username'],
        'password': data['password']
    }
    users.append(user)
    user_id_counter += 1
    return jsonify(user), 201

# Create a venue
@app.route('/venues', methods=['POST'])
def create_venue():
    global venue_id_counter
    data = request.json
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

# Get all venues
@app.route('/venues', methods=['GET'])
def get_venues():
    return jsonify(venues), 200

# Get a specific venue
@app.route('/venues/<int:id>', methods=['GET'])
def get_venue(id):
    venue = next((v for v in venues if v['id'] == id), None)
    if not venue:
        return jsonify({'error': 'Venue not found.'}), 404
    return jsonify(venue), 200

# Upload a photo
@app.route('/photos', methods=['POST'])
def upload_photo():
    global photo_id_counter
    data = request.json
    if not data.get('venueId') or not data.get('ownerId') or not data.get('url'):
        return jsonify({'error': 'Venue ID, owner ID, and URL are required.'}), 400

    photo = {
        'id': photo_id_counter,
        'venueId': data['venueId'],
        'ownerId': data['ownerId'],
        'url': data['url']
    }
    photos.append(photo)
    photo_id_counter += 1
    return jsonify(photo), 201

# Get all photos of a venue
@app.route('/venues/<int:id>/photos', methods=['GET'])
def get_photos_of_venue(id):
    venue_photos = [p for p in photos if p['venueId'] == id]
    if not venue_photos:
        return jsonify({'error': 'No photos found for this venue.'}), 404
    return jsonify(venue_photos), 200

# Get a specific photo
@app.route('/photos/<int:id>', methods=['GET'])
def get_photo(id):
    photo = next((p for p in photos if p['id'] == id), None)
    if not photo:
        return jsonify({'error': 'Photo not found.'}), 404
    return jsonify(photo), 200

if __name__ == '__main__':
    # Render sets PORT as an environment variable. Default to 5000 if not set.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
