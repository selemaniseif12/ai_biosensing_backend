import pandas as pd

df = pd.read_csv("app/ml/simulation_training_data.csv")
print("COLUMNS:", df.columns.tolist())
print(df.head())
