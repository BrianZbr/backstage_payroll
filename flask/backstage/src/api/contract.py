from flask import Blueprint, jsonify, request
from ..models import Contract, db

bp = Blueprint('contract', __name__, url_prefix='/contract')


@bp.route('', methods=['GET'])
def show_contracts():
    contracts = Contract.query.all()
    result = []
    for c in contracts:
        result.append(c.serialize())
    return jsonify(result)


@bp.route('', methods=['POST', 'PUT'])
def create_contract():
    if not 'client_id' in request.json:
        return abort(400, description="client_id is required")
    else:
        client_id = request.json['client_id']
    if 'start_date' in request.json:
        start_date = request.json['start_date']
    else:
        start_date = None
    if 'end_date' in request.json:
        end_date = request.json['end_date']
    else:
        end_date = None
    if 'contract_description' in request.json:
        contract_description = request.json['contract_description']
    else:
        contract_description = None

    c = Contract(
        client_id=client_id, start_date=start_date, end_date=end_date, contract_description=contract_description
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(c.serialize())
