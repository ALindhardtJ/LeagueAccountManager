import requests
from bs4 import BeautifulSoup
from threading import Thread
from PyQt5.QtCore import QTimer
from typing import Optional
from utilities import utils, obj_names
from database import dbHandler


class AccountManager:
    def __init__(self, parent):
        self.parent = parent
        self.__accounts = {}
        self.__selected_account: Optional["Account"] = None
        self.__collecting_data: bool = False
        self.__accounts_filtered: bool = False

    @property
    def accounts(self) -> dict:
        return self.__accounts
    
    @property
    def selected_account(self):
        return self.__selected_account
    
    def set_selected_account(self, account: Optional["Account"]) -> None:
        self.__selected_account = account

    def is_selected_account(self, account: Optional["Account"]) -> bool:
        return account == self.selected_account
    
    @property
    def collecting_data(self) -> bool:
        return self.__collecting_data

    def set_collecting_data(self, collecting_data: bool):
        self.__collecting_data = collecting_data

    @property
    def accounts_filtered(self) -> bool:
        return self.__accounts_filtered

    def set_accounts_filtered(self, accounts_filtered: bool):
        self.__accounts_filtered = accounts_filtered


    def create_account(self, account_id: int, summoner_name: str, region: str, tagline: str, username: str, password: str) -> "Account":
        account = Account(
            parent=self,
            account_id = account_id,
            summoner_name = summoner_name,
            region = region,
            tagline = tagline,
            username = username,
            password = password
        )
        self.__accounts[account.account_id] = account
        return account


    def delete_selected_account(self) -> None:
        if self.selected_account is not None:
            if self.selected_account.account_id in self.accounts:
                del self.accounts[self.selected_account.account_id]
                self.set_selected_account(account=None)


    def edit_selected_account(self, region: str, tagline: str, summoner_name: str, username: str, password: str) -> None:
        if self.selected_account is not None:
            if self.selected_account.account_id in self.accounts:
                self.selected_account.set_region(region)
                self.selected_account.set_tagline(tagline)
                self.selected_account.set_summoner_name(summoner_name)
                self.selected_account.set_username(username)
                self.selected_account.set_password(password)

  

    def sort_accounts_by_rank(self):
        tiers = utils.TIERS
        roman_numerals = {"I": 1, "II": 2, "III": 3, "IV": 4}
        max_lp = 100

        def rank_to_value(account):
            rank = account.rank
            if rank is None:
                return float('inf') 
            if "Challenger" in rank or "GrandMaster" in rank or "Master" in rank:
                parts = rank.split()
                tier = parts[0]
                lp = max_lp - int(parts[2]) if len(parts) > 1 else max_lp
                numeral = 0
            elif "Unranked" in rank:
                tier = "Unranked"
                numeral = 0
                lp = max_lp
            else:
                parts = rank.split()
                tier = parts[0]
                numeral = roman_numerals[parts[1]]
                lp = max_lp - int(parts[3]) if len(parts) > 3 else max_lp

            return tiers.index(tier) * 500 + numeral * 100 + lp

        sorted_accounts = sorted(self.__accounts.values(), key=rank_to_value)

        self.__accounts = {account.account_id: account for account in sorted_accounts}


    def filter_accounts(self, account_ids: list):
        self.set_accounts_filtered(True)
        self.__accounts = {account_id: account for account_id, account in self.__accounts.items() if account_id in account_ids}


    def update_accounts_from_db(self):
        self.set_accounts_filtered(False)

        for account_data in dbHandler.get_accounts():
            account_id, region, tagline, summoner_name, username, password = account_data
            if account_id in self.__accounts:
                existing_account = self.__accounts[account_id]
                existing_account.set_summoner_name(summoner_name)
                existing_account.set_region(region)
                existing_account.set_tagline(tagline)
                existing_account.set_username(username)
                existing_account.set_password(password)
            else:
                account = self.create_account(account_id, summoner_name, region, tagline, username, password)
                if self.selected_account is None:
                    self.set_selected_account(account)
    

    def fetch_account_data(self, single_account: Optional["Account"] = None):
        self.set_collecting_data(True)

        if self.parent.buttons.get_button(obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value):
            self.parent.buttons.get_button(obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value).setText("Collecting account data")
            self.parent.buttons.get_button(obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value).setChecked(self.collecting_data)
            self.parent.buttons.get_button(obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value).setDisabled(True)

        threads = []
        finished_threads = 0

        def callback():
            nonlocal finished_threads
            finished_threads += 1
            if finished_threads == len(threads):
                self.sort_accounts_by_rank()
                self.set_collecting_data(False)
                self.parent.buttons.get_button(obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value).setEnabled(True)
                self.parent.buttons.get_button(obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value).setText("Refresh all account data")
                self.parent.buttons.get_button(obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value).setChecked(self.collecting_data)
                
                QTimer.singleShot(0, self.parent.refresh_gui_account_manager)

        if single_account:
            thread = Thread(target=self.web_scrape, args=(single_account, callback))
            thread.start()
            threads.append(thread)
        else:
            for account in self.accounts.values():
                thread = Thread(target=self.web_scrape, args=(account, callback))
                thread.start()
                threads.append(thread)


    def web_scrape(self, account: "Account", callback: callable):
        url = f"{utils.LOG_URL}{account.region.lower()}/{account.summoner_name}-{account.tagline}"
        response = requests.get(url, headers=utils.HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')

        level_element = soup.find("div", class_="bannerSubtitle")
        level = int(level_element.text.strip().split()[1]) if level_element else "Failed"

        games_played_element = soup.find("div", id="graphDD4", class_="pie-chart small")
        games_played = games_played_element.text.strip() if games_played_element else "Failed"

        winrate_element = soup.find("div", id="graphDD5", class_="pie-chart small")
        winrate = winrate_element.text.strip() if winrate_element else "Failed"

        if "%" in games_played:
            games_played, winrate = winrate, games_played

        try:
            rank = soup.find("div", class_="leagueTier").text.strip()
            if "Master" in rank or "Grandmaster" in rank or "Challenger" in rank:
                rank, lp, lp_string = rank.split()
                rank = f"{rank} - {lp} {lp_string}"
            elif "Diamond" in rank:
                rank, tier, lp, lp_string = rank.split()
                rank = f"{rank} {tier} - {lp} {lp_string}"
            elif rank != "Unranked":
                try:
                    lp = soup.find("span", class_="leaguePoints").text.strip()
                    rank = rank + " - " + lp + " LP"
                except:
                    pass
        except:
            rank = "Unranked"
    
        account.set_level(level)
        account.set_rank(rank)
        account.set_games_played(games_played)
        account.set_winrate(winrate)

        callback()



class Account():
    def __init__(self, parent, account_id: int, summoner_name: str, region: str, tagline: str, username: str, password: str):
        self.parent = parent
        self.__account_id: int = account_id
        self.__summoner_name: str = summoner_name
        self.__region: str = region
        self.__tagline: str = tagline
        self.__username: str = username
        self.__password: str = password
        self.__level: int | None = None
        self.__rank: str | None = None
        self.__winrate: str | None = None
        self.__games_played: int | None = None


    @property
    def account_id(self) -> int:
        return self.__account_id

    def set_account_id(self, account_id: int):
        self.__account_id = account_id

    @property
    def summoner_name(self) -> str:
        return self.__summoner_name

    def set_summoner_name(self, summoner_name: str):
        self.__summoner_name = summoner_name

    @property
    def region(self) -> str:
        return self.__region

    def set_region(self, region: str):
        self.__region = region

    @property
    def tagline(self) -> str:
        return self.__tagline

    def set_tagline(self, tagline: str):
        self.__tagline = tagline

    @property
    def username(self) -> str:
        return self.__username

    def set_username(self, username: str):
        self.__username = username

    @property
    def password(self) -> str:
        return self.__password

    def set_password(self, password: str):
        self.__password = password

    @property
    def level(self) -> int:
        return self.__level

    def set_level(self, level: int):
        self.__level = level

    @property
    def rank(self) -> str:
        return self.__rank

    def set_rank(self, rank: str):
        self.__rank = rank

    @property
    def winrate(self) -> str:
        return self.__winrate

    def set_winrate(self, winrate: str):
        self.__winrate = winrate

    @property
    def games_played(self) -> int:
        return self.__games_played

    def set_games_played(self, games_played: int):
        self.__games_played = games_played
