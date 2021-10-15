from flask import Blueprint, json, jsonify, abort, request
from ..models import UserAccount, db
import hashlib
import secrets


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def index():
    user_accounts = UserAccount.query.all()
    result = []
    for u in user_accounts:
        result.append(u.serialize())
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    u = UserAccount(
        email=request.json['email'],
        username=request.json['username'],
        password=scramble(request.json['password'])
    )
    db.session.add(u)
    db.session.commit()
    return jsonify(u.serialize())


@bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id: int):
    u = UserAccount.query.get_or_404(user_id)
    try:
        db.session.delete(u)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id: int):
    u = UserAccount.query.get_or_404(user_id)
    if 'email' in request.json.keys():
        u.email = request.json['email']
    if 'username' in request.json.keys():
        u.username = request.json['username']
    if 'password' in request.json.keys():
        u.password = scramble(request.json['password'])
    try:
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
