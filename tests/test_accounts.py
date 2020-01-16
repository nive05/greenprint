"""
Test cases for account Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
import uuid
from werkzeug.exceptions import NotFound
from service.models import account, DataValidationError, db
from service import app

DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost:3306/test')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccounts(unittest.TestCase):
    """ Test Cases for Accounts """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        account.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_an_account(self):
        """ Create an account and assert that it exists """
        account = account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        self.assertTrue(account != None)
        self.assertEqual(account.id, None)
        self.assertEqual(account.owner, "John Doe")
        self.assertEqual(account.account_id, 1)
        self.assertEqual(account.account_type, "credit card")
        self.assertEqual(account.institution_id, 4)
        self.assertEqual(account.balance, 500)

    def test_add_an_account(self):
        """ Create an account and add it to the database """
        accounts = account.all()
        self.assertEqual(accounts, [])
        account = account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        self.assertTrue(account != None)
        self.assertEqual(account.id, None)
        account.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(account.id, 1)
        accounts = account.all()
        self.assertEqual(len(accounts), 1)

    def test_update_an_account(self):
        """ Update an account """
        account = account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        account.save()
        self.assertEqual(account.id, 1)
        # Change it an save it
        account.account_id = 2
        account.save()
        self.assertEqual(account.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        accounts = account.all()
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0].account_id, 2)

    def test_delete_an_account(self):
        """ Delete an account """
        account = account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        account.save()
        self.assertEqual(len(account.all()), 1)
        # delete the account and make sure it isn't in the database
        account.delete()
        self.assertEqual(len(account.all()), 0)

    def test_serialize_an_account(self):
        """ Test serialization of an account """
        account = account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        data = account.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('owner', data)
        self.assertEqual(data['owner'], "John Doe")
        self.assertIn('account_id', data)
        self.assertEqual(data['account_id'], 1)
        self.assertIn('account_type', data)
        self.assertEqual(data['account_type'], "credit card")
        self.assertIn('institution_id', data)
        self.assertEqual(data['institution_id'], 4)
        self.assertIn('balance', data)
        self.assertEqual(data['balance'], 500)

    def test_deserialize_an_account(self):
        """ Test deserialization of an account """ #also had status
        data = {"owner" : "John Doe","account_id" : 1,"account_type" : "credit card","institution_id" : 4,"balance" : 500}
        account = account()
        account.deserialize(data)
        self.assertNotEqual(account, None)
        self.assertEqual(account.id, None)
        self.assertEqual(account.owner, "John Doe"),
        self.assertEqual(account.account_id, 1),
        self.assertEqual(account.account_type, "credit card"),
        self.assertEqual(account.institution_id, 4),
        self.assertEqual(account.balance, 500)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        account = account()
        self.assertRaises(DataValidationError, account.deserialize, data)

    def test_find_account(self):
        """ Find an account by ID """
        account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500).save()
        next_account = account( owner = "Jane Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        next_account.save()
        account = account.find(next_account.id)
        self.assertIsNot(account, None)
        self.assertEqual(account.id, next_account.id)
        self.assertEqual(account.owner, "Jane Doe")
        self.assertEqual(account.account_id, 1),
        self.assertEqual(account.account_type, "credit card"),
        self.assertEqual(account.institution_id, 4),
        self.assertEqual(account.balance, 500)
    
    def test_find_account_by_owner(self):
        """ Find an account by owner """
        account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500).save()
        next_account = account( owner = "Jane Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        next_account.save()
        account = account.find_by_owner(2)[0]
        self.assertIsNot(account, None)
        self.assertEqual(account.id, next_account.id)
        self.assertEqual(account.owner, "Jane Doe")
        self.assertEqual(account.account_id, 1),
        self.assertEqual(account.account_type, "credit card"),
        self.assertEqual(account.institution_id, 4),
        self.assertEqual(account.balance, 500)
    

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        account( owner = "John Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500).save()
        next_account = account( owner = "Jane Doe", account_id = 1, account_type = "credit card", institution_id = 4, balance = 500)
        next_account.save()
        account = account.find_or_404(next_account.id)
        self.assertIsNot(account, None)
        self.assertEqual(account.id, next_account.id)
        self.assertEqual(account.owner, "Jane Doe")
        self.assertEqual(account.account_id, 1),
        self.assertEqual(account.account_type, "credit card"),
        self.assertEqual(account.institution_id, 4),
        self.assertEqual(account.balance, 500)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, account.find_or_404, 0)




######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPets)
    unittest.TextTestRunner(verbosity=2).run(suite)
