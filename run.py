"""Entry point — run from project root: python run.py"""
import subprocess, sys, os

# 1. Generate dataset if missing
dataset = os.path.join('dataset', 'heart_disease_data.csv')
if not os.path.exists(dataset):
    print("Generating dataset...")
    subprocess.run([sys.executable, os.path.join('dataset', 'generate_dataset.py')], check=True)

# 2. Run analysis if missing
analysis = os.path.join('analysis', 'outputs', 'analysis_results.json')
if not os.path.exists(analysis):
    print("Running analysis...")
    subprocess.run([sys.executable, os.path.join('analysis', 'data_analysis.py')], check=True)

# 3. Start Flask
os.chdir('flask_app')
sys.path.insert(0, '.')
from app import app
print("\nHeartWatch Analytics is running!")
print("   Open: http://localhost:5000\n")
app.run(debug=False, port=5000)
