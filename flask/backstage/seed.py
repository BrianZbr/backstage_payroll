import random
import string
import hashlib
import secrets
import datetime
from faker import Faker
from sqlalchemy import func
from backstage.src.models import Employee, UserAccount, Client, Contract, WorkRole, db
from backstage.src import create_app

EMPLOYEE_COUNT = 30
CLIENT_COUNT = 10
CONTRACT_COUNT = 20
WORKROLE_COUNT = 40


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )
    salt = secrets.token_hex(16)
    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def truncate_tables():
    """Delete all rows from database tables"""
    # db.session.execute(likes_table.delete())
    WorkRole.query.delete()
    Contract.query.delete()
    Client.query.delete()
    UserAccount.query.delete()
    Employee.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    db.session.commit()
    fake = Faker()

    # generate data for employee table
    for _ in range(EMPLOYEE_COUNT):
        first_name = fake.unique.first_name()
        last_name = fake.unique.last_name()
        ssn = fake.ssn().replace('-', '')
        last_employee = Employee(
            first_name=first_name,
            last_name=last_name,
            ssn=ssn
        )
        db.session.add(last_employee)
    db.session.commit()

    # generate data for user_account
    employees = Employee.query.all()
    for employee in employees:
        # assign user accounts to half the employees
        add_user = random.randint(0, 1)
        if add_user == 1:
            username = employee.first_name.lower() + str(random.randint(1, 150))
            last_user = UserAccount(
                username=username,
                email=f"{username}@{fake.domain_name()}",
                password=random_passhash(),
                employee_id=employee.employee_id,
            )
            db.session.add(last_user)

    # generate data for client table
    for _ in range(CLIENT_COUNT):
        company_name = fake.company()
        last_client = Client(
            company_name=company_name
        )
        db.session.add(last_client)
    db.session.commit()

    # generata data for contract table
    # TODO use actual client_ids instead of range? same below for contracts, employees
    max_cl_id = db.session.query(func.max(Client.client_id)).scalar()
    min_cl_id = db.session.query(func.min(Client.client_id)).scalar()
    for _ in range(CONTRACT_COUNT):
        client_id = random.randint(min_cl_id, max_cl_id)
        contract_description = fake.catch_phrase()
        start_date = fake.date_between(datetime.date(2019, 1, 1), '+1y')
        end_date = fake.date_between(start_date, '+1y')
        last_contract = Contract(
            client_id=client_id, contract_description=contract_description, start_date=start_date, end_date=end_date
        )
        # .strftime("%Y-%m-%d")
        db.session.add(last_contract)
    db.session.commit()

    # generate data for workrole table
    min_co_id = db.session.query(func.min(Contract.contract_id)).scalar()
    max_co_id = db.session.query(func.max(Contract.contract_id)).scalar()
    for _ in range(WORKROLE_COUNT):
        contract_id = random.randint(min_co_id, max_co_id)
        workrole_description = fake.job()
        hour_budget = random.randint(5, 90) * 10
        hourly_pay = random.randint(60, 200) / 4
        hourly_deduction = round(
            hourly_pay * random.choice([.5, .10, .15, .20]), 2)
        last_workrole = WorkRole(
            contract_id=contract_id, workrole_description=workrole_description, hour_budget=hour_budget, hourly_pay=hourly_pay, hourly_deduction=hourly_deduction
        )
        db.session.add(last_workrole)
    db.session.commit()


# run script
main()
