# FactoryPulse: Real-Time Efficiency Monitoring (Storage Module)

This project focuses on detecting and analyzing inefficiencies and anomalies in a storage module operating as part of a manufacturing line.

The solution combines data analysis, feature engineering, anomaly detection using Machine Learning, and visualization with KPI dashboards.

---

## Objective

Automatically detect abnormal behavior in the storage system using real production signal data and present key performance insights to support factory efficiency improvements.

---

## Dataset

- Source: Real-world smart factory environment (SmartFactoryOWL, Fraunhofer IOSB-INA)
- Type: Time-series data of binary signals from sensors and actuators
- File: `Storagemodule.csv`  
- Examples of signals:
  - `FunnelBlocked.I_xSignal`: whether the funnel is blocked
  - `StorageSiloFull.I_xSignal`: silo full indicator
  - `Aspirator.O_xOn`: aspirator actuator on/off
  - `MuscleTrigger.xOn`: pneumatic system internal trigger
  - ...

---

## Steps and Methodology

### 1. Exploratory Data Analysis (EDA)
- Analyze distributions of binary signals
- Visualize operating cycles, idle times, system states
- Identify suspicious activity (e.g. unusual time intervals, inactive periods)

### 2. Feature Engineering
- `DeltaTime`: duration between signal records
- `ActiveSignals`: number of signals triggered per row
- `IsIdle`: system inactive flag
- `IsTimingOutlier`: flag based on IQR method (unusual timing)
- Timestamp resampling to minute/hour for KPIs

### 3. Machine Learning – Anomaly Detection
- **Goal**: Build an unsupervised model to detect abnormal operational behavior
- Model used: `IsolationForest`
  - Ideal for unlabeled, high-dimensional, time-based data
- Features used: operational status, timing gaps, system triggers
- Output: `Anomaly` column (0 = normal, 1 = anomaly)

> If you have labels, you could use classification (Random Forest, XGBoost).  
> If not (as here), unsupervised detection is the best fit.

### 4. Power BI – KPI Dashboard
The output files (`predicted_anomalies.csv`, `anomaly_kpi.csv`) are used in a Power BI dashboard presenting:
- Average idle time per day
- Number of operations per hour
- Error/anomaly rate per shift
- Activity trend heatmaps

---

## 📁 Project Structure (clickable)

- [`01_raw_data/`](./01_raw_data/) – Raw CSV files (sensor readings from modules)
- [`02_notebooks/`](./02_notebooks/) – Notebooks with EDA and ML workflow  
  - [`02_01_DataCleaning_FeatureEngineering_modelML.ipynb`](./02_notebooks/02_01_DataCleaning_FeatureEngineering_modelML.ipynb)
- [`03_ExportResults_notebooks/`](./03_model/) – Exported trained model
- [`04_production_Scripts/`](./04_scripts/) – Python scripts for production  
  - [`02_01_IsolationForestDetectedAnomaly.py`](./04_scripts/02_01_IsolationForestDetectedAnomaly.py)
- [`05_production_Scripts_Output/`](./05_outputs/) – Output CSVs  
  - [`predicted_anomalies.csv`](./05_outputs/predicted_anomalies.csv)  
  - [`anomaly_kpi.csv`](./05_outputs/anomaly_kpi.csv)
- [`06_BI_Dashboards/`](./06_bi_dashboard/) – (Optional) Power BI dashboard

