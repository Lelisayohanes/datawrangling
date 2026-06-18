# Sales Data - Processed

## Purpose
This directory contains cleaned and feature-engineered data derived from raw transportation sector online sales records, suitable for analysis and visualization.


## Raw Data Context
For full details on raw data, see `data/sales-data/README.md`.

### Raw Data Summary
- **Purpose**: Vehicle registration/sales records from the transportation sector
- **Source**: Two CSV files covering November and December 2022
- **Contents**: Individual vehicle registration records
- **Structure**: 12 columns including:
  - Vehicle details (fuel type, class, make year, seat capacity)
  - Insurance information
  - Temporal details (registration dates)
  - Office location codes


## Processed Data

### Purpose
To provide clean, consistent, and enriched data for analysis and visualization.

### Transformations Applied
1. **Data Integration**: Merged November and December 2022 datasets
2. **Text Standardization**: Cleaned and standardized text fields (uppercase, stripped whitespace)
3. **Fuel Type Normalization**: Standardized inconsistent fuel type labels
4. **Data Type Conversion**: Converted date columns to proper datetime format
5. **Missing Value Handling**:
   - Filled missing fuel type values with "UNKNOWN"
   - Removed records with missing insurance validity dates
6. **Deduplication**: Removed duplicate records
7. **Feature Engineering**: Created new analytical features:
   - `registration_month`: Month of registration
   - `registration_year`: Year of registration
   - `vehicle_age`: Vehicle age at registration (years)
   - `insurance_duration_days`: Days from registration to insurance expiry
   - `expiry_month`: Month of insurance expiry

### Output Structure
- `vehicle_clean_master.csv`: Cleaned, merged raw data
- `vehicle_features.csv`: Cleaned data with engineered features
- `summary_stats/`: Aggregated statistics
  - `fuel_distribution.csv`: Fuel type counts
  - `vehicle_class_distribution.csv`: Vehicle class counts
  - `monthly_registrations.csv`: Registrations by month
  - `insurance_duration_by_class.csv`: Insurance duration stats by vehicle class
  - `fuel_type_mappings.csv`: Fuel type normalization mapping
  - `data_quality_report.csv`: Missing values before/after cleaning
- `plots/`: Visualizations
  - `monthly_registrations.png`: Registrations by month
  - `fuel_type_distribution.png`: Top 10 fuel types
  - `vehicle_class_distribution.png`: Top 10 vehicle classes
  - `insurance_duration_histogram.png`: Insurance duration distribution
- `DATA_VERSION.md`: Version information

### Usage
```python
import pandas as pd

# Load processed data with features
df = pd.read_csv(
    "vehicle_features.csv",
    parse_dates=["makeYear", "insuranceValidity", "fromdate", "todate"]
)
```


## Data Quality
- Total records after cleaning: 152,865
- Date range: 2022-11-01 to 2022-12-01
- See `summary_stats/data_quality_report.csv` for missing value details
