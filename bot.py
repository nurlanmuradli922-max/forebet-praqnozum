import requests, pytz
from datetime import datetime
from bs4 import BeautifulSoup

tz = pytz.timezone("Asia/Baku")
now = datetime.now(tz)
tarix = now.strftime("%d.%m.%Y %H:%M")

fg = []
st = "Yoxlanilir"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,az;q=0.8",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

try:
    url = "https://www.predictz.com/predictions/"
    r = requests.get(url, headers=headers, timeout=30)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        # Predictz -deki oyunlar
        games = soup.select(".ptable .ptable_row")[:7]
        
        for g in games:
            try:
                home = g.select_one(".ptable_home").get_text(strip=True)
                away = g.select_one(".ptable_away").get_text(strip=True)
                pred = g.select_one(".ptable_pred").get_text(strip=True)
                if home and away:
                    fg.append(f"{home} vs {away} → {pred}")
            except:
                continue
        
        st = f"Ugurla yenilendi - Kod {r.status_code}"
        if not fg:
            fg = ["Bu saat üçün proqnoz tapılmadı"]
            st = "Sayt açıldı amma oyun tapılmadı"
    else:
        st = f"Sayt blokladı - Kod {r.status_code}"
        fg = ["Proqnozlar hazırda əlçatan deyil, növbəti saat yoxlanacaq"]

except Exception as e:
    st = f"Xəta: {str(e)[:50]}"
    fg = ["Proqnozlar hazırda əlçatan deyil, növbəti saat yoxlanacaq"]

# README YAZ
oyunlar_text = "\n".join([f"• {x}" for x in fg])

md = f"""⚽ Futbol Proqnozlari - {tarix}

Avtomatik yenilenir (her saat)

Bugunku oyunlar:
{oyunlar_text}

---
Son yenilenme: {tarix} Baki vaxti
Status: {st}
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)

print(md)