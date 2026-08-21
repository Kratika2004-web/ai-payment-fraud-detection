import streamlit as st
import requests
import pandas as pd
import os
import datetime
st.title("💳 AI Payment Fraud Detection Dashboard")

if "history" not in st.session_state:
    st.session_state["history"] = []
amount = st.number_input("Transaction Amount", min_value=1.0, max_value=10000.0, step=0.5)
transaction_type = st.selectbox("Transaction Type", ["Online", "POS", "ATM"])
location = st.selectbox("Location", ["Lucknow", "Delhi", "Mumbai"])

if st.button("Check Fraud"):
    url = "http://127.0.0.1:5000/detect_fraud"
    data = {"amount": amount, "transaction_type": transaction_type, "location": location}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()["status"]
        record = {"Amount": amount, "Type": transaction_type, "Location": location, "Result": result}
        st.session_state["history"].append(record)

        # Better styling
        if result == "Fraud":
            st.error("🚨 Fraud Detected")
        else:
            st.success("✅ Legit Transaction")

        # Save to CSV
        df = pd.DataFrame(st.session_state["history"])
        if not os.path.exists("data"):
            os.makedirs("data")
        df.to_csv("data/transaction_history.csv", index=False)
    else:
        st.error("API request failed")
if st.session_state["history"]:
    st.subheader("Transaction History")
    df = pd.DataFrame(st.session_state["history"])
    st.table(df)
    # Fraud vs Legit count
    st.subheader("Fraud vs Legit Overview")
    count_chart = df["Result"].value_counts()
    st.bar_chart(count_chart)

    # Amount distribution
    st.subheader("Transaction Amount Distribution")
    st.line_chart(df["Amount"])

    # Fraud by Transaction Type
    st.subheader("Fraud by Transaction Type")
    type_chart = df.groupby("Type")["Result"].value_counts().unstack().fillna(0)
    st.bar_chart(type_chart)

    # Fraud by Location
    st.subheader("Fraud by Location")
    location_chart = df.groupby("Location")["Result"].value_counts().unstack().fillna(0)
    st.bar_chart(location_chart)

    # Fraud Trend Over Time
    st.subheader("Fraud Percentage Over Time")
    df["FraudFlag"] = df["Result"].apply(lambda x: 1 if x == "Fraud" else 0)
    fraud_trend = df.groupby("Timestamp")["FraudFlag"].mean()
    st.line_chart(fraud_trend)


