from pathlib import Path

REGIONS = ["EUW", "EUNE", "KR", "NA", "OCE", "LAN", "LAS", "JP", "BR", "RU", "TR"]
TIERS = ["Challenger", "GrandMaster", "Master", "Diamond", "Emerald", "Platinum", "Gold", "Silver", "Bronze", "Iron", "Unranked"]
LOG_URL = "https://www.leagueofgraphs.com/summoner/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

CLIPBOARD_LOGO_FILE = Path("images/copy.png")
APP_ICON_FILE = Path("images/icon.ico")
APP_LOGO_FILE = Path("images/account_man_icon_2.png")
stylesheet_file = Path("stylesheets/stylesheet.css")
with stylesheet_file.open('r') as css_file:
    STYLESHEET = css_file.read()

