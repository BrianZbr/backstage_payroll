from flask import Blueprint, jsonify, request, abort
from ..models import WorkRole, db

bp = Blueprint('workrole', __name__, url_prefix='/workrole')


@bp.route('', methods=['GET'])
def show_workroles():
    workroles = WorkRole.query.all()
    result = []
    for w in workroles:
        result.append(w.serialize())
    return jsonify(result)


@bp.route('', methods=['POST', 'PUT'])
def create_workroles():
    if not 'contract_id' in request.json:
        return abort(400, description="contract_id is required")
    else:
        contract_id = request.json['contract_id']
    if 'workrole_description' in request.json:
        workrole_description = request.json['workrole_description']
    else:
        workrole_description = None
    if 'hour_budget' in request.json:
        hour_budget = request.json['hour_budget']
    else:
        hour_budget = None
    if 'hourly_pay' in request.json:
        hourly_pay = request.json['hourly_pay']
    else:
        hourly_pay = None
    if 'hourly_deduction' in request.json:
        hourly_deduction = request.json['hourly_deduction']
    else:
        hourly_deduction = None
    w = WorkRole(
        contract_id=contract_id, workrole_description=workrole_description, hour_budget=hour_budget, hourly_pay=hourly_pay, hourly_deduction=hourly_deduction
    )
    db.session.add(w)
    db.session.commit()
    return jsonify(w.serialize())


@bp.route('/<int:work_role_id>', methods=['POST', 'PUT'])
def update_workrole(work_role_id: int):
    w = WorkRole.query.get_or_404(work_role_id)
    if 'hour_budget' in request.json:
        w.hour_budget = request.json['hour_budget']
    if 'hourly_pay' in request.json:
        w.hourly_pay = request.json['hourly_pay']
    if 'hourly_deduction' in request.json:
        w.hourly_deduction = request.json['hourly_deduction']
    try:
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
