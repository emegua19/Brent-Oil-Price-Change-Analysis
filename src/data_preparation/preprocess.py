import pandas as pd
import numpy as np
import os
import csv

def load_oil_data(filepath: str) -> pd.DataFrame:
    """
    Load and preprocess Brent oil price data with robust validation and interpolation.

    Args:
        filepath (str): Path to the raw CSV file containing 'Date' and 'Price'.

    Returns:
        pd.DataFrame: Cleaned DataFrame with parsed 'Date', 'Price', and 'LogReturn'.
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")

    # Attempt multiple date formats
    date_formats = ['%d-%b-%y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
    for fmt in date_formats:
        try:
            df['Date'] = pd.to_datetime(df['Date'], format=fmt, errors='coerce')
            if df['Date'].notna().sum() > 0:
                break
        except ValueError:
            continue
    if df['Date'].isna().all():
        raise ValueError("Failed to parse 'Date' column. Check format.")

    # Sort by date, drop NaN dates
    df = df.sort_values('Date').dropna(subset=['Date']).reset_index(drop=True)

    # Validate prices
    if (df['Price'] <= 0).any():
        raise ValueError("Invalid prices found (zero or negative).")
    df = df.dropna(subset=['Price']).reset_index(drop=True)

    # Check for duplicate or missing dates
    if df['Date'].duplicated().any():
        raise ValueError("Duplicate dates found in data.")
    date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D')
    if len(date_range) != len(df):
        print(f"Warning: {len(date_range) - len(df)} missing dates detected. Interpolating...")
        # Interpolate missing dates
        df = df.set_index('Date').reindex(date_range).interpolate(method='linear').reset_index()
        df.columns = ['Date', 'Price']

    # Calculate log returns
    df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1))
    df = df.dropna().reset_index(drop=True)

    # Outlier detection and capping
    log_return_std = df['LogReturn'].std()
    outliers = df[abs(df['LogReturn']) > 5 * log_return_std]
    if not outliers.empty:
        print(f"Warning: {len(outliers)} outliers detected in LogReturn. Capping at ±5 * std.")
        df['LogReturn'] = df['LogReturn'].clip(-5 * log_return_std, 5 * log_return_std)

    return df

def save_processed_data(df: pd.DataFrame, output_path: str):
    """
    Save the processed DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame with processed data
        output_path (str): File path to save the CSV file
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ Processed data saved to: {output_path}")
    except Exception as e:
        raise Exception(f"Failed to save data: {e}")

def load_event_data(filepath: str) -> pd.DataFrame:
    """
    Load the curated geopolitical and economic event data.

    Args:
        filepath (str): Path to the events CSV file.

    Returns:
        pd.DataFrame: DataFrame containing event data sorted by date.
    """
    try:
        events = pd.read_csv(
            filepath,
            parse_dates=['Date'],
            quoting=csv.QUOTE_MINIMAL,
            encoding='utf-8'
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")

    # Validate event data
    if events['Date'].isna().any():
        raise ValueError("Invalid dates found in events.csv.")
    if events[['Event_Description', 'Event_Type']].isna().any().any():
        raise ValueError("Missing Event_Description or Event_Type values.")

    events = events.sort_values('Date').reset_index(drop=True)
    if events['Date'].duplicated().any():
        raise ValueError("Duplicate dates found in events.csv.")

    return events

def main():
    """
    Main function to preprocess oil price and event data.
    """
    # Define relative paths
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(project_root, 'data')
    raw_path = os.path.join(data_dir, 'raw', 'brent_oil_prices.csv')
    processed_path = os.path.join(data_dir, 'processed', 'brent_oil_log_returns.csv')
    events_path = os.path.join(data_dir, 'processed', 'events.csv')

    # Process oil data
    oil_df = load_oil_data(raw_path)
    save_processed_data(oil_df, processed_path)
    
    # Load and print event data
    events_df = load_event_data(events_path)
    print("Events Data (First 5 Rows):")
    print(events_df.head())

if __name__ == "__main__":
    main()