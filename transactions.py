import time

from queries import *
from database_manager import *
from account import *
from user import *
import datetime


class Transaction:
    transaction_table = QueryManager("transaction", db_config, DatabaseManager)
    account_table = QueryManager("account", db_config, DatabaseManager)
    user_table = QueryManager("users", db_config, DatabaseManager)

    def __init__(self, transaction_id, account_id, amount, transaction_type):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_time = datetime.datetime.now()
        self.transaction_type = transaction_type

    @classmethod
    def deposit(cls, account_id, amount):

        account = cls.account_table.select(["account_id", "user_id", "balance"],
                                           f"account_id='{account_id}'")
        accounts = Account(*account[0])

        accounts.deposit_account(account_id, amount)

        cls.transaction_table.insert({
            "account_id": account_id,
            "amount": amount,
            "transaction_time": str(datetime.datetime.now()),
            "transaction_type": "deposit"
        }, "transaction_id")


@classmethod
def withdrawal(cls, account_id, amount):
    account = cls.account_table.select(["account_id", "user_id", "balance"],
                                       f"account_id='{account_id}'")
    accounts = Account(*account[0])
    accounts.withdrawal_account(account_id, amount)
    cls.transaction_table.insert({
        "account_id": account_id,
        "amount": amount,
        "transaction_time": str(datetime.datetime.now()),
        "transaction_type": "withdrawal"
    }, "transaction_id")


@classmethod
def transfer(cls, account_id1, account_id2, amount):
    account = cls.account_table.select(["account_id", "user_id", "balance"],
                                       f"account_id='{account_id1}'")
    transfer = Account(*account[0])
    account2 = cls.account_table.select(["account_id", "user_id", "balance"],
                                        f"account_id='{account_id2}'")
    getter = Account(*account2[0])
    cls.transaction_table.insert({
        "account_id": account_id1,
        "amount": amount,
        "transaction_time": str(datetime.datetime.now()),
        "transaction_type": "transfer"
    }, "transaction_id")
    transfer.withdrawal_account(account_id1, amount)
    getter.deposit_account(account_id2, amount)
