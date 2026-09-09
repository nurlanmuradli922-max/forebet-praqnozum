import pytz, requests
from datetime import datetime
from bs4 import BeautifulSoup

tz = pytz.timezone("Asia/Baku")
now = datetime.now(tz)
tarix = now.strftime("%d.%m.%Y %H:%M")
fg = []

url = "https://api.allorigins.win/raw?url=https://www.predictz.com/predictions/"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        games = soup.select(".ptable_row")[:8]
        for g in games:
            h = g.select_one(".ptable_home")
            a = g.select_one(".ptable_away")
            p = g.select_one(".ptable_pred")
            if h and a and p:
                fg.append(f"{h.text.strip()} vs {a.text.strip()} -> {p.text.strip()}")
except Exception as e:
    print(e)

if not fg:
    print("alinmadi, README pozulmasin")
    exit(0)

txt = "\n".join([f"• {x}" for x in fg])
md = f"⚽ Futbol Proqnozlari - {tarix}\n\nAvtomatik yenilenir (her saat)\n\nBugunku oyunlar:\n{txt}\n\n---\nSon yenilenme: {tarix} Baki vaxti\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)