import cv2
import requests, os
import numpy as np
import pytesseract
from flask import Flask, request
from googletrans import Translator as APITranslator
from translate import Translator as ScrapTranslator
import json
from waitress import serve

app = Flask(__name__)


scrapTranslatorClient = ScrapTranslator(to_lang="fa")
APITranslatorClient = APITranslator()


def translate(english_text: str):
    return


def handle_image(image_content: bytes):
    image = None
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    assert image is not None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    text_to_translate = ""
    for i in range(len(data["text"])):
        x, y, w, h = (
            data["left"][i],
            data["top"][i],
            data["width"][i],
            data["height"][i],
        )
        text = data["text"][i]
        if text.strip():
            text_to_translate += text + " "

    text_to_translate = text_to_translate.lower()
    translated_text1 = APITranslatorClient.translate(text_to_translate, dest="fa").text
    translated_text2 = scrapTranslatorClient.translate(text_to_translate)

    return translated_text1, translated_text2


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


@app.route("/", methods=["POST"])
def get_translate():
    if "meme" not in request.files:
        return "No file found", 400

    file = request.files["meme"]
    data = file.read()

    translates = handle_image(data)
    return json.dumps(translates)


if __name__ == "__main__":

    print("Running...")
    serve(
        app,
        host="0.0.0.0",
        port=4040,
        threads=4,
        connection_limit=100,
        channel_timeout=120,
        asyncore_use_poll=1,
    )
