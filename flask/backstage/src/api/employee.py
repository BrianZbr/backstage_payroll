from flask import Blueprint, jsonify, abort
from flask.globals import request
from ..models import Employee, db

bp = Blueprint('employee', __name__, url_prefix='/employee')


@bp.route('', methods=['GET'])
def show_employees():
    employees = Employee.query.all()
    result = []
    for e in employees:
        result.append(e.serialize())
    return jsonify(result)


@bp.route('', methods=['POST', 'PUT'])
def create_employee():
    if 'ssn' in request.json:
        ssn = request.json['ssn']
    else:
        ssn = None
    if len(ssn) != 9:
        return abort(400, description="SSN must be 9 characters long. Do not include dashes.")
    if 'first_name' in request.json:
        first_name = request.json['first_name']
    else:
        first_name = None
    if 'last_name' in request.json:
        last_name = request.json['last_name']
    else:
        last_name = None
    if 'user_id' in request.json:
        user_id = request.json['user_id']
    else:
        user_id = None
    e = Employee(
        ssn=ssn,
        first_name=first_name,
        last_name=last_name
    )
    db.session.add(e)
    db.session.commit()
    return jsonify(e.serialize())


@bp.route('/<int:user_id>', methods=['POST', 'PUT'])
def update(user_id: int):
    e = Employee.query.get_or_404(user_id)
    if 'ssn' in request.json:
        e.ssn = request.json['ssn']
    if 'first_name' in request.json:
        e.first_name = request.json['first_name']
    if 'last_name' in request.json:
        e.last_name = request.json['last_name']
    if 'user_id' in request.json:
        e.user_id = request.json[user_id]
    try:
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
