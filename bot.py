import requests, pytz
from datetime import datetime
from bs4 import BeautifulSoup

tz = pytz.timezone("Asia/Baku")
now = datetime.now(tz)
tarix = now.strftime("%d.%m.%Y %H:%M")

fg = []
st = "Yoxlanir"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
}

try:
    # Predictz - GitHub-dan problemsiz açılır
    url = "https://www.predictz.com/predictions/"
    r = requests.get(url, headers=headers, timeout=30)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        # Predictz-in oyun qutuları
        games = soup.select("div.ptable_row")[:20]
        for g in games:
            try:
                teams = g.select_one("div.ptable_name").get_text(strip=True) if g.select_one("div.ptable_name") else ""
                pred = g.select_one("div.ptable_prediction").get_text(strip=True) if g.select_one("div.ptable_prediction") else ""
                if teams:
                    fg.append(f"{teams} -> {pred}")
            except: continue
        st = f"Predictz OK - {len(fg)} oyun"
    else:
        st = f"Status {r.status_code}"
except Exception as e:
    st = f"Xeta: {e}"

if not fg:
    # Fallback demo - heç vaxt boş qalmasın deyə
    fg = [
        "Real Madrid vs Barcelona -> 1X",
        "Man City vs Arsenal -> 1",
        "Bayern vs Dortmund -> Over 2.5",
        "Galatasaray vs Fenerbahce -> 1",
        "Qarabag vs Neftci -> 1"
    ]
    st = st + " (demo gösterilir)"

oyun_metni = "\n".join([f"- {o}" for o in fg])

readme = f"""# ⚽ Futbol Proqnozlari - {tarix}

Avtomatik yenilenir (her saat)

### Bugunku oyunlar:
{oyun_metni}

---
Son yenilenme: {tarix} Baki vaxti
Status: {st}
"""

with open("README.md","w",encoding="utf-8") as f:
    f.write(readme)

print(st)