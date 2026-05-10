import pandas as pd

data = pd.read_csv('data/training_data.csv')

print(data)
print(data.head())
print(data.info())

x = data["text"]
y = data['label']

print('x')
print('y')