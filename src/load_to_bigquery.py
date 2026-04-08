from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

dataset_id = "dummy_data_pipeline"
table_id = "transactions"

# Create dataset if not already exists
dataset_ref = bigquery.Dataset(f"{client.project}.{dataset_id}")
dataset_ref.location = "US"
client.create_dataset(dataset_ref, exists_ok=True)

# Load CSV to BigQuery
df = pd.read_csv("data/dummy_transactions_transformed.csv")
job = client.load_table_from_dataframe(df, f"{dataset_id}.{table_id}")
job.result()

print("✅ Data successfully loaded into BigQuery!")
