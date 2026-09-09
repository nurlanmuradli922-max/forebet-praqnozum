import requests, json, os, random, time
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

def get_games():
    url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"
    try:
        time.sleep(random.randint(2,4))
        r = requests.get(url, headers=HEADERS, timeout=25)
        # Forebet bloklayanda Cloudflare səhifəsi qaytarır
        if r.status_code != 200 or "Just a moment" in r.text or len(r.text) < 5000:
            print(f"BLOK: {r.status_code}")
            return None
        
        soup = BeautifulSoup(r.text, "html.parser")
        games = []
        for el in soup.select(".rcnt, .tr_0, .tr_1")[:20]:
            t = el.get_text(" ", strip=True)
            if len(t) > 10:
                games.append(t)
        return games if games else None
    except Exception as e:
        print(f"Xeta: {e}")
        return None

new_games = get_games()

# === ƏSAS HİSSƏ: Boş olanda README-ni silmə ===
if new_games:
    final_games = new_games
    # yadda saxla
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_games, f, ensure_ascii=False, indent=2)
    status = "✅ Canlı proqnozlar"
else:
    # Blokdasa köhnədən götür
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            final_games = json.load(f)
        status = "⚠️ Forebet müvəqqəti blokda idi - köhnə oyunlar göstərilir"
    else:
        final_games = []
        status = "Oyunlar yüklənmədi, növbəti saatda cəhd ediləcək"

# README yaz
now = datetime.now(pytz.timezone("Asia/Baku")).strftime("%d.%m.%Y %H:%M")
text = f"⚽ Futbol Proqnozları - {now}\n\nAvtomatik yenilənir (hər saat)\n\n## Bugünkü oyunlar:\n{status}\n\n"
for g in final_games:
    text += f"- {g}\n"
text += f"\n---\nSon yenilənmə: {now} Baku vaxtı\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(text)