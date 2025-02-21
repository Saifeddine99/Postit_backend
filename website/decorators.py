import os
import time
from functools import wraps
import jwt
from flask import Blueprint, request, jsonify, g

# Rate Limiting (Max: 1 request per 3 second)
RATE_LIMIT = 3  # Seconds
last_request_time = 0

def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_request_time
        time_since_last_request = time.time() - last_request_time
        if time_since_last_request < RATE_LIMIT:
            time.sleep(RATE_LIMIT - time_since_last_request)  # Wait if needed
        result = func(*args, **kwargs)
        last_request_time = time.time()
        return result
    return wrapper



from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Decorator to protect routes that require authentication:
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        token = token.replace("Bearer ", "").strip()  # Remove "Bearer " and whitespace
        #print("Cleaned Token:", token)  # Debugging
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            g.user_id = int(data['sub'])  # Store user ID in g object
            
        except Exception as e:
            print("Decoding Error:", e) # Print the error
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    
    return decorated