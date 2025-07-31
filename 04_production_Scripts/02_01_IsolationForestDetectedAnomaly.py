import pandas as pd 
from sklearn.ensemble import IsolationForest

# Load the storage module data

path_storagemodele = '../airflow/FactoryPulse_Real-Time_Efficiency_Monitoring/01_RawData/Storagemodule.csv'
df_storage = pd.read_csv(path_storagemodele, sep=',')

# Convert Timestamp to datetime and sort
df_storage['Timestamp'] = pd.to_datetime(df_storage['Timestamp'], unit='ms')
df_storage.sort_values(by='Timestamp', inplace=True, ascending=True)


# Select binary columns (except Timestamp)  
# Count the number of active signals (whether something is working)
# Create a flag: 1 = idle (meaning nothing is working), 0 = activity
binary_cols = df_storage.columns.drop('Timestamp')
df_storage['ActiveSignals'] = df_storage[binary_cols].sum(axis=1)
df_storage['IsIdle'] = (df_storage['ActiveSignals'] == 0).astype(int)
df_storage['DeltaTime'] = df_storage['Timestamp'].diff().dt.total_seconds()

# Check for outliers in DeltaTime using IQR method
Q1 = df_storage['DeltaTime'].quantile(0.25)
Q3 = df_storage['DeltaTime'].quantile(0.75)
IQR = Q3 - Q1

# Identify outliers
# Outliers are defined as values below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR
outliers = df_storage[(df_storage['DeltaTime'] < (Q1 - 1.5 * IQR)) | (df_storage['DeltaTime'] > (Q3 + 1.5 * IQR))]
print(f"Number of outliers in DeltaTime: {len(outliers)}")

# Create a flag for timing outliers
df_storage['IsTimingOutlier'] = df_storage.index.isin(outliers.index).astype(int)

# Group by minute to analyze anomalies
df_storage['Minute'] = df_storage['Timestamp'].dt.floor('T')
outliers_by_minute = df_storage.groupby('Minute')['IsTimingOutlier'].mean().reset_index()

df_storage['DeltaTime'] = df_storage['DeltaTime'].fillna(0)

# Prepare features for Isolation Forest model
features = [
    'ActiveSignals',
    'DeltaTime',
    'IsIdle',
    'IsTimingOutlier',
    'Aspirator.O_xOn',
    'MuscleTrigger.O_xOn',
    'MuscleTrigger.xOn'
]
# Select features for the model
X = df_storage[features].copy()
X = X.fillna(0)

# Train Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X)

# Predict anomalies
df_storage['Anomaly'] = model.predict(X)
df_storage['Anomaly'] = df_storage['Anomaly'].map({1: 0, -1: 1})

print(df_storage['Anomaly'].value_counts())

# Group by minute to analyze anomalies
anomalies_by_minute = df_storage.groupby('Minute')['Anomaly'].mean().reset_index()

# Save the results to CSV files
df_storage.to_csv('../airflow/FactoryPulse_Real-Time_Efficiency_Monitoring/05_production_Scripts_Output/predicted_anomalies.csv', index=False)
anomalies_by_minute.to_csv('../airflow/FactoryPulse_Real-Time_Efficiency_Monitoring/05_production_Scripts_Output/anomaly_kpi.csv', index=False)
