from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    # db.Column(db.Integer, unique=True)
    user = db.relationship(
        "UserAccount", back_populates="employee", uselist=False)
    ssn = db.Column(db.String(9))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def __init__(self, ssn: str, first_name: str, last_name: str):
        self.ssn = ssn
        self.first_name = first_name
        self.last_name = last_name

    def serialize(self):
        return {
            'employee_id': self.employee_id,
            'created': self.created
        }


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


class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    company_name = db.Column(db.Text, unique=True)


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


class WorkRole(db.Model):
    __tablename__ = 'work_role'
    work_role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey(
        'contract.contract_id'), unique=True, nullable=False)
    hour_budget = db.Column(db.Numeric)
    hourly_pay = db.Column(db.Numeric)
    hourly_deduction = db.Column(db.Numeric)


employee_work_role_table = db.Table(
    'employee_work_role',
    db.Column(
        'employee_id', db.Integer,
        db.ForeignKey('employee.employee_id'),
        primary_key=True
    ),
    db.Column(
        'work_role_id', db.Integer,
        db.ForeignKey('work_role.work_role_id'),
        primary_key=True
    ),
    db.Column(
        'created', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


class TimeWorked(db.Model):
    __tablename__ = 'time_worked'
    time_worked_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employee.employee_id'), unique=True, nullable=False)
    work_role_id = db.Column(db.Integer, db.ForeignKey(
        'work_role.work_role_id'), nullable=False)
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
