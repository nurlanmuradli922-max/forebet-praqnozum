from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

baku = pytz.timezone('Asia/Baku')
now_str = datetime.now(baku).strftime("%d.%m.%Y %H:%M")

def forebet_cehd():
    try:
        s = requests.Session()
        r = s.get("https://www.forebet.com/en/football-tips-and-predictions-for-today",
                  impersonate="chrome120", timeout=40)
        if r.status_code!= 200:
            return None
        soup = BeautifulSoup(r.text, 'lxml')
        oyunlar = []
        for row in soup.select("tr.tr_0, tr.tr_1")[:10]:
            ev = row.select_one(".homeTeam")
            sef = row.select_one(".awayTeam")
            pr = row.select_one(".forepr")
            if ev and sef:
                oyunlar.append(f"- **{ev.get_text(strip=True)} vs {sef.get_text(strip=True)}** -> Proqnoz: {pr.get_text(strip=True) if pr else '1'}")
        return oyunlar if oyunlar else None
    except:
        return None

def predictz_cehd():
    try:
        s = requests.Session()
        r = s.get("https://www.predictz.com/predictions/", impersonate="chrome120", timeout=40)
        soup = BeautifulSoup(r.text, 'lxml')
        oyunlar = []
        for row in soup.select(".ptable tr")[:10]:
            cols = row.select("td")
            if len(cols) >= 2:
                oyunlar.append(f"- **{cols[0].get_text(strip=True)}** -> {cols[1].get_text(strip=True)}")
        return oyunlar if oyunlar else None
    except:
        return None

# Evvel Forebet, alinmasa PredictZ
netice = forebet_cehd()
menbe = "Forebet.com"
if not netice:
    netice = predictz_cehd()
    menbe = "PredictZ.com"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"⚽ Futbol Proqnozlari - {now_str}\n")
    f.write("Avtomatik yenilenir (her saat)\n\n")
    f.write("Bugunku oyunlar:\n\n")
    if netice:
        for o in netice:
            f.write(o + "\n")
    else:
        f.write("Hələlik oyun tapılmadı, 1 saata yenilənəcək.\n")
    f.write(f"\nSon yenilenme: {now_str} Baki vaxti | Menbe: {menbe}\n")

print("Hazirdir!")