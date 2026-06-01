import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report




data = pd.read_csv('data/training_data.csv')



# print(data)
# print(data.head())
# print(data.info())

x = data["text"]
y = data['label']

# print('x')
# print('y')

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size = 0.2,
    random_state = 42
)

# print()

# print("TRAIN DATA:")
# print(x_train)

# print()

# print("TEST DATA:")
# print(x_test)

vectorizer = CountVectorizer()
x_train_vectors = vectorizer.fit_transform(x_train)
x_test_vectors = vectorizer.transform(x_test)

# print(x_test_vectors)
# print(x_test_vectors)

model = MultinomialNB()
model.fit(x_train_vectors, y_train)
prediction = model.predict(x_test_vectors)

print(prediction)

print("Real answer is >>> ")
print(y_test.values)

print("Model prediction")
print(prediction)

print(classification_report(y_test, prediction))