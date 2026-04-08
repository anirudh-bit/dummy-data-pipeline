import pandas as pd

df = pd.read_csv("data/dummy_transactions.csv")

def detect_anomalies(df, col="amount"):
    median = df[col].median()
    mad = (df[col] - median).abs().median()
    df['anomaly'] = ((df[col] - median).abs() / mad) > 3
    return df

df = detect_anomalies(df)
df.to_csv("data/dummy_transactions_transformed.csv", index=False)
print("✅ Transformation complete. Anomalies detected and saved.")
