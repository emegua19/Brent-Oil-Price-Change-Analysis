# src/data_preparation/preprocess.py

import pandas as pd
import numpy as np
import os
import csv

def load_oil_data(filepath: str) -> pd.DataFrame:
    """
    Load and preprocess Brent oil price data.
    
    Parameters:
        filepath (str): Path to the raw CSV file containing 'Date' and 'Price'.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with parsed 'Date', 'Price', and 'LogReturn'.
    """
    df = pd.read_csv(filepath)
    
    # Convert 'Date' to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    df = df.sort_values('Date').dropna(subset=['Date']).reset_index(drop=True)
    
    # Calculate log returns
    df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1))
    df = df.dropna().reset_index(drop=True)
    
    return df

def save_processed_data(df: pd.DataFrame, output_path: str):
    """
    Save the processed DataFrame to a CSV file.
    
    Parameters:
        df (pd.DataFrame): DataFrame with processed data
        output_path (str): File path to save the CSV file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Processed data saved to: {output_path}")

def load_event_data(filepath: str) -> pd.DataFrame:
    """
    Load the curated geopolitical and economic event data.
    
    Parameters:
        filepath (str): Path to the events CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing event data sorted by date.
    """
    events = pd.read_csv(
        filepath,
        parse_dates=['Date'],
        quoting=csv.QUOTE_MINIMAL,
        encoding='utf-8'
    )
    events = events.sort_values('Date').reset_index(drop=True)
    return events

# Run directly for quick testing
if __name__ == "__main__":
    oil_df = load_oil_data("data/raw/brent_oil_prices.csv")
    save_processed_data(oil_df, "data/processed/brent_oil_log_returns.csv")
    
    events_df = load_event_data("data/processed/events.csv")
    print(events_df.head())
