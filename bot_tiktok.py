import os
import random
import datetime
from PIL import Image, ImageDraw, ImageFont
import schedule
import time
import requests

# Telegram Einstellungen
BOT_TOKEN = "7714845517:AAEBEsR455rGe-md4Vz3cipNGeGOoHUBY-Q"
CHAT_ID = 6402353772  # z.B. 123456789 als int

OUTPUT_FOLDER = "daily_tiktoks"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_equation():
    x = random.randint(1, 10)
    m = random.randint(1, 10)
    b = random.randint(1, 10)
    y = m * x + b
    return f"{m}x + {b} = {y}"

def create_math_image():
    base = Image.open("canva_template.png").convert("RGBA")
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype("arial.ttf", 40)

    equation = generate_equation()
    text_position = (54, 220)  # anpassen

    draw.text(text_position, equation, font=font, fill="black")

    filename = f"{OUTPUT_FOLDER}/{datetime.date.today()}_equation.png"
    base.save(filename)
    print(f"Bild gespeichert: {filename}")
    return filename

def send_telegram_photo(filepath):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(filepath, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID}
        r = requests.post(url, files=files, data=data)
    if r.status_code == 200:
        print("Bild erfolgreich via Telegram gesendet.")
    else:
        print("Fehler beim Senden:", r.text)

def job():
    filepath = create_math_image()
    send_telegram_photo(filepath)

# Täglich um 21:13 Uhr
schedule.every().day.at("21:52").do(job)

print("Bot läuft... (Strg+C zum Stoppen)")
while True:
    schedule.run_pending()
    time.sleep(5)
