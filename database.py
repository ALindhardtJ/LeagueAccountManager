import sqlite3

class AccountManagerDB():
    def __init__(self):
        filename = "./database.sqlite"
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS accounts (account_id INTEGER PRIMARY KEY, region TEXT, tagline TEXT, summoner_name TEXT, username TEXT, password TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS champions (champion_id INTEGER, champion_name TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS skins (skin_id INTEGER, skin_name TEXT, champion_id INTEGER, FOREIGN KEY(champion_id) REFERENCES champions(champion_id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS account_champions (account_id INTEGER, champion_id INTEGER, FOREIGN KEY(account_id) REFERENCES accounts(account_id), FOREIGN KEY(champion_id) REFERENCES champions(champion_id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS account_skins (account_id INTEGER, skin_id INTEGER, FOREIGN KEY(account_id) REFERENCES accounts(account_id), FOREIGN KEY(skin_id) REFERENCES skins(skin_id))")
        self.conn.commit()

#--------------------------------------------------------------------------------------------
# Functions for printing data from tables
    def print_accounts(self):
        self.cur.execute("SELECT * from accounts")
        print(self.cur.fetchall())


    def print_champions(self):
        self.cur.execute("SELECT * from champions")
        print(self.cur.fetchall())


    def print_skins(self):
        self.cur.execute("SELECT * from skins")
        print(self.cur.fetchall())


    def print_account_champions(self):
        self.cur.execute("SELECT * from account_champions")
        print(self.cur.fetchall())


    def print_account_skins(self):
        self.cur.execute("SELECT * from account_skins")
        print(self.cur.fetchall())

#--------------------------------------------------------------------------------------------
# Check for duplicates
    def check_for_duplicates(self):
        tables = ["accounts", "champions", "skins", "account_champions", "account_skins"]
        duplicate_rows = {}
        for table in tables:
            self.cur.execute(f"SELECT * FROM {table}")
            rows = self.cur.fetchall()
            duplicates = [row for row in rows if rows.count(row) < 1]
            if duplicates:
                duplicate_rows[table] = duplicates
        return duplicate_rows
#--------------------------------------------------------------------------------------------
# Retrieve data from tables
    def get_account(self, account_id):
        self.cur.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
        account = self.cur.fetchone()
        return account


    def get_accounts(self):
        self.cur.execute("SELECT * FROM accounts")
        allAccs = self.cur.fetchall()
        return allAccs


    def get_last_account(self):
        self.cur.execute("SELECT * FROM accounts ORDER BY account_id DESC LIMIT 1")
        account = self.cur.fetchone()
        return account
        

    def get_first_account_id(self):
        self.cur.execute("SELECT account_id FROM accounts ORDER BY account_id ASC LIMIT 1")
        account = self.cur.fetchone()
        if account:
            return account[0]
        else:
            return 1
        

    def get_champions_names(self) -> list[str]:
        champions_list = []
        self.cur.execute("SELECT * FROM champions")
        all_champions = self.cur.fetchall()
        for items in all_champions:
            champion_id, champion_name = items
            champions_list.append(champion_name)
        return champions_list
    

    def get_skin_names(self) -> list[str]:
        skins_list = []
        self.cur.execute("SELECT * FROM skins")
        all_champions = self.cur.fetchall()
        for items in all_champions:
            champion_id, champion_name = items
            skins_list.append(champion_name)
        return skins_list    


    def get_accounts_by_champion(self, champion_name:str) -> list:
        self.cur.execute("SELECT champion_id FROM champions WHERE LOWER(champion_name) = LOWER(?)", (champion_name.lower(),))
        champion_id = self.cur.fetchone()
        if champion_id:
            self.cur.execute("SELECT accounts.* FROM accounts JOIN account_champions ON accounts.account_id = account_champions.account_id WHERE account_champions.champion_id = ?", (champion_id[0],))
            accounts = self.cur.fetchall()
            return accounts
        else:
            return []
        

    def get_accounts_by_skin(self, skin_name:str) -> list:
        self.cur.execute("SELECT skin_id FROM skins WHERE LOWER(skin_name) = LOWER(?)", (skin_name.lower(),))
        skin_id = self.cur.fetchone()
        if skin_id:
            self.cur.execute("SELECT accounts.* FROM accounts JOIN account_skins ON accounts.account_id = account_skins.account_id WHERE account_skins.skin_id = ?", (skin_id[0],))
            accounts = self.cur.fetchall()
            return accounts
        else:
            return []


    def get_champions_by_account(self, account_id: int):
        if isinstance(account_id, int):
            self.cur.execute("SELECT champion_id FROM account_champions WHERE account_id = ?", (account_id,))
        # elif isinstance(identifier, str):
        #     self.cur.execute("SELECT account_id FROM accounts WHERE LOWER(summoner_name) = LOWER(?)", (identifier,))
        #     account_id = self.cur.fetchone()
        #     if account_id:
        #         self.cur.execute("SELECT champion_id FROM account_champions WHERE account_id = ?", (account_id[0],))
        #     else:
        #         return []
        else:
            return []

        champion_ids = self.cur.fetchall()

        champions = []
        for champion_id in champion_ids:
            self.cur.execute("SELECT champion_name FROM champions WHERE champion_id = ?", (champion_id))
            champion_name = self.cur.fetchone()
            if champion_name:
                champions.append(champion_name[0])

        return champions
    

    def get_skins_by_account(self, account_id: int):
        if isinstance(account_id, int):
            self.cur.execute("SELECT skin_id FROM account_skins WHERE account_id = ?", (account_id,))
        # elif isinstance(identifier, str):
        #     self.cur.execute("SELECT account_id FROM accounts WHERE LOWER(summoner_name) = LOWER(?)", (identifier,))
        #     account_id = self.cur.fetchone()
        #     if account_id:
        #         self.cur.execute("SELECT skin_id FROM account_skins WHERE account_id = ?", (account_id[0],))
        #     else:
        #         return []
        else:
            return []

        skin_ids = self.cur.fetchall()

        skins = []
        for skin_id in skin_ids:
            self.cur.execute("SELECT skin_name FROM skins WHERE skin_id = ?", (skin_id))
            skin_name = self.cur.fetchone()
            if skin_name:
                skins.append(skin_name[0])

        return skins
    

#--------------------------------------------------------------------------------------------
# Change tables in any way    
    def add_account(
            self,
            region: str,
            tagline: str,
            summoner_name: str,
            username: str,
            password: str
        ) -> tuple:
        self.cur.execute("INSERT INTO accounts (region, tagline, summoner_name, username, password) VALUES (?, ?, ?, ?, ?)", (region, tagline, summoner_name, username, password))
        self.conn.commit()
        self.cur.execute("SELECT * FROM accounts ORDER BY account_id DESC LIMIT 1")
        account = self.cur.fetchone()
        return account


    def delete_account(self, account_id) -> None:
        self.cur.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
        self.cur.execute("DELETE FROM account_champions WHERE account_id = ?", (account_id,))
        self.cur.execute("DELETE FROM account_skins WHERE account_id = ?", (account_id,))
        self.conn.commit()


    def edit_account(self, account_id: int, region: str, tagline: str, summoner_name: str, username: str, password: str) -> None:
        self.cur.execute("UPDATE accounts SET region = ?, tagline = ?, summoner_name = ?, username = ?, password = ? WHERE account_id = ?",
            (region, tagline, summoner_name, username, password, account_id)
        )
        self.conn.commit()


    def drop_table(self, table_name: str) -> None:
        self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")


    def add_champion(self, champion_id: int, champion_name: str) -> None:
        self.cur.execute("INSERT INTO champions (champion_id, champion_name) VALUES (?, ?)", (champion_id, champion_name))
        self.conn.commit()


    def add_skin(self, skin_id: int, skin_name: str, champion_id: int) -> None:
        self.cur.execute("INSERT INTO skins (skin_id, skin_name, champion_id) VALUES (?, ?, ?)", (skin_id, skin_name, champion_id))
        self.conn.commit()


    def add_champion_name_to_dict_by_champion_id(self, skins_info_list: list[dict]) -> list[dict]:
        for skin_info_dict in skins_info_list:
            self.cur.execute(f"Select champion_name FROM champions WHERE champion_id = ?", (skin_info_dict["champion_id"],))
            champion_name = self.cur.fetchone()
            if champion_name:
                skin_info_dict["champion_name"] = champion_name[0]
        return skins_info_list
    

    def assign_champions_to_account(self, summoner_name: str, tagline: str, champion_list: list) -> None:
        self.cur.execute("SELECT account_id FROM accounts WHERE LOWER(summoner_name) = LOWER(?) AND tagline = ?", (summoner_name.lower(), tagline))
        account_id = self.cur.fetchone()
        if account_id:
            champion_ids = []
            for champion in champion_list:
                champion_id = champion[0]
                champion_name = champion[1]
                self.cur.execute("SELECT champion_id FROM champions WHERE LOWER(champion_name) = LOWER(?)", (champion_name.lower(),))
                champion_id_from_table = self.cur.fetchone()
                if champion_id_from_table:
                    if champion_id == champion_id_from_table[0]:
                        champion_ids.append(champion_id)
                    else:
                        print("Champion id's dont match")
                        print(f"{champion_id=}")
                        print(f"{champion_id_from_table[0]=}")
                else:
                    self.add_champion(champion_id=champion_id, champion_name=champion_name)
                    # print("New champion added:", champion_name, champion_id)
                    champion_ids.append(champion_id)

            self.cur.execute("SELECT champion_id FROM account_champions WHERE account_id = ?", (account_id[0],))
            assigned_champion_ids = [row[0] for row in self.cur.fetchall()]
            # print(f"{assigned_champion_ids=}")
            champion_ids_to_assign = [champion_id for champion_id in champion_ids if champion_id not in assigned_champion_ids]
            # print(f"{champion_ids_to_assign=}")
            for champion_id in champion_ids_to_assign:
                self.cur.execute("INSERT INTO account_champions (account_id, champion_id) VALUES (?, ?)", (account_id[0], champion_id))
            self.conn.commit()
        else:
            pass
            print("Account not found.")


    def assign_skins_to_account(self, summoner_name: str, tagline: str, skin_list: list) -> None:
        self.cur.execute("SELECT account_id FROM accounts WHERE LOWER(summoner_name) = LOWER(?) AND tagline = ?", (summoner_name.lower(), tagline))
        account_id = self.cur.fetchone()
        if account_id:
            skin_ids = []
            for skin in skin_list:
                skin_id = skin[0]
                skin_name = skin[1]
                champion_id = skin[2]
                self.cur.execute("SELECT * FROM skins WHERE skin_id = ?", (skin_id,))
                skin_id_from_table = self.cur.fetchone()
                if skin_id_from_table:
                    if skin_id == skin_id_from_table[0]:
                        skin_ids.append(skin_id)
                    else:
                        print("Skin id's dont match")
                        print(f"{skin_id=}")
                        print(f"{skin_id_from_table[0]=}")
                else:
                    self.add_skin(skin_id=skin_id, skin_name=skin_name, champion_id=champion_id)
                    # print("New skin added:", skin_id, skin_name, champion_id)
                    skin_ids.append(skin_id)

            self.cur.execute("SELECT skin_id FROM account_skins WHERE account_id = ?", (account_id[0],))
            assigned_skin_ids = [row[0] for row in self.cur.fetchall()]
            # print(f"{assigned_skin_ids=}")
            skin_ids_to_assign = [skin_id for skin_id in skin_ids if skin_id not in assigned_skin_ids]
            # print(f"{skin_ids_to_assign=}")
            for skin_id in skin_ids_to_assign:
                self.cur.execute("INSERT INTO account_skins (account_id, skin_id) VALUES (?, ?)", (account_id[0], skin_id))
            self.conn.commit()
        else:
            pass
            print("Account not found.")


#-----------------------------------------------------------------------
dbHandler = AccountManagerDB()
#-----------------------------------------------------------------------
