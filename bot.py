import json
import os
import pytz
from datetime import datetime

fg = []
st = "Blokdadir"

try:
    if os.path.exists("games.json"):
        with open(
            "games.json",
            "r",
            encoding="utf-8"
        ) as f:
            fg = json.load(f)
except:
    pass

tz = pytz.timezone(
    "Asia/Baku"
)

now = datetime.now(tz)
now = now.strftime(
    "%d.%m %H:%M"
)

text = f"# Futbol - {now}\n\n"
text += f"{st}\n\n"

for g in fg:
    text += f"- {g}\n"

text += f"\n---\nSon: {now}\n"

with open(
    "README.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(text)

print("OK")