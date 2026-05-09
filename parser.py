import os
import re

import pytesseract

from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

os.environ["TESSDATA_PREFIX"] = (
    r"C:\Program Files\Tesseract-OCR\tessdata"
)


def preprocess_image(image_path):

    image = Image.open(image_path)

    image = image.convert("L")

    enhancer = ImageEnhance.Contrast(image)

    image = enhancer.enhance(2)

    image = image.filter(ImageFilter.SHARPEN)

    return image


def clean_text(text):

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_text(image_path):

    processed_image = preprocess_image(image_path)

    text = pytesseract.image_to_string(
        processed_image,
        lang="eng+rus"
    )

    cleaned_text = clean_text(text)

    return cleaned_text