"""
Heart Disease Analysis System - Flask Application
"""
import os, json, subprocess, sys
from flask import Flask, render_template, jsonify

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_JSON = os.path.join(BASE_DIR, '..', 'analysis', 'outputs', 'analysis_results.json')

def load_analysis():
    if not os.path.exists(ANALYSIS_JSON):
        script = os.path.join(BASE_DIR, '..', 'analysis', 'data_analysis.py')
        subprocess.run([sys.executable, script], check=True)
    with open(ANALYSIS_JSON) as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/risk-factors')
def risk_factors():
    return render_template('risk_factors.html')

@app.route('/tableau')
def tableau():
    return render_template('tableau.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/kpi')
def api_kpi():
    return jsonify(load_analysis()['kpi'])

@app.route('/api/age-distribution')
def api_age():
    return jsonify(load_analysis()['age_distribution'])

@app.route('/api/gender-distribution')
def api_gender():
    return jsonify(load_analysis()['gender_distribution'])

@app.route('/api/cholesterol')
def api_cholesterol():
    return jsonify(load_analysis()['cholesterol_distribution'])

@app.route('/api/bp')
def api_bp():
    return jsonify(load_analysis()['bp_distribution'])

@app.route('/api/lifestyle')
def api_lifestyle():
    return jsonify(load_analysis()['lifestyle_factors'])

@app.route('/api/bmi')
def api_bmi():
    return jsonify(load_analysis()['bmi_distribution'])

@app.route('/api/chest-pain')
def api_chest_pain():
    return jsonify(load_analysis()['chest_pain'])

@app.route('/api/regional')
def api_regional():
    return jsonify(load_analysis()['regional'])

@app.route('/api/correlation')
def api_correlation():
    return jsonify(load_analysis()['correlation'])

@app.route('/api/scatter')
def api_scatter():
    return jsonify(load_analysis()['scatter_sample'])

@app.route('/api/risk-by-age')
def api_risk():
    return jsonify(load_analysis()['risk_by_age'])

@app.route('/api/monthly-trend')
def api_monthly():
    return jsonify(load_analysis()['monthly_trend'])

@app.route('/api/all')
def api_all():
    return jsonify(load_analysis())

if __name__ == '__main__':
    print("\n❤️  Heart Disease Analysis System")
    print("   Running at: http://localhost:5000\n")
    app.run(debug=True, port=5000)
