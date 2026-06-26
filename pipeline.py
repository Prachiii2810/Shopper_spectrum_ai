import pandas as pd
import numpy as np
import pickle

print("⚙️ Step 1: Loading raw dataset into pipeline...")
df = pd.read_csv("data.csv", encoding="ISO-8859-1")

# ==========================================
# 1. DATA CLEANING
# ==========================================
print("🧼 Step 2: Running data cleaning pipeline...")
df.dropna(subset=['CustomerID', 'Description'], inplace=True)
df['CustomerID'] = df['CustomerID'].astype(int).astype(str)
df['Description'] = df['Description'].str.strip().str.upper()
df.drop_duplicates(inplace=True)

# Filter out cancellations and non-positive numbers
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Feature engineering
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

print(f"✅ Data cleaned. Rows remaining: {df.shape[0]}")

# ==========================================
# 2. RFM CUSTOMER SEGMENTATION
# ==========================================
print("📊 Step 3: Computing RFM metrics and scores...")
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',                                 
    'TotalAmount': 'sum'                                    
})
rfm.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalAmount': 'Monetary'}, inplace=True)

# Generate Quantile Ranks (1 to 4 scaling)
quantiles = rfm.quantile(q=[0.25, 0.5, 0.75]).to_dict()

def r_score(x, p, d):
    if x <= d[p][0.25]: return 4
    elif x <= d[p][0.50]: return 3
    elif x <= d[p][0.75]: return 2
    return 1

def fm_score(x, p, d):
    if x <= d[p][0.25]: return 1
    elif x <= d[p][0.50]: return 2
    elif x <= d[p][0.75]: return 3
    return 4

rfm['R'] = rfm['Recency'].apply(r_score, args=('Recency', quantiles))
rfm['F'] = rfm['Frequency'].apply(fm_score, args=('Frequency', quantiles))
rfm['M'] = rfm['Monetary'].apply(fm_score, args=('Monetary', quantiles))

# Map scores to business segments
def segment_customer(row):
    r, f, m = row['R'], row['F'], row['M']
    if r >= 3 and f >= 3 and m >= 3: return 'High Value Customer'
    elif r >= 3 and (f >= 2 or m >= 2): return 'Regular Customer'
    elif r == 2: return 'Occasional Customer'
    else: return 'At-Risk Customer'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# ==========================================
# 3. PRODUCT RECOMMENDATION ENGINE
# ==========================================
print("🛒 Step 4: Building product co-occurrence matrix...")
item_counts = df['Description'].value_counts()
popular_items = item_counts[item_counts >= 10].index
df_filtered = df[df['Description'].isin(popular_items)]

co_matrix = pd.crosstab(df_filtered['InvoiceNo'], df_filtered['Description'])
co_matrix = (co_matrix > 0).astype(int)

# Matrix multiplication to find cross-purchases
co_occurrence = co_matrix.T.dot(co_matrix)
np.fill_diagonal(co_occurrence.values, 0)

reco_map = {}
for item in co_occurrence.index:
    reco_map[item] = co_occurrence[item].sort_values(ascending=False).head(5).index.tolist()

# ==========================================
# 4. EXPORT ARTIFACTS
# ==========================================
print("💾 Step 5: Exporting artifacts to disk...")
backend_data = {
    'rfm_data': rfm[['Recency', 'Frequency', 'Monetary', 'Segment']],
    'recommendations': reco_map,
    'product_list': sorted(df['Description'].unique().tolist())
}

with open("app_data.pkl", "wb") as f:
    pickle.dump(backend_data, f)

print("🎉 Pipeline run completely successful! Saved as 'app_data.pkl'.")
