import json, os, pytz, cloudscraper
from datetime import datetime
from bs4 import BeautifulSoup

fg = []
st = "Blokdadir"
tz = pytz.timezone("Asia/Baku")
now = datetime.now(tz)
tarix = now.strftime("%d.%m.%Y %H:%M")

try:
    scraper = cloudscraper.create_scraper()
    url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"
    r = scraper.get(url, timeout=30)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        oyunlar = soup.select("tr.fn")[:15]
        for oy in oyunlar:
            try:
                ev = oy.select_one(".tn1").get_text(strip=True)
                sef = oy.select_one(".tn2").get_text(strip=True)
                proq = oy.select_one(".fprc span").get_text(strip=True)
                fg.append(f"{ev} vs {sef} -> {proq}")
            except: continue
        st = f"{len(fg)} oyun tapildi" if fg else "Sayt acildi ama oyun tapilmadi"
    else:
        st = f"Blokdadir Status:{r.status_code}"
except Exception as e:
    st = f"Xeta: {e}"

oyun_metni = "\n".join([f"- {o}" for o in fg]) if fg else f"Hal-hazirda oyunlar yuklenmedi - {st}"

readme = f"""⚽ Futbol Proqnozlari - {tarix}
Avtomatik yenilenir (her saat)
Bugunku oyunlar:
{oyun_metni}

Son yenilenme: {tarix} Baki vaxti
"""
with open("README.md","w",encoding="utf-8") as f:
    f.write(readme)