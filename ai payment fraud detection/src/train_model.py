import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle

# Load dataset
df = pd.read_csv("data/synthetic_transactions.csv")

# Features
X = df[["amount"]]

# Train model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

# Save model
with open("src/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.pkl")
