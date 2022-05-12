"""Test the balance"""
from app import db
from app.db.models import User, Transactions


def test_balance_none(application, client):
    """Test if a user logs in that it displays balance"""
    with application.app_context():
        # Add user to be able to test login
        user = User('test@gmail.com', 'test@123')
        db.session.add(user)
        db.session.commit()

        assert user.balance is None
        db.session.delete(user)


def test_balance_calculations(application, client):
    """Test the balance calculations of the app"""
    testdata = [2000, 2000, -100, 200, 200, 200, -1000, 200, 1000,
                -100, 100, 1000, 1000, -100, 1000, 100
                - 100, 100, 100, 100, -100, 100, 4242, -2324, 4242,
                432, 432, -4323]
    balance = 0
    for data in testdata:
        balance += data

    assert balance == 10601
