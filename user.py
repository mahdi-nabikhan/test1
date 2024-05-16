from queries import *
from database_manager import *
from account import *
from transactions import *


class User:
    user_table = QueryManager("users", db_config, DatabaseManager)
    account_table = QueryManager("account", db_config, DatabaseManager)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def login(cls, username, password):
        users = cls.user_table.select(
            ["username", "password"],
            f"username='{username}' and password='{password}'"
        )
        if users:
            print("welcome")
            return cls(*users[-1])
        else:
            raise ValueError("invalid username and password")

    def register(self):
        users = self.user_table.select(
            ["username"],
            f"username='{self.username}'"
        )
        if not users:
            user = self.user_table.insert(
                {

                    "username": self.username,
                    "password": self.password,

                }, "user_id"
            )
            return User(user[0][0], self.username, self.password)

        else:
            raise ValueError(" this username already exists")

    def create_accounts(self, balance):
        user_id = User.user_table.select(["user_id"], f"username='{self.username}'")
        Account.create_accounts(user_id[0][0], balance)

    def deposit(self, account_id, value):
        account = User.account_table.select(["account_id", "user_id", "balance"],
                                            f"account_id='{account_id}'")

        new = Account(*account[0])
        new.deposit_account(account_id, value)

    def withdrawal(self, account_id, value):
        account = User.account_table.select(["account_id", "user_id", "balance"],
                                            f"account_id='{account_id}'")

        new = Account(*account[0])
        new.withdrawal_account(account_id, value)
