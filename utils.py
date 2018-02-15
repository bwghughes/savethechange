import logging
from datetime import datetime
from decimal import Decimal
from typing import List

from pymonzo import MonzoAPI
from pymonzo.api_objects import MonzoAccount, MonzoTransaction

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def get_api() -> MonzoAPI:
    # TODO - Check connectivity - see https://github.com/pawelad/pymonzo/blob/master/src/pymonzo/exceptions.py
    return MonzoAPI()


def change_to_save(transactions: List[MonzoTransaction]) -> List[float]:
    change = []
    for t in transactions:
        change.append(round_up_transaction(t))
    return sum(change)


def round_up_transaction(transaction: MonzoTransaction) -> float:
    if transaction.amount:
        # TODO - Clean up
        saved_change = divmod(transaction.amount, 500)[1]
        
        # If its bang on add another fiver
        if saved_change == 0:
            saved_change = 500
        return saved_change


def get_current_account(monzo: MonzoAPI) -> MonzoAccount:
    current_account = list(filter(lambda x: x.type == "uk_retail", monzo.accounts()))
    if len(current_account) == 1:
        return current_account[0]
    else:
        return None
    

def get_todays_transactions(monzo: MonzoAPI, account: MonzoAccount) -> List[MonzoTransaction]:
    transactions = monzo.transactions(account.id, limit=50)
    return list(filter(lambda x: x.created.date() == (datetime.today().date()), transactions))
