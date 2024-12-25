import sys

import cv2
import numpy as np
import pytesseract


def handle_image(image_content: bytes):
    image = None
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    assert image is not None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    text = ""
    for i in range(len(data["text"])):
        # x, y, w, h = (
        #     data["left"][i],
        #     data["top"][i],
        #     data["width"][i],
        #     data["height"][i],
        # )
        text = data["text"][i]
        if text.strip():
            text += text + " "

    # text = text.lower()
    return text


for image_path in sys.argv[1:]:

    with open(image_path, "rb") as f:
        image_data = f.read()
        print(handle_image(image_data))
