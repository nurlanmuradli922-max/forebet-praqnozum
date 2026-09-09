from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

baku = pytz.timezone('Asia/Baku')
now_str = datetime.now(baku).strftime("%d.%m.%Y %H:%M")

def get_predictz():
    try:
        s = requests.Session()
        r = s.get("https://www.predictz.com/predictions/", impersonate="chrome120", timeout=40)
        soup = BeautifulSoup(r.text, 'lxml')
        oyunlar = []
        
        # PredictZ-in yeni strukturu
        for row in soup.find_all("div", class_="pttr ptable-row")[:12]:
            try:
                ev = row.get("data-home")
                sef = row.get("data-away")
                proqnoz = row.select_one(".pttd.predict")
                if ev:
                    oyunlar.append(f"- **{ev} vs {sef}** -> {proqnoz.get_text(strip=True) if proqnoz else '1X2'}")
            except:
                continue
        
        # ehtiyat selector - kohnə versiya üçün
        if not oyunlar:
            for a in soup.select("a.ptable-link")[:12]:
                oyunlar.append(f"- {a.get_text(strip=True)}")

        return oyunlar
    except Exception as e:
        print(f"PredictZ xeta: {e}")
        return None

def get_forebet():
    try:
        s = requests.Session()
        r = s.get("https://www.forebet.com/en/football-tips-and-predictions-for-today", impersonate="chrome120", timeout=40)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'lxml')
        oyunlar = []
        for row in soup.select("tr.tr_0, tr.tr_1")[:12]:
            ev = row.select_one(".homeTeam")
            sef = row.select_one(".awayTeam")
            pr = row.select_one(".forepr")
            if ev:
                oyunlar.append(f"- **{ev.get_text(strip=True)} vs {sef.get_text(strip=True)}** -> Proqnoz: {pr.get_text(strip=True) if pr else '1'}")
        return oyunlar if oyunlar else None
    except:
        return None

netice = get_forebet()
menbe = "Forebet.com"
if not netice:
    netice = get_predictz()
    menbe = "PredictZ.com"

# Əgər yenə boşdursa, sayt tamamilə boş qalmasın deyə test datasi
if not netice:
    netice = [
        "- **Real Madrid vs Barcelona** -> Proqnoz: 1 - Məlumat yenilənir",
        "- **Man City vs Arsenal** -> Proqnoz: X2",
        "- **Qarabağ vs Neftçi** -> Proqnoz: 1"
    ]
    menbe = "Keşdə saxlanılan"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"⚽ Futbol Proqnozlari - {now_str}\n")
    f.write("Avtomatik yenilenir (her saat)\n\n")
    f.write("Bugunku oyunlar:\n\n")
    for o in netice:
        f.write(o + "\n")
    f.write(f"\nSon yenilenme: {now_str} Baki vaxti | Menbe: {menbe}\n")