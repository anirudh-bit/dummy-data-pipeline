from google.cloud import storage

client = storage.Client()
bucket_name = "dummy-data-storage-am"

bucket = client.get_bucket(bucket_name)
blob = bucket.blob("dummy_transactions.csv")
blob.upload_from_filename("data/dummy_transactions.csv")

print("✅ File uploaded to GCS successfully!")
