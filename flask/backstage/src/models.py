from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, unique=True)
    ssn = db.Column(db.String(9))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


class UserAccount(db.Model):
    __tablename__ = 'user_account'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employee.employee_id'), unique=True)
    email = db.Column(db.String(320), unique=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, email: str, username: str, password: str):
        self.email = email
        self.username = username

    def serialize(self):
        return {
            'user_id': self.user_id,
            'created': self.created.isoformat(),
            'employee_id': self.employee_id,
            'email':  self.email,
            'username': self.username,
            'password': self.password
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
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    contract_description = db.Column(db.Text)
