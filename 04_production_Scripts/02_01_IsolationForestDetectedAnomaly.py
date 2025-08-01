import pandas as pd
import joblib

def preprocess_storage_data(df: pd.DataFrame) -> pd.DataFrame:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df = df.sort_values('Timestamp').reset_index(drop=True)
    
    # Wypełnij DeltaTime
    df['DeltaTime'] = df['Timestamp'].diff().dt.total_seconds().fillna(0)

    # Aktywne sygnały
    binary_cols = df.columns.drop('Timestamp')
    df['ActiveSignals'] = df[binary_cols].sum(axis=1)

    # Idle flag
    df['IsIdle'] = (df['ActiveSignals'] == 0).astype(int)

    # Outlier detection (IQR logic)
    Q1 = df['DeltaTime'].quantile(0.25)
    Q3 = df['DeltaTime'].quantile(0.75)
    IQR = Q3 - Q1
    df['IsTimingOutlier'] = ((df['DeltaTime'] < Q1 - 1.5 * IQR) |
                             (df['DeltaTime'] > Q3 + 1.5 * IQR)).astype(int)
    
    return df

# ====== PRODUCTION SCRIPT ======
# 1. Load data
df = pd.read_csv('../airflow/FactoryPulse_Real-Time_Efficiency_Monitoring/01_RawData/Storagemodule.csv')

# 2. Transform data exactly like in training
df = preprocess_storage_data(df)

# 3. Prepare feature matrix
features = [
    'ActiveSignals', 'DeltaTime', 'IsIdle', 'IsTimingOutlier',
    'Aspirator.O_xOn', 'MuscleTrigger.O_xOn', 'MuscleTrigger.xOn'
]
X = df[features].fillna(0)

# 4. Load trained model
model = joblib.load('../airflow/FactoryPulse_Real-Time_Efficiency_Monitoring/03_ExportResults_notebooks/isolation_forest_model.pkl')

# 5. Predict
df['Anomaly'] = model.predict(X)
df['Anomaly'] = df['Anomaly'].map({1: 0, -1: 1})




# Save the results to CSV files
df.to_csv('../airflow/FactoryPulse_Real-Time_Efficiency_Monitoring/05_production_Scripts_Output/predicted_anomalies.csv', index=False)
# anomalies_by_minute.to_csv('../airflow/FactoryPulse_Real-Time_Efficiency_Monitoring/05_production_Scripts_Output/anomaly_kpi.csv', index=False)
