import os
os.environ["MKL_THREADING_LAYER"] = "GNU"  # Prevent MKL threading issues
import pymc as pm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arviz as az

def load_log_return_data(filepath: str) -> pd.DataFrame:
    """
    Load and preprocess Brent oil price log returns data.

    Args:
        filepath (str): Path to the CSV file containing log returns.

    Returns:
        pd.DataFrame: DataFrame with 'Date' (datetime) and 'LogReturn' (float) columns.
    """
    try:
        df = pd.read_csv(filepath, parse_dates=["Date"])
        df = df.dropna(subset=["LogReturn"])
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")

def run_change_point_model(data: pd.Series, dates: pd.Series, events_path: str, output_dir: str, num_change_points: int = 3):
    """
    Run a Bayesian change point model on Brent oil log returns and match with events.

    Args:
        data (pd.Series): Log returns series.
        dates (pd.Series): Corresponding dates.
        events_path (str): Path to events.csv.
        output_dir (str): Directory to save outputs.
        num_change_points (int): Number of change points (1 or 3).

    Returns:
        tuple: (model, trace) PyMC model and posterior trace.
    """
    # Create output directories
    os.makedirs(os.path.join(output_dir, 'figures', 'trace_plots'), exist_ok=True)
    
    # Prepare data
    n = len(data)
    data = data.values
    dates = dates.values
    
    # Load events
    try:
        events_df = pd.read_csv(events_path, parse_dates=["Date"])
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {events_path}")
    
    # Estimate data scale for priors
    data_std = np.std(data)
    
    # Bayesian change point model
    with pm.Model() as model:
        if num_change_points == 3:
            # Three change points
            tau_1 = pm.DiscreteUniform("tau_1", lower=0, upper=n//3)
            tau_2 = pm.DiscreteUniform("tau_2", lower=n//3, upper=2*n//3)
            tau_3 = pm.DiscreteUniform("tau_3", lower=2*n//3, upper=n-1)
            mu_1 = pm.Normal("mu_1", mu=0, sigma=data_std / 10)
            mu_2 = pm.Normal("mu_2", mu=0, sigma=data_std / 10)
            mu_3 = pm.Normal("mu_3", mu=0, sigma=data_std / 10)
            mu_4 = pm.Normal("mu_4", mu=0, sigma=data_std / 10)
            sigma_1 = pm.HalfNormal("sigma_1", sigma=data_std / 2)
            sigma_2 = pm.HalfNormal("sigma_2", sigma=data_std / 2)
            sigma_3 = pm.HalfNormal("sigma_3", sigma=data_std / 2)
            sigma_4 = pm.HalfNormal("sigma_4", sigma=data_std / 2)
            idx = np.arange(n)
            mu = pm.math.switch(tau_1 >= idx, mu_1, 
                    pm.math.switch(tau_2 >= idx, mu_2, 
                    pm.math.switch(tau_3 >= idx, mu_3, mu_4)))
            sigma = pm.math.switch(tau_1 >= idx, sigma_1, 
                       pm.math.switch(tau_2 >= idx, sigma_2, 
                       pm.math.switch(tau_3 >= idx, sigma_3, sigma_4)))
        else:
            # Single change point
            tau = pm.DiscreteUniform("tau", lower=0, upper=n-1)
            mu_1 = pm.Normal("mu_1", mu=0, sigma=data_std / 10)
            mu_2 = pm.Normal("mu_2", mu=0, sigma=data_std / 10)
            sigma_1 = pm.HalfNormal("sigma_1", sigma=data_std / 2)
            sigma_2 = pm.HalfNormal("sigma_2", sigma=data_std / 2)
            idx = np.arange(n)
            mu = pm.math.switch(tau >= idx, mu_1, mu_2)
            sigma = pm.math.switch(tau >= idx, sigma_1, sigma_2)
        
        # Likelihood
        returns = pm.Normal("returns", mu=mu, sigma=sigma, observed=data)
        
        # Sampling
        trace = pm.sample(draws=10000, tune=5000, chains=4, random_seed=42, return_inferencedata=True)
    
    # Check convergence
    var_names = ["tau_1", "tau_2", "tau_3", "mu_1", "mu_2", "mu_3", "mu_4", "sigma_1", "sigma_2", "sigma_3", "sigma_4"] if num_change_points == 3 else ["tau", "mu_1", "mu_2", "sigma_1", "sigma_2"]
    summary = az.summary(trace, var_names=var_names)
    r_hat = summary['r_hat'].max()
    if r_hat > 1.1:
        print(f"Warning: Model may not have converged (r_hat = {r_hat:.2f}). Check trace plots.")
    else:
        print(f"Model converged (r_hat = {r_hat:.2f}).")
    
    # Save posterior summary
    with open(os.path.join(output_dir, 'posterior_summaries.txt'), 'w') as f:
        f.write(summary.to_string())
    
    # Save trace
    trace_path = os.path.join(output_dir, 'change_point_trace.nc')
    trace.to_netcdf(trace_path)
    
    # Identify change points
    if num_change_points == 3:
        tau_1_posterior = trace.posterior['tau_1'].values.flatten()
        tau_2_posterior = trace.posterior['tau_2'].values.flatten()
        tau_3_posterior = trace.posterior['tau_3'].values.flatten()
        tau_1_mode = int(np.bincount(tau_1_posterior).argmax())
        tau_2_mode = int(np.bincount(tau_2_posterior).argmax())
        tau_3_mode = int(np.bincount(tau_3_posterior).argmax())
        change_point_dates = [pd.to_datetime(dates[tau_1_mode]), pd.to_datetime(dates[tau_2_mode]), pd.to_datetime(dates[tau_3_mode])]
        change_points_df = pd.DataFrame({'Date': change_point_dates, 'Tau_Mode': [tau_1_mode, tau_2_mode, tau_3_mode]})
    else:
        tau_posterior = trace.posterior['tau'].values.flatten()
        tau_mode = int(np.bincount(tau_posterior).argmax())
        change_point_dates = [pd.to_datetime(dates[tau_mode])]
        change_points_df = pd.DataFrame({'Date': change_point_dates, 'Tau_Mode': [tau_mode]})
    
    # Save change points
    change_points_df.to_csv(os.path.join(output_dir, 'change_points.csv'), index=False)
    
    # Plot posterior distributions
    plt.figure(figsize=(12, 8))
    az.plot_posterior(trace, var_names=var_names)
    plt.savefig(os.path.join(output_dir, 'figures', 'trace_plots', 'change_point_trace.png'))
    plt.close()
    
    # Plot log returns with change points
    plt.figure(figsize=(12, 6))
    plt.plot(dates, data, label="Log Returns", alpha=0.7)
    for cp_date in change_point_dates:
        plt.axvline(cp_date, color='r', linestyle='--', label=f'Change Point: {cp_date.strftime("%Y-%m-%d")}')
    plt.xlabel("Date")
    plt.ylabel("Log Return")
    plt.title("Brent Oil Log Returns with Detected Change Points")
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'figures', 'log_returns_change_point.png'))
    plt.close()
    
    # Associate change points with events
    events_df['Date'] = pd.to_datetime(events_df['Date'])
    matched_events = []
    for cp_date in change_point_dates:
        events_df['Date_Diff'] = abs(events_df['Date'] - cp_date)
        closest_event = events_df.loc[events_df['Date_Diff'].idxmin()]
        matched_events.append({
            'Change_Point_Date': cp_date,
            'Event_Date': closest_event['Date'],
            'Event_Description': closest_event['Event_Description'],
            'Event_Type': closest_event['Event_Type'],
            'Date_Diff_Days': closest_event['Date_Diff'].days
        })
    
    # Quantify impact
    if num_change_points == 3:
        mean_1, mean_2, mean_3, mean_4 = summary.loc['mu_1', 'mean'], summary.loc['mu_2', 'mean'], summary.loc['mu_3', 'mean'], summary.loc['mu_4', 'mean']
        impact_1 = ((mean_2 - mean_1) / abs(mean_1)) * 100 if abs(mean_1) > 1e-10 else np.nan
        impact_2 = ((mean_3 - mean_2) / abs(mean_2)) * 100 if abs(mean_2) > 1e-10 else np.nan
        impact_3 = ((mean_4 - mean_3) / abs(mean_3)) * 100 if abs(mean_3) > 1e-10 else np.nan
        matched_events[0].update({'Mean_Before': mean_1, 'Mean_After': mean_2, 'Impact_Percent': impact_1})
        matched_events[1].update({'Mean_Before': mean_2, 'Mean_After': mean_3, 'Impact_Percent': impact_2})
        matched_events[2].update({'Mean_Before': mean_3, 'Mean_After': mean_4, 'Impact_Percent': impact_3})
    else:
        mean_before = summary.loc['mu_1', 'mean']
        mean_after = summary.loc['mu_2', 'mean']
        impact_percent = ((mean_after - mean_before) / abs(mean_before)) * 100 if abs(mean_before) > 1e-10 else np.nan
        matched_events[0].update({'Mean_Before': mean_before, 'Mean_After': mean_after, 'Impact_Percent': impact_percent})
    
    # Save matched events
    matched_events_df = pd.DataFrame(matched_events)
    matched_events_df.to_csv(os.path.join(output_dir, 'matched_events.csv'), index=False)
    
    # Print results
    for i, event in enumerate(matched_events):
        print(f"Change Point {i+1} Date: {event['Change_Point_Date'].strftime('%Y-%m-%d')}")
        print(f"Closest Event: {event['Event_Description']} on {event['Event_Date'].strftime('%Y-%m-%d')}")
        print(f"Date Difference: {event['Date_Diff_Days']} days")
        print(f"Mean Log Return Before: {event['Mean_Before']:.6f}")
        print(f"Mean Log Return After: {event['Mean_After']:.6f}")
        print(f"Impact: {event['Impact_Percent']:.2f}% change in mean log return" if not np.isnan(event['Impact_Percent']) else "Impact: Not calculated (Mean_Before ≈ 0)")
    
    return model, trace

def main():
    """
    Main function to handle file inputs and run the change point model.
    """
    # Define local paths
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(project_root, 'data')
    data_path = os.path.join(data_dir, 'processed', 'brent_oil_log_returns.csv')
    events_path = os.path.join(data_dir, 'processed', 'events.csv')
    output_dir = os.path.join(project_root, 'results')
    
    # Load data
    df = load_log_return_data(data_path)
    
    # Run model (default: three change points)
    model, trace = run_change_point_model(df["LogReturn"], df["Date"], events_path, output_dir, num_change_points=3)

if __name__ == "__main__":
    main()