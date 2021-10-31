from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

employee_workrole_table = db.Table(
    'employee_workrole',
    db.Column(
        'employee_id', db.Integer,
        db.ForeignKey('employee.employee_id'),
        primary_key=True
    ),
    db.Column(
        'workrole_id', db.Integer,
        db.ForeignKey('workrole.workrole_id'),
        primary_key=True
    ),
    db.Column(
        'created', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


class UserAccount(db.Model):
    __tablename__ = 'user_account'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employee.employee_id'), unique=True)
    employee = db.relationship("Employee", back_populates="user")
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(320), unique=True)

    def __init__(self, email: str, username: str, password: str, employee_id: int):
        self.email = email
        self.username = username
        self.password = password
        self.employee_id = employee_id

    def serialize(self):
        return {
            'user_id': self.user_id,
            'created': self.created.isoformat(),
            'employee_id': self.employee_id,
            'email':  self.email,
            'username': self.username
        }


class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    user = db.relationship(
        "UserAccount", back_populates="employee", uselist=False)
    ssn = db.Column(db.String(9))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    assigned_workroles = db.relationship(
        "WorkRole", secondary=employee_workrole_table)

    def __init__(self, ssn: str, first_name: str, last_name: str):
        self.ssn = ssn
        self.first_name = first_name
        self.last_name = last_name

    def serialize(self):
        if self.assigned_workroles:
            workroles = []
            for workrole in self.assigned_workroles:
                workroles.append(workrole.workrole_id)
        else:
            workroles = None
        return {
            'employee_id': self.employee_id,
            'created': self.created,
            'workroles': workroles
        }


class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    company_name = db.Column(db.Text, unique=True)

    def serialize(self):
        return{
            'client_id': self.client_id,
            'created': self.created,
            'company_name': self.company_name
        }


class Contract(db.Model):
    __tablename__ = 'contract'
    contract_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey(
        'client.client_id'), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    contract_description = db.Column(db.Text)

    def serialize(self):
        return {
            'contract_id': self.contract_id,
            'created': self.created,
            'client_id': self.client_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'contract_description': self.contract_description
        }


class WorkRole(db.Model):
    __tablename__ = 'workrole'
    workrole_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey(
        'contract.contract_id'), nullable=False)
    workrole_description = db.Column(db.Text)
    hour_budget = db.Column(db.Numeric)
    hourly_pay = db.Column(db.Numeric)
    hourly_deduction = db.Column(db.Numeric)
    assigned_employees = db.relationship(
        "Employee", secondary=employee_workrole_table)

    def serialize(self):
        if self.hour_budget:
            self.hour_budget = float(self.hour_budget)
        if self.hourly_pay:
            self.hourly_pay = float(self.hourly_pay)
        if self.hourly_deduction:
            self.hourly_deduction = float(self.hourly_deduction)
        employees = []
        if self.assigned_employees:
            for employee in self.assigned_employees:
                employees.append(employee.employee_id)
        return{
            'workrole_id': self.workrole_id,
            'created': self.created,
            'contract_id': self.contract_id,
            'workrole_description': self.workrole_description,
            'hour_budget': self.hour_budget,
            'hourly_pay': self.hourly_pay,
            'hourly_deduction': self.hourly_deduction,
            'assigned_employees': employees
        }


class TimeWorked(db.Model):
    __tablename__ = 'time_worked'
    time_worked_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employee.employee_id'), nullable=False)
    workrole_id = db.Column(db.Integer, db.ForeignKey(
        'workrole.workrole_id'), nullable=False)
    check_id = db.Column(db.Integer)
    date_worked = db.Column(db.Date, nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    hours_worked = db.Column(db.Numeric)


class Paycheck(db.Model):
    __tablename__ = 'paycheck'
    paycheck_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    contract_description = db.Column(db.Text, nullable=False)
