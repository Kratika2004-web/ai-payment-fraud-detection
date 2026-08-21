import requests

url = "http://127.0.0.1:5000/detect_fraud"
data = {"amount": 4500}

response = requests.post(url, json=data)
print(response.json())
