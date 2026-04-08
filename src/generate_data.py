import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()
num_rows = 5000

data = {
    "customer_id": [f"C{str(i).zfill(4)}" for i in range(num_rows)],
    "transaction_date": [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)],
    "product_category": [random.choice(['Electronics', 'Groceries', 'Apparel', 'Books']) for _ in range(num_rows)],
    "amount": [round(np.random.exponential(scale=50), 2) for _ in range(num_rows)],
    "city": [random.choice(['Belfast', 'London', 'Manchester', 'Glasgow']) for _ in range(num_rows)],
    "payment_type": [random.choice(['Card', 'Cash', 'Online']) for _ in range(num_rows)]
}

df = pd.DataFrame(data)

# Add some anomalies
for _ in range(20):
    idx = random.randint(0, num_rows - 1)
    df.loc[idx, 'amount'] *= 10

df.to_csv("data/dummy_transactions.csv", index=False)
print("✅ Dummy data generated and saved to data/dummy_transactions.csv")
