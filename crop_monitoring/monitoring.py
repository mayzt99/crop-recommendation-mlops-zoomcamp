import pandas as pd
import numpy as np
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric, DatasetMissingValuesMetric
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
import pickle
# import psycopg2
from datetime import datetime
import json

def load_reference_data():
    """Load reference dataset for monitoring"""
    df = pd.read_csv('data/Crop_recommendation.csv')
    return df

def create_monitoring_report(reference_data, current_data):
    """Create Evidently monitoring report"""
    
    # Define column mapping
    column_mapping = ColumnMapping(
        target='label',
        numerical_features=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'],
        categorical_features=['label']
    )
    
    # Create report
    report = Report(metrics=[
        DataDriftPreset(),
        DataQualityPreset(),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ])
    
    report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)
    
    return report

# def save_monitoring_results(report, timestamp):
#     """Save monitoring results to PostgreSQL"""
    
#     # Get report as dict
#     report_dict = report.as_dict()
    
#     # Extract key metrics
#     dataset_drift = report_dict['metrics'][2]['result']['dataset_drift']
#     missing_values = report_dict['metrics'][3]['result']['current']['number_of_missing_values']
    
#     # Connect to PostgreSQL
#     conn = psycopg2.connect(
#         host="localhost",
#         database="postgres",
#         user="postgres",
#         password="example",
#         port="5432"
#     )
    
#     cur = conn.cursor()
    
#     # Create table if not exists
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS monitoring_results (
#             id SERIAL PRIMARY KEY,
#             timestamp TIMESTAMP,
#             dataset_drift BOOLEAN,
#             missing_values INTEGER,
#             report_json TEXT
#         )
#     """)
    
#     # Insert results
#     cur.execute("""
#         INSERT INTO monitoring_results (timestamp, dataset_drift, missing_values, report_json)
#         VALUES (%s, %s, %s, %s)
#     """, (timestamp, dataset_drift, missing_values, json.dumps(report_dict)))
    
#     conn.commit()
#     cur.close()
#     conn.close()

def simulate_current_data():
    """Simulate current production data with some drift"""
    reference_data = load_reference_data()
    
    # Add some drift to simulate production data
    current_data = reference_data.copy()
    current_data['N'] = current_data['N'] + np.random.normal(0, 5, len(current_data))
    current_data['temperature'] = current_data['temperature'] + np.random.normal(0, 2, len(current_data))
    
    return current_data.sample(n=100)  # Sample for monitoring

def run_monitoring():
    """Main monitoring function"""
    print("Starting monitoring...")
    
    # Load data
    reference_data = load_reference_data()
    current_data = simulate_current_data()
    
    print(f"Reference data shape: {reference_data.shape}")
    print(f"Current data shape: {current_data.shape}")
    
    # Create monitoring report
    report = create_monitoring_report(reference_data, current_data)
    
    # Save results
    timestamp = datetime.now()
    # save_monitoring_results(report, timestamp)
    
    # Save HTML report
    report.save_html(f"monitoring_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.html")
    
    print(f"Monitoring completed at {timestamp}")
    print("Report saved to HTML file and database")

if __name__ == "__main__":
    run_monitoring()