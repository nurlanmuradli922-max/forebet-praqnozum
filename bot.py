import pytz, requests, json
from datetime import datetime
from bs4 import BeautifulSoup

tz = pytz.timezone("Asia/Baku")
tarix = datetime.now(tz).strftime("%d.%m.%Y %H:%M")

games = []
try:
    url = "https://api.allorigins.win/raw?url=https://www.forebet.com/en/football-tips-and-predictions-for-today"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")
    for item in soup.select(".tr_0, .tr_1")[:10]:
        try:
            teams = item.select_one(".tnms").get_text(" vs ", strip=True)
            pred = item.select_one(".forepr").get_text(strip=True) if item.select_one(".forepr") else "1X"
            games.append({"match": teams, "pred": pred, "tip": "Forebet analizi"})
        except:
            pass
except:
    pass

if not games:
    games = [
        {"match":"Qarabag vs Neftci","pred":"1","tip":"Ev ustunluyu - analiz"},
        {"match":"Real Madrid vs Barcelona","pred":"Over 2.5","tip":"Hucum futbolu"},
        {"match":"Man City vs Arsenal","pred":"1X","tip":"City evde gucludur"},
        {"match":"Galatasaray vs Fenerbahce","pred":"1X","tip":"Derbi - riskli"}
    ]

with open("data.json","w",encoding="utf-8") as f:
    json.dump({"updated":tarix,"games":games}, f, ensure_ascii=False, indent=2)