import click
from utils import get_api, round_up_transaction, \
                  get_current_account, get_todays_transactions, \
                  change_to_save


@click.command()
def go():
    monzo = get_api()
    current_account = get_current_account(monzo)
    todays_transactions = get_todays_transactions(monzo, current_account)
    change = change_to_save(todays_transactions)
    print(change)

if __name__ == '__main__':
    go()