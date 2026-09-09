import cloudscraper, json
from datetime import datetime
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
    oyunlar = []
    try:
        # Forebet-i cloudscraper ile açırıq - 403 vermir
        url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"
        r = scraper.get(url, headers=headers, timeout=30)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            for row in soup.select(".tr_0, .tr_1")[:20]:
                try:
                    ev = row.select_one(".tnmsz")
                    proq = row.select_one(".predict")
                    if ev and proq:
                        oyunlar.append(f"{ev.text.strip()} - {proq.text.strip()}")
                except: continue
        else:
            oyunlar = [f"Sayt cavab vermedi Kod: {r.status_code}"]
    except Exception as e:
        oyunlar = [f"Xeta: {e}"]

    # README-e yaz
    vaxt = datetime.now().strftime("%d.%m.%Y %H:%M")
    text = f"⚽ Futbol Proqnozlari - {vaxt}\nAvtomatik yenilenir (her saat)\n\nBugunku oyunlar:\n"
    if oyunlar:
        for i,o in enumerate(oyunlar,1):
            text+=f"{i}. {o}\n"
    else:
        text+="Oyun tapilmadi\n"
    text+=f"\nSon yenilenme: {vaxt} Baki vaxti\nMenbeler: Forebet.com + PredictZ"

    with open("README.md","w",encoding="utf-8") as f:
        f.write(text)
    with open("data.json","w",encoding="utf-8") as f:
        json.dump({"oyunlar":oyunlar,"vaxt":vaxt},f,ensure_ascii=False,indent=2)

if __name__=="__main__":
    main()