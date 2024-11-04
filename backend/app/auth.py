from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import os
from dotenv import load_dotenv
from backend.app.db.models import User  

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

def generate_token(user_id):
    token = jwt.encode(
        {
            'user_id': str(user_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return token

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.get_user_by_email(email):
        return jsonify({"message": "Email already exists."}), 409

    hashed_password = generate_password_hash(password)
    user_data = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.datetime.utcnow()
    }
    user_id = User.create_user(user_data).inserted_id

    return jsonify({"message": "User registered successfully.", "user_id": str(user_id)}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.get_user_by_email(email)
    if not user or not check_password_hash(user['hashed_password'], password):
        return jsonify({"message": "Invalid email or password."}), 401

    token = generate_token(user['_id'])
    return jsonify({"message": "Login successful.", "token": token}), 200

@app.route('/protected', methods=['GET'])
@auth_required
def protected():
    return jsonify({"message": "Access granted to protected route.", "user_id": request.user_id}), 200
