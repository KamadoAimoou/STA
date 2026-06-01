import re

import joblib
import pandas as pd


MODEL_PATH = "models/ticket_classifier.pkl"

model = joblib.load(MODEL_PATH)


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
    tokens = extract_tokens(text)

    result = {}

    for token in tokens:
        entity_type = predict_entity(token)

        if entity_type not in result:
            result[entity_type] = token

    return result


if __name__ == "__main__":
    sample_text = "Air Astana flight KC878 seat 13J gate B12 departure 10:45 from Almaty"

    entities = extract_ml_entities(sample_text)

    print(entities)