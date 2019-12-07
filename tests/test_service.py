"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
from flask_api import status    # HTTP Status Codes
from unittest.mock import MagicMock, patch
from service.models import account, DataValidationError, db
from .account_factory import AccountFactory
from service.service import app, init_db, initialize_logging


DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost:3306/test')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountServer(unittest.TestCase):
    """ Account Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.debug = False
        initialize_logging(logging.INFO)
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()



    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def _create_accounts(self, count):
        """ Factory method to create accounts in bulk """
        accounts = []
        for _ in range(count):
            test_account = AccountFactory()
            resp = self.app.post('/accounts',
                                 json=test_account.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create a test account')
            new_account = resp.get_json()
            test_account.id = new_account['id']
            accounts.append(test_account)
        return accounts

    def test_root_url(self):
        """ Test / route """
        resp = self.app.get('/',
                            content_type='application/json')
        print(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_account_list(self):
        """ Get a list of accounts """
        self._create_accounts(5)
        resp = self.app.get('/accounts')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_account(self):
        """ Get a single account """
        test_account = self._create_accounts(1)[0]
        resp = self.app.get('/accounts/{}'.format(test_account.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['owner'], test_account.owner)

    def test_get_account_by_account_id(self):
        """ Get an account linked to account id"""
        test_account = self._create_accounts(1)[0]
        resp = self.app.get('/accounts/account_id/{}'.format(test_account.account_id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()[0]
        self.assertEqual(data['owner'], test_account.owner)

    def test_get_account_not_found(self):
        """ Get an account thats not found """
        resp = self.app.get('/accounts/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account(self):
        """ Update an existing account """
        # create a account to update
        test_account = AccountFactory()
        resp = self.app.post('/accounts',
                             json=test_account.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the account
        new_account = resp.get_json()
        new_account['account_id'] = 2
        resp = self.app.put('/accounts/{}'.format(new_account['id']),
                            json=new_account,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_account = resp.get_json()
        self.assertEqual(updated_account['account_id'], 2)

    def test_update_account_failure(self):
        """ Update an existing account (failure) """
        # create a account to update
        test_account = AccountFactory()
        resp = self.app.post('/accounts',
                             json=test_account.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the account
        new_account = resp.get_json()
        new_account['account_id'] = 2
        resp = self.app.put('/accounts/{}'.format(5),
                            json=new_account,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        """ Delete a account """
        test_account = self._create_accounts(1)[0]
        resp = self.app.delete('/accounts/{}'.format(test_account.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/accounts/{}'.format(test_account.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_account(self):
        """ cancel an existing account """
        # create a account to cancel
        test_account = AccountFactory()
        resp = self.app.post('/accounts',
                             json=test_account.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # cancel the account
        new_account = resp.get_json()
        # new_account['status'] = 'Cancelled'
        resp = self.app.put('/accounts/{}/cancel'.format(new_account['id']),
                            json=new_account,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        cancelled_account = resp.get_json()
        # self.assertEqual(cancelled_account['status'], 'Cancelled')

    def test_cancel_account_failure(self):
        """ Failure test for cancelling an existing account """
        # create a account to cancel
        test_account = AccountFactory()
        resp = self.app.post('/accounts',
                             json=test_account.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # cancel the account
        new_account = resp.get_json()
        # new_account['status'] = 'Cancelled'
        resp = self.app.put('/accounts/{}/cancel'.format(23),
                            json=new_account,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_server_error(self):
        """Test INTERNAL_SERVER_ERROR"""
        resp = self.app.post('/accounts')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_get_account_by_account_type(self):
        """ Get an account linked to account type"""
        test_account = self._create_accounts(1)[0]
        print(test_account.account_type)
        resp = self.app.get('/accounts/account_type/{}'.format(test_account.account_type),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()[0]
        self.assertEqual(data['owner'], test_account.owner)

    def test_get_account_by_institution_id(self):
        """ Get an account linked to institution id"""
        test_account = self._create_accounts(1)[0]
        print(test_account.institution_id)
        resp = self.app.get('/accounts/institution_id/{}'.format(test_account.institution_id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()[0]
        self.assertEqual(data['owner'], test_account.owner)

    def test_get_account_by_balance(self):
        """ Get an account linked to balance"""
        test_account = self._create_accounts(1)[0]
        print(test_account.balance)
        resp = self.app.get('/accounts/balance/{}'.format(test_account.balance),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()[0]
        self.assertEqual(data['owner'], test_account.owner)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
