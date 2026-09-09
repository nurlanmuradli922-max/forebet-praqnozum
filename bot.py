from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# Bakı vaxtı
baku_time = datetime.now(pytz.timezone('Asia/Baku')).strftime("%d.%m.%Y %H:%M")

def get_forebet():
    oyunlar = []
    try:
        # Bu kitabxana 403-ü keçir
        session = requests.Session()
        r = session.get(
            "https://www.forebet.com/en/football-tips-and-predictions-for-today",
            impersonate="chrome120",
            timeout=30
        )
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            for row in soup.select("tr.tr_0, tr.tr_1")[:15]:
                try:
                    ev = row.select_one(".homeTeam").get_text(strip=True)
                    sef = row.select_one(".awayTeam").get_text(strip=True)
                    proqnoz = row.select_one(".forepr").get_text(strip=True)
                    if ev:
                        oyunlar.append(f"| {ev} vs {sef} | {proqnoz} |")
                except:
                    continue
        else:
            print(f"Forebet kod: {r.status_code}")
            return None
    except Exception as e:
        print(f"Xəta: {e}")
        return None
    return oyunlar

oyunlar = get_forebet()

# README.md-ni yarat
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"⚽ Futbol Proqnozlari - {baku_time}\n")
    f.write(f"Avtomatik yenilenir (her saat)\n\n")
    f.write(f"Bugunku oyunlar:\n\n")

    if oyunlar and len(oyunlar) > 0:
        f.write("| Oyun | Proqnoz |\n")
        f.write("|---|---|\n")
        for oy in oyunlar:
            f.write(f"{oy}\n")
    else:
        f.write("1. Sayt cavab vermedi, 5 deq sonra yeniden yoxlanacaq\n")

    f.write(f"\nSon yenilenme: {baku_time} Baki vaxti Menbeler: Forebet.com + PredictZ\n")

print("README yenilendi!")