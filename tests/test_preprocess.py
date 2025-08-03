import sys
import os
import pandas as pd
import numpy as np

# Add the src/ directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_preparation.preprocess import load_oil_data, load_event_data

OIL_DATA_PATH = "data/raw/brent_oil_prices.csv"
EVENT_DATA_PATH = "data/processed/events.csv"

def test_load_oil_data_format():
    df = load_oil_data(OIL_DATA_PATH)
    
    # Check required columns
    assert "Date" in df.columns
    assert "Price" in df.columns
    assert "LogReturn" in df.columns

    # Check types
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])
    assert pd.api.types.is_float_dtype(df["Price"])
    assert pd.api.types.is_float_dtype(df["LogReturn"])

def test_log_return_calculation():
    df = load_oil_data(OIL_DATA_PATH)

    # Check log return calculation for a valid index
    idx = 1  # Use second row to avoid NaN from shift
    log_return_example = df["LogReturn"].iloc[idx]
    price_today = df["Price"].iloc[idx]
    price_yesterday = df["Price"].iloc[idx-1]
    expected_log_return = np.log(price_today / price_yesterday)
    
    assert isinstance(log_return_example, float)
    assert not pd.isna(log_return_example)
    assert np.isclose(log_return_example, expected_log_return, rtol=1e-5)

def test_load_event_data_format():
    df = load_event_data(EVENT_DATA_PATH)

    # Check required columns
    expected_cols = {"Date", "Event_Description", "Event_Type"}
    assert expected_cols.issubset(set(df.columns))

    # Check that date column is parsed
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])
    assert df.shape[0] >= 10  # At least 10 events