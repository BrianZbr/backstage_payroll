from flask import Blueprint, jsonify, request, abort
from ..models import Employee, WorkRole, db

bp = Blueprint('employee_workrole', __name__, url_prefix='/employee_workrole')


@bp.route('', methods=['GET'])
def get_employee_workrole():
    return 'Nothing to see here'


@bp.route('', methods=['POST', 'PUT'])
def assign_employees_workroles():
    if not 'employee_ids' in request.json or not 'workrole_ids' in request.json:
        return abort(400, description="Request must include at least one value for employee_ids and for workrole_ids.")
    if not type(request.json['employee_ids']) == list or not type(request.json['workrole_ids']) == list:
        return abort(400, description="Both employee_ids and workrole_ids must be lists.")
    e_list = []
    w_list = []
    for employee in request.json['employee_ids']:
        e = Employee.query.get_or_404(employee)
        for workrole in request.json['workrole_ids']:
            last_workrole = WorkRole.query.get_or_404(workrole)
            w_list.append(last_workrole)
            e.assigned_workroles.append(last_workrole)
            e_list.append(e)
            db.session.add(e)
    db.session.commit()
    return jsonify(
        {
            'employees': [e.serialize() for e in set(e_list)],
            'workroles': [w.serialize() for w in set(w_list)]
        }
    )


@bp.route('', methods=['DELETE'])
def remove_employees_workroles():
    if not 'employee_ids' in request.json or not 'workrole_ids' in request.json:
        return abort(400, description="Request must include at least one value for employee_ids and for workrole_ids.")
    if not type(request.json['employee_ids']) == list or not type(request.json['workrole_ids']) == list:
        return abort(400, description="Both employee_ids and workrole_ids must be lists.")
    e_list = []
    w_list = []
    for employee in request.json['employee_ids']:
        e = Employee.query.get_or_404(employee)
        for workrole in request.json['workrole_ids']:
            last_workrole = WorkRole.query.get_or_404(workrole)
            w_list.append(last_workrole)
            e.assigned_workroles.remove(last_workrole)
            e_list.append(e)
            db.session.add(e)
    db.session.commit()
    return jsonify(
        {
            'employees': [e.serialize() for e in set(e_list)],
            'workroles': [w.serialize() for w in set(w_list)]
        }
    )
