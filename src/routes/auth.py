from flask import Blueprint, request, jsonify
from src.models import User, db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).all():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user: User= User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        print()
        print("error")
        print()
        return jsonify({'message': 'Invalid credentials'}), 400

    return jsonify({'message': 'login successful', 'uid': user.id, 'username': user.username}), 200
