import requests
from datetime import datetime
url="https://www.forebet.com/en/football-tips-and-predictions-for-today"
h={"User-Agent":"Mozilla/5.0"}
t=requests.get(url,headers=h,timeout=30).text
open("README.md","w",encoding="utf-8).write(f"#Proqnoz{datetime.now()}\n\n{t[:2000]}")
