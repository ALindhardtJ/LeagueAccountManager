from lcu_driver import Connector
from PyQt5.QtCore import QThread
import asyncio

from configuration_files import configuration_values



class MyLcuDriver(QThread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.connector = Connector()
        self.account_data_fetched: bool = False
        self.champions_imported: bool = False
        self.skins_imported: bool = False
        self.account_id: int | None = None
        self.summoner_name: str | None = None
        self.summoner_tagline: str | None = None
        self.summoner_id: int | None = None
        self.summoner_puuid: str | None = None
        self.owned_champions_list: list[int,str] = []
        self.owned_skins_list: list[int,str,int] = []


        @self.connector.open
        async def on_open(connection):
            pass

        @self.connector.ready
        async def on_ready(connection):
            await self.get_summoner_data(connection)
            await self.import_champions(connection)
            await self.import_skins(connection)

        @self.connector.close
        async def disconnect(connection):
            self.account_data_fetched = False
            self.champions_imported = False
            self.skins_imported = False
            self.account_id = None
            self.summoner_name = None
            self.summoner_tagline = None
            self.summoner_id = None
            self.summoner_puuid = None
            self.owned_champions_list = []
            self.owned_skins_list = []


        @self.connector.ws.register('/lol-matchmaking/v1/ready-check', event_types=('UPDATE',))
        async def on_ready_check(connection, event):
            if configuration_values.automatic_queue_accept:
                if event.data["playerResponse"] == "None":
                    response = await connection.request('POST', '/lol-matchmaking/v1/ready-check/accept')        


    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connector.start())


    async def get_summoner_data(self, connection):
        while True:
            response = await connection.request('GET', '/lol-summoner/v1/current-summoner')
            if response.status == 404:
                await asyncio.sleep(1)
            else:
                summoner_data = await response.json()
                self.account_id = summoner_data["accountId"]
                self.summoner_puuid = summoner_data["puuid"]
                self.summoner_id = summoner_data["summonerId"]
                self.summoner_name = summoner_data["gameName"]
                self.summoner_tagline = summoner_data["tagLine"]
                self.account_data_fetched = True
                break


    async def import_champions(self, connection):
        self.owned_champions_list.clear()
        while True:
            response = await connection.request('GET', '/lol-champions/v1/owned-champions-minimal')
            if response.status == 404:
                await asyncio.sleep(1)
            else:
                champions_owned_data = await response.json()
                for champion_dict in champions_owned_data:
                    if champion_dict["ownership"]["owned"] and not champion_dict["ownership"]["rental"]["rented"]:
                        self.owned_champions_list.append([champion_dict["id"], champion_dict["name"]])
                self.champions_imported = True
                break


    async def import_skins(self, connection):
        self.owned_skins_list.clear()
        while True:
            response = await connection.request('GET', f'/lol-champions/v1/inventories/{self.summoner_id}/skins-minimal')
            if response.status == 404:
                await asyncio.sleep(1)
            else:
                skins_owned_data = await response.json()
                for skins_dict in skins_owned_data:
                    if (
                        skins_dict["ownership"]["owned"]
                            and not skins_dict["isBase"]
                                and not skins_dict["ownership"]["rental"]["rented"]
                    ):
                        self.owned_skins_list.append([skins_dict["id"], skins_dict["name"], skins_dict["championId"]])
                self.skins_imported = True
                break