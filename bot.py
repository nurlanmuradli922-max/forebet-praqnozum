import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
}

def get_forebet():
    try:
        r = requests.get("https://www.forebet.com/en/football-tips-and-predictions-for-today", headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        out = []
        for row in soup.select(".tr_0, .tr_1, .tr_2, .tr_3")[:20]:
            t = row.select_one(".date_bah")
            nm = row.select_one(".tnms a")
            pr = row.select_one(".fprc span")
            if nm and pr:
                out.append(f"- {t.text.strip() if t else ''} {nm.text.strip()} -> Proqnoz: {pr.text.strip()}")
        return out
    except:
        return []

def get_predictz():
    try:
        r = requests.get("https://www.predictz.com/predictions/", headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        out = []
        for row in soup.select(".ptable .pttr")[:20]:
            teams = row.select_one(".pttd.pt_name")
            pred = row.select_one(".pttd.pt_pred")
            if teams:
                out.append(f"- {teams.text.strip()} -> {pred.text.strip() if pred else ''}")
        return out
    except:
        return []

games = get_forebet()
if not games:
    games = get_predictz()
if not games:
    games = ["Hal-hazırda oyunlar yüklənmədi, növbəti saatda yenidən cəhd edəcək - Forebet müvəqqəti blokdadır"]

now = datetime.now().strftime("%d.%m.%Y %H:%M")
content = f"# ⚽ Futbol Proqnozları - {now}\n\n**Avtomatik yenilənir (hər saat)**\n\n### Bugünkü oyunlar:\n\n" + "\n".join(games) + f"\n\n---\nSon yenilənmə: {now} Baku vaxtı"

with open("README.md","w",encoding="utf-8") as f:
    f.write(content)
print(content)