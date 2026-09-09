import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

try:
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    games = []
    # Forebet yeni dizayn
    for row in soup.select(".tr_0, .tr_1")[:15]:
        try:
            time_el = row.select_one(".date_bah")
            teams_el = row.select_one(".tnms a")
            pred_el = row.select_one(".fprc span")
            if teams_el:
                games.append(f"- {time_el.text.strip() if time_el else ''} {teams_el.text.strip()} -> {pred_el.text.strip() if pred_el else ''}")
        except:
            continue

    if not games:
        # fallback - sadə mesaj
        games = ["Bugün üçün proqnozlar yüklənmədi, 1 saatdan sonra avtomatik yenilənəcək"]

    content = f"# Forebet Proqnoz - {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\nSon yenilənmə: {datetime.now()}\n\n### Bugünkü oyunlar:\n\n" + "\n".join(games)

except Exception as e:
    content = f"# Xəta - {datetime.now()}\n\nXəta oldu: {e}\n\nBir azdan yenidən yoxla"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print(content)