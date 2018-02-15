import pytest
from unittest.mock import MagicMock
from datetime import datetime
from pymonzo.api_objects import MonzoTransaction, MonzoAccount
from pymonzo import MonzoAPI
import arrow
from utils import round_up_transaction, get_current_account, \
                  get_api, get_todays_transactions

@pytest.fixture(scope="function")
def account():
    data = {'id': '123', 
        'description': 'Test',
        'created': str(arrow.utcnow()), 
        }
    
    a = MonzoAccount(data=data)
    return a

@pytest.fixture(scope="function")
def transaction():
    data = {'account_balance': 12343, 
        'amount': -150,
        'created': str(arrow.utcnow()), 
        'currency': 'GBP', 
        'description': 'Test',
        'id': '1234', 
        'merchant': 'Boots', 
        'metadata': '', 
        'notes': '', 
        'is_load': False}
    
    t = MonzoTransaction(data=data)
    return t


@pytest.fixture(scope="function")
def api():
    return MagicMock()


def test_round_up_transaction(transaction):
    ru = round_up_transaction(transaction)
    assert ru == 350


def test_round_up_transaction_if_divisible_by_500(transaction):
    transaction.amount = -500
    ru = round_up_transaction(transaction)
    assert ru == 500


def test_get_current_account(api):
    get_current_account(api)
    assert api.accounts.called


def test_get_current_account_none_if_no_accounts(api):
    api.return_value = []
    account = get_current_account(api)
    assert api.accounts.called
    assert account == None


def test_get_api():
    assert isinstance(get_api(), MonzoAPI)


def test_get_todays_transactions(api, account):
    assert api.transactions.called_once_with(account.id)