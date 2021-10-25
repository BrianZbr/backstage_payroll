from flask import Blueprint, jsonify, request
from ..models import Client, db

bp = Blueprint('client', __name__, url_prefix='/client')


@bp.route('', methods=['GET'])
def show_clients():
    clients = Client.query.all()
    result = []
    for c in clients:
        result.append(c.serialize())
    return jsonify(result)


@bp.route('', methods=['POST', 'PUT'])
def create_client():
    if 'company_name' in request.json:
        company_name = request.json['company_name']
    c = Client(
        company_name=company_name
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(c.serialize())


@bp.route('/<int:client_id>', methods=['POST', 'PUT'])
def update_client(client_id: int):
    c = Client.query.get_or_404(client_id)
    if 'company_name' in request.json:
        c.company_name = request.json['company_name']
    try:
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
