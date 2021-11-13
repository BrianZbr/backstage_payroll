from backstage.src import create_app
from backstage.src.models import UserAccount
import pytest


@pytest.fixture
def testuser():
    test_user_account = UserAccount(
        username="TEST_USER_1_username",
        email="TEST@TESTUSER.COM",
        password="TEST_USER_pw1",
        employee_id=None
    )
    return test_user_account
