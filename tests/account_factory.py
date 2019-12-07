"""
Test Factory to make fake objects for testing
"""
import factory
import uuid
from factory.fuzzy import FuzzyChoice
from service.models import account

class AccountFactory(factory.Factory):
    """ Creates fake account that you don't have to feed """
    class Meta:
        model = account
    id = factory.Sequence(lambda n: n)
    owner = 'John Doe'
    account_id = 1
    account_type = "credit card"
    institution_id = 4
    balance = 500

if __name__ == '__main__':
    for _ in range(10):
        account = AccountFactory()
        print(account.serialize())