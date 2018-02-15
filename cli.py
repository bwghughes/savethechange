import click
from utils import get_api, round_up_transaction, \
                  get_current_account, get_todays_transactions, \
                  change_to_save, send_sms

@click.option('--recipient', default="447477999880", help='Recipient phone number. \
              Starts 44........')
@click.command()
def go(recipient):
    monzo = get_api()
    current_account = get_current_account(monzo)
    todays_transactions = get_todays_transactions(monzo, current_account)
    change = change_to_save(todays_transactions)
    send_sms(change, recipient)

if __name__ == '__main__':
    go()