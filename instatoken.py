import os
import random
import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
import cloudinary
import cloudinary.uploader
import time

# Cloudinary config (deine Daten)
cloudinary.config(
    cloud_name="dplxennym",
    api_key="528736563868917",
    api_secret="wNbvGlcuONOztNcg3gOVGAtK0LA"
)

# Instagram
INSTAGRAM_USER_ID = "17841475424497360"  # deine Instagram Business User ID
ACCESS_TOKEN = "EAFUmrYmQSVUBPJ3WH2eZBtZAZBMWN0lU8KaZAmr1yEZAVRUxVvBsZBEvffr13dT6hzSEwNUJwZAyV2112ZBvdNCRwp3iddQNd0wYopY2rcAWgBwsDY7cSrKgoAYk3puzjTl9fkRw8FsR177i0JGME1PePCALcQFrVUHhl2yS8i6wfMB333xCIrWhwDI62j6P8CkuidlXeS5yA0NbAYEWVAxDFp332mPN7IZCZCvQZDZD"
CAPTION = "Can you solve this? #math #mathtest #iqtest #braintest"

OUTPUT_FOLDER = "daily_tiktoks"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_equation():
    x = random.randint(1, 9)
    m = random.randint(1, 9)
    b = random.randint(1, 9)
    y = m * x + b
    return f"{m}x + {b} = {y}"

def create_math_image():
    base = Image.open("MATH TEST.png").convert("RGBA")
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype("/home/zapbrain/math_bot/arialbd.ttf", 140)  # fettes Arial

    equation = generate_equation()
    image_width = base.width

    bbox = draw.textbbox((0, 0), equation, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (image_width - text_width) // 2
    text_y = 460  # fixierte y-Koordinate

    draw.text((text_x, text_y), equation, font=font, fill="black")

    filename = f"{OUTPUT_FOLDER}/{datetime.date.today()}_equation.png"
    base.save(filename)
    print(f"Bild gespeichert: {filename}")
    return filename

def upload_to_cloudinary(image_path):
    result = cloudinary.uploader.upload(image_path)
    url = result['secure_url']
    print(f"Bild hochgeladen: {url}")
    return url

def post_to_instagram(image_url):
    # 1. Container erstellen mit Bild-URL und Caption
    url = f"https://graph.facebook.com/v16.0/{INSTAGRAM_USER_ID}/media"
    params = {
        "image_url": image_url,
        "caption": CAPTION,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, params=params)
    res.raise_for_status()
    container_id = res.json()["id"]
    print(f"Container-ID erhalten: {container_id}")

    # 2. Container veröffentlichen
    publish_url = f"https://graph.facebook.com/v16.0/{INSTAGRAM_USER_ID}/media_publish"
    publish_params = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    }
    # Instagram braucht manchmal paar Sekunden bis Container bereit ist
    time.sleep(3)

    res2 = requests.post(publish_url, params=publish_params)
    res2.raise_for_status()
    print("Bild erfolgreich auf Instagram gepostet.")
    return res2.json()

def main():
    image_path = create_math_image()
    image_url = upload_to_cloudinary(image_path)
    post_to_instagram(image_url)

if __name__ == "__main__":
    main()
