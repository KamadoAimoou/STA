import re

import joblib
import pandas as pd


MODEL_PATH = "models/ticket_classifier.pkl"

model = joblib.load(MODEL_PATH)

AIRLINES = [
    "Air Astana",
    "FlyArystan",
    "Turkish Airlines",
    "Qatar Airways",
    "Emirates",
    "Lufthansa",
    "SCAT",
]

CITIES = [
    "ATYRAU",
    "ALMATY",
    "ASTANA",
    "AKTAU",
    "SHYMKENT",
    "ISTANBUL",
    "DOHA",
    "DUBAI",
]


def extract_features(value):
    value = str(value)

    return {
        "length": len(value),
        "has_digits": any(char.isdigit() for char in value),
        "has_letter": any(char.isalpha() for char in value),
        "starts_with_digit": value[0].isdigit(),
        "starts_with_letter": value[0].isalpha(),
        "end_with_digit": value[-1].isdigit(),
        "end_with_letter": value[-1].isalpha(),
        "has_collon": ":" in value,
        "word_count": len(value.split()),
        "has_space": " " in value,
    }
    
def format_ml_entities(entities):
    return (
                "✈️ Ticket Summary\n\n"
        f"Airline: {entities.get('airline', 'Not found')}\n"
        f"Flight number: {entities.get('flight_number', 'Not found')}\n"
        f"Seat: {entities.get('seat', 'Not found')}\n"
        f"Gate: {entities.get('gate', 'Not found')}\n"
        f"Time: {entities.get('time', 'Not found')}\n"
        f"City: {entities.get('city', 'Not found')}\n\n"
        "✅ Advice:\n"
        "Check your gate and boarding time on the airport screen."
    )


def predict_entity(value):
    features = extract_features(value)

    features_df = pd.DataFrame([features])

    prediction = model.predict(features_df)

    return prediction[0]


def extract_tokens(text):
    tokens = re.findall(
        r"[A-Z]{2}\d{3,4}|[0-9]{1,2}[A-Z]|[A-Z]\d{1,3}|\d{1,2}:\d{2}|[A-Za-z]+(?:\s[A-Za-z]+)?",
        text
    )

    return tokens


def extract_ml_entities(text):
    result = {}

    upper_text = text.upper()

    for airline in AIRLINES:
        if airline.upper() in upper_text:
            result["airline"] = airline
            break

    for city in CITIES:
        if city in upper_text:
            if "city" not in result:
                result["city"] = city.title()

    flight_match = re.search(
        r"\b([A-Z]{2}\s?\d{3,4})\b",
        text
    )

    if flight_match:
        result["flight_number"] = flight_match.group(1)

    seat_match = re.search(
        r"Seat[:\s]*([0-9]{1,2}[A-Z])",
        text,
        re.IGNORECASE
    )

    if seat_match:
        result["seat"] = seat_match.group(1)

    time_match = re.search(
        r"\b([0-2]?\d:[0-5]\d)\b",
        text
    )

    if time_match:
        result["time"] = time_match.group(1)

    gate_match = re.search(
        r"Gate[:\s]*([A-Z]?\d{1,3})",
        text,
        re.IGNORECASE
    )

    if gate_match:
        result["gate"] = gate_match.group(1)

    return result

if __name__ == "__main__":
    sample_text = "Air Astana flight KC878 seat 13J gate B12 departure 10:45 from Almaty"

    entities = extract_ml_entities(sample_text)

    print(entities)
