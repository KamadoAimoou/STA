import joblib
import pandas as pd


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


model = joblib.load("models/ticket_classifier.pkl")

sample = "13J"

features = extract_features(sample)

features_df = pd.DataFrame([features])

prediction = model.predict(features_df)

print("Text:", sample)
print("Prediction:", prediction[0])