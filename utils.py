import os
import logging
from datetime import datetime
from decimal import Decimal
from typing import List
from twilio.rest import Client

from pymonzo import MonzoAPI
from pymonzo.api_objects import MonzoAccount, MonzoTransaction

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_api() -> MonzoAPI:
    # TODO - Check connectivity - see https://github.com/pawelad/pymonzo/blob/master/src/pymonzo/exceptions.py
    log.debug("Connecting to api...")
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
    log.debug("Getting current account...")
    current_account = list(filter(lambda x: x.type == "uk_retail", monzo.accounts()))
    if len(current_account) == 1:
        log.debug(f"Got {current_account}...")
        return current_account[0]
    else:
        return None
    

def get_todays_transactions(monzo: MonzoAPI, account: MonzoAccount) -> List[MonzoTransaction]:
    log.debug(f"Getting transactions from {account}...")
    transactions = monzo.transactions(account.id, limit=50)
    return list(filter(lambda x: x.created.date() == (datetime.today().date()), transactions))


def send_sms(change, recipient):
    log.debug(f"Sending sms to {recipient}...")
    client = Client()
    client.messages.create(to=recipient, from_=os.getenv("TWILIO_FROM_NUMBER"),
                                 body=f"You saved £{change / 100} today!")