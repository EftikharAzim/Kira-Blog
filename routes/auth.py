from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTDecodeError
from schemas import RegisterSchema, LoginSchema

register_schema = RegisterSchema()
login_schema = LoginSchema()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    errors = register_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200

@auth_bp.before_request
def check_jwt():
    if request.endpoint == 'auth.login' or request.endpoint == 'auth.register':
        # Skip JWT validation for login and register endpoints
        return
    try:
        verify_jwt_in_request()
    except JWTDecodeError:
        return jsonify({"msg": "Invalid token"}), 401
