import jwt
import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from .db_models import User, db
from werkzeug.security import generate_password_hash, check_password_hash #werkzeug is used for password hashing!

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


auth_bp = Blueprint('auth', __name__)  # Created a Blueprint for auth routes
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password_hash, data['password']):
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=24), # Token expiration time
            'iat': datetime.utcnow(),
            'sub': str(user.id)  # Subject (user ID)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401