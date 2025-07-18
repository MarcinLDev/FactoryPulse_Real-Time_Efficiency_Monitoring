        +-----------------------+
        |     Raw Data (CSV)   |
        |  StorageModule.csv   |
        +----------+------------+
                   |
                   v
        +-----------------------+
        |   Data Preprocessing  |
        |   - Timestamp parsing |
        |   - Status encoding   |
        |   -Feature engineering| 
        |(cycle time, idle time)|
        +----------+------------+
                   |
                   v
        +------------------------+
        |   Exploratory Analysis |
        |   - Status trends      |
        |   - Time-series charts |
        |   - Downtime detection |
        +----------+-------------+
                   |
                   v
        +------------------------+
        |     ML/Anomaly Model   |
        |   - Isolation Forest   |
        |   - Clustering/Stats   |
        +----------+-------------+
                   |
                   v
        +------------------------+
        |      Export Results    |
        |   - ML predictions     |
        |   - KPI metrics (CSV)  |
        +----------+-------------+
                   |
                   v
        +------------------------+
        |       Power BI         |
        |   - Real-time KPI Dash |
        |   - Heatmaps/Trends    |
        +------------------------+
