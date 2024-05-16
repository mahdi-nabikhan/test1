from queries import *
from database_manager import *


class Account:
    account_table = QueryManager("account", db_config, DatabaseManager)

    def __init__(self, account_id, user_id, balance):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance

    @classmethod
    def create_accounts(cls, user_id, balance):
        accounts = cls.account_table.insert({
            "user_id": user_id,
            "balance": balance
        }, "account_id")
        accounts_id = accounts[0][0]
        return cls(accounts_id, user_id, balance)

    def deposit_account(self, account_id, values):
        self.balance += values
        self.account_table.update({"balance": self.balance},
                                  f"account_id={account_id}")

    def withdrawal_account(self, account_id, values):
        if self.balance < values:
            raise ValueError("nooooo")
        self.balance -= values
        self.account_table.update({"balance": self.balance},
                                  f"account_id={account_id}")
