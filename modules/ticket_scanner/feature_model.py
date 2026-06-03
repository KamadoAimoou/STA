import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

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
    
data = pd.read_csv('data/training_data.csv')

sample = data["text"].iloc[0]

features = extract_features(sample)
print("Text: ", sample)
print("Features: ", features)


features_df = data["text"].apply(extract_features).apply(pd.Series)
print()
print("Feature table ")

print(features_df.head())

print("Shape")
print(features_df.shape)

X = features_df
y = data["label"]
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)

model.fit(x_train, y_train)
predictions = model.predict(x_test)

print()
print("Real Answer")
print(y_test.values)

print()
print("MODEL PREDICTIONS:")
print(predictions)

print()
print("CLASSIFICATION REPORT:")
print(classification_report(y_test, predictions))

joblib.dump(model, "models/ticket_classifier.pkl")
print()
print("Model saved to models/ticket classifier.pkl")