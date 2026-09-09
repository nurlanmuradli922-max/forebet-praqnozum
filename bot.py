import json
import pytz
from datetime import datetime
import os

# Fayl adları
GAMES_FILE = "games.json"

final_games = []
status = ""

# Köhnə oyunları yoxla
try:
    if os.path.exists(GAMES_FILE):
        with open(GAMES_FILE, "r", encoding="utf-8") as f:
            old_data = json.load(f)
            if old_data:
                final_games = old_data
                status = "⚠️ Forebet müvəqqəti blokda idi - köhnə oyunlar göstərilir"
            else:
                status = "Hal-hazırda oyunlar yüklənmədi, növbəti saatda yenidən cəhd edəcək - Forebet müvəqqəti blokdadır"
    else:
        final_games = []
        status = "Hal-hazırda oyunlar yüklənmədi, növbəti saatda yenidən cəhd edəcək - Forebet müvəqqəti blokdadır"
except Exception as e:
    final_games = []
    status = f"Hal-hazırda oyunlar yüklənmədi, növbəti saatda yenidən cəhd edəcək - Forebet müvəqqəti blokdadır"

# Əgər heç status yoxdursa
if not status:
    status = "Hal-hazırda oyunlar yüklənmədi, növbəti saatda yenidən cəhd edəcək - Forebet müvəqqəti blokdadır"

# README yaz
now = datetime.now(pytz.timezone("Asia/Baku")).strftime("%d.%m.%Y %H:%M")
text = f"# ⚽ Futbol Proqnozları - {now}\n\n**Avtomatik yenilənir (hər saat)**\n\n### Bugünkü oyunlar:\n\n{status}\n\n"
for g in final_games:
    text += f"- {g}\n"

text += f"\n---\nSon yenilənmə: {now} Baku vaxtı\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(text)

print("README.md yeniləndi")