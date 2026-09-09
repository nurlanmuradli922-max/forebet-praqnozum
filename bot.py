import pytz, requests
from datetime import datetime
from bs4 import BeautifulSoup

tz = pytz.timezone("Asia/Baku")
now = datetime.now(tz)
tarix = now.strftime("%d.%m.%Y %H:%M")

fg = []

# GitHub-i bloklamayan proxy ile cekirik
target_url = "https://www.predictz.com/predictions/"
proxy_url = f"https://api.allorigins.win/raw?url={target_url}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    r = requests.get(proxy_url, headers=headers, timeout=40)
    
    if r.status_code == 200 and "ptable" in r.text:
        soup = BeautifulSoup(r.text, "lxml")
        games = soup.select(".ptable .ptable_row")[:8]
        
        for g in games:
            try:
                home = g.select_one(".ptable_home").get_text(strip=True)
                away = g.select_one(".ptable_away").get_text(strip=True)
                pred = g.select_one(".ptable_pred").get_text(strip=True)
                if home and away:
                    fg.append(f"{home} vs {away} → {pred}")
            except:
                continue
    
    # Eger yene bosdursa, fallback - Forebet (bu sayt az bloklayir)
    if not fg:
        r2 = requests.get("https://api.allorigins.win/raw?url=https://www.forebet.com/en/football-tips-and-predictions-for-today", headers=headers, timeout=40)
        if r2.status_code == 200:
            soup2 = BeautifulSoup(r2.text, "lxml")
            rows = soup2.select(".tr_0, .tr_1")[:8]
            for row in rows:
                try:
                    txt = row.get_text(" ", strip=True)
                    if len(txt) > 10:
                        fg.append(txt[:60])
                except:
                    pass

except Exception as e:
    print(f"Xeta: {e}")

# EGER YENE ALINMASA, README-NI POZMA! KOHNESINI SAXLA
if not fg:
    print("Proqnoz alinmadi, README yenilenmir - kohnesi qalir")
    exit(0) # <- en vacib yer, pis yazı yazmasın

oyunlar_text = "\n".join([f"• {x}" for x in fg])

md = f"""⚽ Futbol Proqnozlari - {tarix}

Avtomatik yenilenir (her saat)

Bugunku oyunlar:
{oyunlar_text}

---
Son yenilenme: {tarix} Baki vaxti | Predictz & Forebet
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)

print(f"Ugurla {len(fg)} oyun yazildi")