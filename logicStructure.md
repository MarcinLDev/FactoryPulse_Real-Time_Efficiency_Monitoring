FactoryPulse_Real-Time_Efficiency_Monitoring/
│
├── 01_raw_data/                       # Raw manufacturing module data (CSV files)
│   ├── Storagemodule.csv
│   ├── Deliverymodule.csv
│   └── [other *.csv modules]
│
├── 02_notebooks/                     # Jupyter Notebooks: EDA, feature engineering, model experiments
│   └── 02_01_DataCleaning_FeatureEngineering_modelML.ipynb
│
├── 03_model/                         # Trained models and exported pipelines
│   └── isolation_forest_model.pkl
│
├── 04_scripts/                       # Clean production-ready Python scripts
│   └── 02_01_IsolationForestDetectedAnomaly.py
│
├── 05_outputs/                       # CSV files with predictions and aggregated KPI outputs
│   ├── predicted_anomalies.csv
│   └── anomaly_kpi.csv
│
├── 06_bi_dashboard/                  # Power BI dashboards or Excel visualization sources
│   └── [e.g. PowerBI_dashboard.pbix]
│
├── logicStructure.md                # Detailed description of project logic, pipeline flow, and reasoning
├── README.md                        # Main project overview and instructions
└── requirements.txt                 # List of Python dependencies for easy environment setup
