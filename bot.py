import pytz, cloudscraper
from datetime import datetime
from bs4 import BeautifulSoup

tz = pytz.timezone("Asia/Baku")
now = datetime.now(tz)
tarix = now.strftime("%d.%m.%Y %H:%M")

fg = []
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

try:
    url = "https://www.predictz.com/predictions/"
    r = scraper.get(url, timeout=30)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        games = soup.select(".ptable .ptable_row")[:7]
        
        for g in games:
            try:
                home = g.select_one(".ptable_home").get_text(strip=True)
                away = g.select_one(".ptable_away").get_text(strip=True)
                pred = g.select_one(".ptable_pred").get_text(strip=True)
                if home and away and pred:
                    fg.append(f"{home} vs {away} → {pred}")
            except:
                continue
        
        if not fg:
            fg = ["Bu saat üçün oyun tapılmadı"]
    
    else:
        fg = [f"Sayt blokladı Kod: {r.status_code}"]

except Exception as e:
    fg = [f"Xeta: {str(e)[:60]}"]

# Demosuz yaz
if not fg:
    fg = ["Proqnozlar hazırda əlçatan deyil"]

oyunlar_text = "\n".join([f"• {x}" for x in fg])

md = f"""⚽ Futbol Proqnozlari - {tarix}

Avtomatik yenilenir (her saat)

Bugunku oyunlar:
{oyunlar_text}

---
Son yenilenme: {tarix} Baki vaxti
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)

print("Yazildi:", tarix)