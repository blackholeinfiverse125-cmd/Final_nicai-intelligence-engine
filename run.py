import os
print(os.getcwd())
print(os.listdir())

import pandas as pd

df = pd.read_csv("clean_weather.csv")

print(df.head())
print(df.columns)