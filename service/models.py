

"""
Models for Greenprint Account Linking Service

Models
------
Account 

Attributes:
-----------
id (int) - unique id for user
owner (string) - name of owner
account_id (int) - unique id for account
account_type (string) - bank / credit_card / investment / loan / other
institution_id (int) - will map institution id to a unique institution name using a table
balance (float) - current balance in account
isHidden (boolean) - True for accounts that are active


name (string) - the name of the pet
category (string) - the category the pet belongs to (i.e., dog, cat)
available (boolean) - True for pets that are available for adoption

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class account(db.Model):
    """
    Class that represents an Account

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(63))
    account_id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(63))
    institution_id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, primary_key=True)
    isHidden = db.Column(db.Boolean())

    def __repr__(self):
        return '<Account %r>' % (self.name)

    def save(self):
        """
        Saves an Account to the data store
        """
        Account.logger.info('Saving %s', self.name)
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes an Account from the data store """
        Account.logger.info('Deleting %s', self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes an Account into a dictionary """
        return {"id": self.id,
                "owner": self.owner,
                "account_id": self.account_id,
                "account_type": self.account_type,
                "institution_id": self.institution_id,
                "balance": self.balance,
                "isHidden":self.isHidden}

    def deserialize(self, data):
        """
        Deserializes an Account from a dictionary

        Args:
            data (dict): A dictionary containing the Account data
        """
        try:
            self.owner = data['owner']
            self.account_id = data['account_id']
            self.account_type = data['account_type']
            self.institution_id = data['institution_id']
            self.balance = data['balance']
            self.isHidden = data['isHidden']
        except KeyError as error:
            raise DataValidationError('Invalid account: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid account: body of request contained' \
                                      'bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Accounts in the database """
        cls.logger.info('Processing all Accounts')
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """ Finds an account it's ID """
        cls.logger.info('Processing lookup for id %s ...', account_id)
        return cls.query.get(account_id)

    @classmethod
    def find_or_404(cls, pet_id):
        """ Find a Pet by it's account """
        cls.logger.info('Processing lookup or 404 for id %s ...', account_id)
        return cls.query.get_or_404(account_id)

    @classmethod
    def find_by_owner(cls, owner):
        """ Returns all Accounts with the given owner

        Args:
            owner (string): the name of the accounts you want to match
        """
        cls.logger.info('Processing owner query for %s ...', owner)
        return cls.query.filter(cls.owner == owner)

    @classmethod
    def find_by_account_id(cls, account_id):
        """ Returns all of the accounts with the same id

        Args:
            account_id (int): the account id of the accounts you want to match
        """
        cls.logger.info('Processing account id query for %s ...', account_id)
        return cls.query.filter(cls.account_id == account_id)


    @classmethod
    def find_by_account_type(cls, account_type):
        """ Returns all of the accounts of a type

        Args:
            account_type (string): the account type you want to match
        """
        cls.logger.info('Processing account type query for %s ...', account_type)
        return cls.query.filter(cls.account_type == account_type)


    @classmethod
    def find_by_institution_id(cls, institution_id):
        """ Returns all of the accounts with the same institution id

        Args:
            institution_id (int): the institution id of the accounts you want to match
        """
        cls.logger.info('Processing institution id query for %s ...', institution_id)
        return cls.query.filter(cls.institution_id == institution_id)


    @classmethod
    def find_by_balance(cls, balance):
        """ Returns all of the accounts with the same balance

        Args:
            balance (int): the balance of the accounts you want to match
        """
        cls.logger.info('Processing balance query for %s ...', balance)
        return cls.query.filter(cls.balance == balance)


    @classmethod
    def find_by_isHidden(cls, isHidden=True):
        """ Query that finds active accounts """
        """ Returns all active accounts 

        Args:
            isHidden (boolean): True for accounts that are active
        """
        cls.logger.info('Processing available query for %s ...', isHidden)
        return cls.query.filter(cls.isHidden == isHidden)
