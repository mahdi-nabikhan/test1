import psycopg2

db_config = {
    'dbname': 'bank_system',
    'user': 'postgres',
    'password': '12345678',
    'host': 'localhost',
    'port': '4060'}

connections = psycopg2.connect(**db_config)
cursor = connections.cursor()

users_table = """
CREATE TABLE users (
user_id serial primary key,
username varchar (300) not null,
password varchar(300) not null
);
"""

account_table = """
CREATE TABLE account (
account_id serial primary key,
user_id int  not null,
balance int not null,
foreign key (user_id) references users(user_id)
);

"""

transaction_table = """
CREATE TABLE transaction (
    transaction_id serial PRIMARY KEY,
    account_id int NOT NULL,
    amount int NOT NULL,
    transaction_time timestamp DEFAULT CURRENT_TIMESTAMP,
    transaction_type varchar(300) NOT NULL CHECK (transaction_type IN ('deposit', 'withdrawal', 'transfer')),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

"""
cursor.execute(transaction_table)
connections.commit()
