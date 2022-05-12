"""Test file for user"""
import logging

from flask_login import current_user
from faker import Faker
from app import db
from app.db.models import User, Transaction



def test_adding_user(application):
    """This test adding a new user"""
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0
        # showing how to add a record
        # create a record
        user = User('test@gmail.com', 'test@123')
        # add it to get ready to be committed
        db.session.add(user)
        # call the commit
        db.session.commit()
        # assert that we now have a new user
        assert db.session.query(User).count() == 1
        # finding one user record by email
        user = User.query.filter_by(email='test@gmail.com').first()
        log.info(user)
        # asserting that the user retrieved is correct
        assert user.email == 'test@gmail.com'
        # this is how you get a related record ready for insert
        user.transactions = [Transaction("1", "2000", "CREDIT"), Transaction("2", "-1000", "DEBIT")]
        # commit is what saves the transactions
        db.session.commit()
        assert db.session.query(Transaction).count() == 2
        transaction1 = Transaction.query.filter_by(transaction_type='CREDIT').first()
        assert transaction1.transaction_type == "CREDIT"
        transaction1.transaction_type = "DEBIT"
        db.session.commit()
        transaction2 = Transaction.query.filter_by(transaction_type='DEBIT').first()
        assert transaction2.transaction_type == "DEBIT"
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0



def user_dashboard_access_approved(client):
    """Test for dashboard access"""
    response = client.get("/dashboard")
    assert response.status_code == 200
    return client.get('/dashboard', follow_redirects=True)


def user_dashboard_access_deny(client):
    """test for access deny"""
    response = client.get("/dashboard")
    assert response.status_code == 403
    return client.get('/dashboard', follow_redirects=False)


def test_upload_csvfile_access_denied(client):
    """test for csv upload"""
    response = client.get("/upload", follow_redirects=False)
    assert response.status_code == 404
