import pandas as pd
import os

def load_raw_data():
    """Load raw sales data from CSV files."""
    df_nov = pd.read_csv("data/sales-data/ts_transport_online_sales_01_11_2022to30_11_2022_0.csv")
    df_dec = pd.read_csv("data/sales-data/ts_transport_online_sales_01_12_2022to31_12_2022_0.csv")
    return df_nov, df_dec

def clean_text_columns(df):
    """Clean text columns by stripping whitespace and converting to uppercase."""
    text_columns = [
        "fuel",
        "vehicleClass",
        "category",
        "OfficeCd",
        "secondVehicle",
        "tempRegistrationNumber"
    ]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.strip().str.upper()
    return df

def standardize_fuel_types(df):
    """Standardize inconsistent fuel type labels."""
    fuel_mapping = {
        "PETROL CNG": "CNG PETROL",
        "+AC0-1": "UNKNOWN"
    }
    if "fuel" in df.columns:
        df["fuel"] = df["fuel"].replace(fuel_mapping)
    return df

def convert_datetime_columns(df):
    """Convert date columns to datetime format."""
    date_columns = [
        "makeYear",
        "insuranceValidity",
        "fromdate",
        "todate"
    ]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def handle_missing_values(df):
    """Handle missing values in the dataset."""
    if "fuel" in df.columns:
        df["fuel"] = df["fuel"].fillna("UNKNOWN")
    if "insuranceValidity" in df.columns:
        df = df.dropna(subset=["insuranceValidity"])
    return df

def add_derived_features(df):
    """Add derived features from existing data."""
    if "fromdate" in df.columns:
        df["registration_month"] = df["fromdate"].dt.month
        df["registration_year"] = df["fromdate"].dt.year
    if "fromdate" in df.columns and "makeYear" in df.columns:
        df["vehicle_age"] = df["fromdate"].dt.year - df["makeYear"].dt.year
    if "insuranceValidity" in df.columns and "fromdate" in df.columns:
        df["insurance_duration_days"] = (df["insuranceValidity"] - df["fromdate"]).dt.days
    if "insuranceValidity" in df.columns:
        df["expiry_month"] = df["insuranceValidity"].dt.month
    return df

def clean_and_process_data():
    """Full data cleaning and processing pipeline."""
    # Load data
    df_nov, df_dec = load_raw_data()
    
    # Clean individual datasets
    df_nov = clean_text_columns(df_nov)
    df_nov = standardize_fuel_types(df_nov)
    df_nov = convert_datetime_columns(df_nov)
    
    df_dec = clean_text_columns(df_dec)
    df_dec = standardize_fuel_types(df_dec)
    df_dec = convert_datetime_columns(df_dec)
    
    # Merge datasets
    merged_df = pd.concat([df_nov, df_dec], ignore_index=True)
    
    # Remove duplicates
    merged_df = merged_df.drop_duplicates().reset_index(drop=True)
    
    # Handle missing values
    merged_df = handle_missing_values(merged_df)
    
    # Add derived features
    merged_df = add_derived_features(merged_df)
    
    return merged_df

if __name__ == "__main__":
    print("Starting data cleaning and processing...")
    processed_df = clean_and_process_data()
    
    # Save processed data
    os.makedirs("processed_data/sales-data", exist_ok=True)
    processed_df.to_csv("processed_data/sales-data/vehicle_features.csv", index=False)
    print("✅ Data processing complete! Processed data saved.")
