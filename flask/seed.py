"""
Populate twitter database with fake data using the SQLAlchemy ORM.
"""

import random
import string
import hashlib
import secrets
from faker import Faker
from backstage.src.models import Employee, UserAccount, db
from backstage.src import create_app

EMPLOYEE_COUNT = 30


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
    UserAccount.query.delete()
    Employee.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()
    last_user = None
    last_employee = None
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
    employees = Employee.query.all()
    for employee in employees:
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
    db.session.commit()


# run script
main()
