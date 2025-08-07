from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Set paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

@app.route("/")
def home():
    return jsonify({"message": "API is running"})

@app.route("/change-points", methods=["GET"])
def get_change_points():
    try:
        file_path = os.path.join(RESULTS_DIR, "change_points.csv")
        print(f"Reading change points from: {file_path}")  # Optional debug print
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/log-returns', methods=['GET'])
def get_log_returns():
    try:
        file_path = os.path.join('data', 'processed', 'brent_oil_log_returns.csv')
        df = pd.read_csv(file_path, parse_dates=["Date"])
        df = df.dropna(subset=["LogReturn"])
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        return jsonify(df[['Date', 'LogReturn']].to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/matched-events', methods=['GET'])
def get_matched_events():
    try:
        file_path = os.path.join('results', 'matched_events.csv')
        df = pd.read_csv(file_path, parse_dates=["Change_Point_Date", "Event_Date"])
        df['Change_Point_Date'] = df['Change_Point_Date'].dt.strftime('%Y-%m-%d')
        df['Event_Date'] = df['Event_Date'].dt.strftime('%Y-%m-%d')
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
