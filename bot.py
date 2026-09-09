import requests
from bs4 import BeautifulSoup
from datetime import datetime
url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36","Accept-Language": "en-US,en;q=0.9","Referer": "https://www.google.com/"}
try:
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')
    games = []
    for row in soup.select(".tr_0, .tr_1")[:15]:
        try:
            t=row.select_one(".date_bah")
            tm=row.select_one(".tnms a")
            p=row.select_one(".fprc span")
            if tm: games.append(f"- {t.text.strip() if t else ''} {tm.text.strip()} -> {p.text.strip() if p else ''}")
        except: continue
    if not games: games = ["Proqnozlar hazirlanir, 1 saata yenilenecek"]
    content = f"# Forebet {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n" + "\n".join(games)
except Exception as e:
    content = f"# Xeta {e}"
with open("README.md","w",encoding="utf-8") as f: f.write(content)