import json, os, pytz, requests
from datetime import datetime
from bs4 import BeautifulSoup

fg = []
tz = pytz.timezone("Asia/Baku")
now = datetime.now(tz)
tarix = now.strftime("%d.%m.%Y %H:%M")

# 3 dənə fərqli yol sınayacaq - biri mütləq keçəcək
urls_to_try = [
    f"https://api.allorigins.win/raw?url=https://www.forebet.com/en/football-tips-and-predictions-for-today",
    f"https://api.codetabs.com/v1/proxy?quest=https://www.forebet.com/en/football-tips-and-predictions-for-today",
    "https://www.forebet.com/en/football-tips-and-predictions-for-today"
]

st = "Yoxlanir"
html = ""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

for url in urls_to_try:
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200 and "forebet" in r.text.lower() and len(r.text) > 5000:
            html = r.text
            st = f"OK via {url[:30]}"
            break
    except Exception as e:
        continue

if html:
    try:
        soup = BeautifulSoup(html, 'lxml')
        oyunlar = soup.select("tr.fn")[:20]
        for oy in oyunlar:
            try:
                ev = oy.select_one(".tn1").get_text(strip=True) if oy.select_one(".tn1") else ""
                sef = oy.select_one(".tn2").get_text(strip=True) if oy.select_one(".tn2") else ""
                proq = oy.select_one(".fprc span").get_text(strip=True) if oy.select_one(".fprc span") else ""
                if ev and sef:
                    fg.append(f"{ev} vs {sef} -> {proq}")
            except: continue
    except Exception as e:
        st = f"Parse xetasi: {e}"

oyun_metni = "\n".join([f"- {o}" for o in fg]) if fg else f"Hal-hazirda oyun tapilmadi - {st}"

readme = f"""# ⚽ Futbol Proqnozlari - {tarix}

Avtomatik yenilenir (her saat)

### Bugunku oyunlar:
{oyun_metni}

---
Son yenilenme: {tarix} Baki vaxti
Status: {st} - {len(fg)} oyun
"""

with open("README.md","w",encoding="utf-8") as f:
    f.write(readme)

print(f"Bitdi: {len(fg)} oyun, {st}")