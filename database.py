import sqlite3
from os import path


class AccountManagerDB():
    def __init__(self):
        filename = "./database.sqlite"
        print(filename)
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS accounts (pkID INTEGER PRIMARY KEY, region TEXT, sumName TEXT, username TEXT, password TEXT)")
        self.conn.commit()

# Add an account to db
    def add_account(self, region, sumName, username, password):
        self.cur.execute("INSERT INTO accounts (region, sumName, username, password) VALUES (?, ?, ?, ?)", (region, sumName, username, password))
        self.conn.commit()

# Get one specific account
    def get_account(self, pkID):
        self.cur.execute(f"SELECT * FROM accounts WHERE pkID = {pkID}")
        account = self.cur.fetchone()
        return account

# Get all accounts from db
    def get_accounts(self):
        self.cur.execute("SELECT * FROM accounts")
        allAccs = self.cur.fetchall()
        return allAccs

# Get last account in db
    def get_last_account(self):
        self.cur.execute("SELECT * FROM accounts ORDER BY pkID DESC LIMIT 1")
        account = self.cur.fetchone()
        return account

# Delete account from db
    def delete_account(self, pkID):
        self.cur.execute(f"DELETE FROM accounts WHERE pkID = {pkID}")
        self.conn.commit()

# Edit account info
    def edit_account(self, edit, column, pkID):
        self.cur.execute(f"UPDATE accounts SET {column} = '{edit}' WHERE pkID = {pkID}")
        self.conn.commit()

# Print all accounts in db
    def print_all_accounts(self):
        self.cur.execute("SELECT * FROM accounts")
        allAccs = self.cur.fetchall()
        for acc in allAccs:
            print(acc)

# Drop table 'accounts'
    def drop_table(self):
        self.cur.execute("DROP TABLE IF EXISTS accounts")

dbHandler = AccountManagerDB()


#-----------------------------------------------------------------------
# dbHandler.add_account("eune","test","test","test")

# dbHandler.get_last_account()

# dbHandler.delete_account()

# dbHandler.get_account()

# allAccs = dbHandler.get_accounts()
# print(allAccs)

# dbHandler.drop_table()

# dbHandler.print_all_accounts()