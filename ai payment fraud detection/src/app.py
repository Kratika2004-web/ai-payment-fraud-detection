from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
with open("src/model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/detect_fraud", methods=["POST"])
def detect_fraud():
    data = request.json
    df = pd.DataFrame([data])
    df = pd.get_dummies(df)

    # Align with training features
    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0
    df = df[model.feature_names_in_]

    prediction = model.predict(df)[0]
    result = "Fraud" if prediction == -1 else "Legit"
    return jsonify({"status": result})

if __name__ == "__main__":
    app.run(debug=True)
