# Dummy Data Pipeline Project — Step-by-Step Build Guide

> This README documents the **exact process of building the project from scratch**, including every step, command, and code snippet.  
> It serves as a reference for recreating or understanding the pipeline.

---

## 1️⃣ Step 0: Set Up Tools and Accounts

### 0.1 Install VS Code
- Download: [https://code.visualstudio.com/](https://code.visualstudio.com/)  
- Install **Python** and **Git** extensions via the Extensions panel.

### 0.2 Install Python
- Download Python 3.11+ from [https://www.python.org/downloads/](https://www.python.org/downloads/)  
- Verify installation:

```bash
python --version
```

### 0.3 Install Required Python Libraries

Create a `requirements.txt` file:

```txt
pandas==2.1.1
numpy==1.27.0
faker==19.2.0
google-cloud-storage==3.19.0
google-cloud-bigquery==3.12.0
pytest==7.4.2
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 0.4 Create GitHub Account
- Go to [https://github.com/](https://github.com/) and sign up.
- We’ll store the project here and use GitHub Actions.

### 0.5 Set Up GCP Free Tier
- Go to [https://cloud.google.com/free](https://cloud.google.com/free)  
- Free tier includes:
  - BigQuery: 1 TB query + 10 GB storage/month  
  - Cloud Storage: 5 GB free  
  - Cloud Functions: 2M invocations/month  

---

## 1️⃣ Step 1: Create GitHub Repository

1. Click **New Repository** on GitHub  
2. Name: `dummy-data-pipeline`  
3. Public, add `.gitignore` → select Python, add README.md  
4. Clone locally:

```bash
git clone https://github.com/<username>/dummy-data-pipeline.git
cd dummy-data-pipeline
```

---

## 2️⃣ Step 2: Create Project Folder Structure

Inside the cloned repo, create:

```txt
dummy-data-pipeline/
├─ src/
│  ├─ generate_data.py
│  ├─ ingest_to_gcs.py
│  ├─ anomaly_detection.py
│  └─ load_to_bigquery.py
├─ data/
├─ tests/
├─ .github/
│  └─ workflows/
│     └─ python-ci.yml
├─ requirements.txt
└─ README.md
```

---

## 3️⃣ Step 3: Generate Dummy Data

**File:** `src/generate_data.py`  

```python
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

# Introduce anomalies
for _ in range(20):
    idx = random.randint(0, num_rows - 1)
    df.loc[idx, 'amount'] *= 10

df.to_csv("data/dummy_transactions.csv", index=False)
print("✅ Dummy data generated at data/dummy_transactions.csv")
```

**Run:**

```bash
python src/generate_data.py
```

Check the generated CSV in `data/dummy_transactions.csv`.

---

## 4️⃣ Step 4: Upload CSV to Google Cloud Storage

### 4.1 Create a GCS Bucket
- Go to GCP Console → Cloud Storage → **Create Bucket**  
- Name: `dummy-data-bucket-<yourname>`  
- Region: Multiregion (US)  
- Storage Class: Standard

### 4.2 Authentication
- Create a Service Account → generate JSON key → save as `gcp-key.json`  
- Set environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/gcp-key.json"
```

### 4.3 Upload Script
**File:** `src/ingest_to_gcs.py`

```python
from google.cloud import storage

client = storage.Client()
bucket_name = "dummy-data-bucket-<yourname>"
bucket = client.get_bucket(bucket_name)

blob = bucket.blob("dummy_transactions.csv")
blob.upload_from_filename("data/dummy_transactions.csv")

print("✅ File uploaded to GCS")
```

**Run:**

```bash
python src/ingest_to_gcs.py
```

---

## 5️⃣ Step 5: Detect Anomalies

**File:** `src/anomaly_detection.py`

```python
import pandas as pd

df = pd.read_csv("data/dummy_transactions.csv")

def detect_anomalies(df, col="amount"):
    median = df[col].median()
    mad = (df[col] - median).abs().median()
    df['anomaly'] = ((df[col] - median).abs() / mad) > 3
    return df

df = detect_anomalies(df)
df.to_csv("data/dummy_transactions_transformed.csv", index=False)

print("✅ Anomalies detected and saved at data/dummy_transactions_transformed.csv")
```

**Run:**

```bash
python src/anomaly_detection.py
```

---

## 6️⃣ Step 6: Load Data into BigQuery

**File:** `src/load_to_bigquery.py`

```python
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()
dataset_id = "dummy_data_pipeline"
table_id = "transactions"

dataset_ref = bigquery.Dataset(f"{client.project}.{dataset_id}")
dataset_ref.location = "US"
client.create_dataset(dataset_ref, exists_ok=True)

df = pd.read_csv("data/dummy_transactions_transformed.csv")
job = client.load_table_from_dataframe(df, f"{dataset_id}.{table_id}")
job.result()

print("✅ Data loaded into BigQuery")
```

**Run:**

```bash
python src/load_to_bigquery.py
```

---

## 7️⃣ Step 7: Add GitHub Actions for CI/CD

**File:** `.github/workflows/python-ci.yml`

```yaml
name: Python CI
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
```

---

## 8️⃣ Step 8: Commit & Push

```bash
git add .
git commit -m "Initial dummy data pipeline"
git push origin main
```

---

## ✅ Free Tier Notes

- Keep CSV < 5 GB, < 10,000 rows  
- BigQuery: 1 TB queries/month, 10 GB storage  
- Cloud Storage: 5 GB free  
- Cloud Functions: 2M invocations/month

---

## 🧭 Summary

You now have a **complete end-to-end data pipeline**:
- Generates dummy data
- Uploads CSV to GCS
- Detects anomalies
- Loads data into BigQuery
- Runs automated tests with GitHub Actions

---