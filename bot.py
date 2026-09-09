import requests
from datetime import datetime
from bs4 import BeautifulSoup

url="https://www.forebet.com/en/football-tips-and-predictions-for-today"
h={"User-Agent":"Mozilla/5.0"}
html=requests.get(url,headers=h,timeout=30).text
soup=BeautifulSoup(html, "html.parser")

matches = []
for row in soup.select(".tr_0, .tr_1")[:30]:
    teams = row.get_text(" ", strip=True)
    matches.append(f"- {teams}")

if not matches:
    matches = ["Oyun tapılmadı, Forebet bloklayıb, bir azdan yenidən yoxla"]

content = f"""# Forebet Proqnoz - {datetime.now().strftime('%d.%m.%Y %H:%M')}

Son yenilənmə: {datetime.now()}

## Bugünkü oyunlar:
{chr(10).join(matches)}
"""
open("README.md","w",encoding="utf-8").write(content)
print("README yaradıldı")