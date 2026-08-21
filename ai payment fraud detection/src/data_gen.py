import pandas as pd
import random
from faker import Faker

# Initialize Faker for fake data
fake = Faker()
rows = []

# Generate 500 synthetic transactions
for i in range(500):
    user_id = fake.uuid4()
    amount = round(random.uniform(10, 5000), 2)
    device_id = fake.uuid4()
    ip = fake.ipv4()
    location = fake.city()
    timestamp = fake.date_time_this_year()
    
    # Fraud injection rules
    fraud_flag = 0
    if amount > 4000:  # unusually high amount
        fraud_flag = 1
    if random.random() < 0.02:  # 2% chance random fraud
        fraud_flag = 1
    
    rows.append([i, user_id, amount, device_id, ip, location, timestamp, fraud_flag])

# Save dataset
df = pd.DataFrame(rows, columns=[
    "transaction_id", "user_id", "amount", "device_id", "ip", "location", "timestamp", "fraud_flag"
])

df.to_csv("data/synthetic_transactions.csv", index=False)
print("✅ Dataset created: synthetic_transactions.csv")
