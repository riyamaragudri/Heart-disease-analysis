"""
Heart Disease Data Analysis & Preprocessing
Generates all statistics, correlation data, and chart-ready JSON files
used by the Flask application.
"""

import pandas as pd
import numpy as np
import json
import os
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'dataset', 'heart_disease_data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'flask_app', 'static', 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} records, {df.shape[1]} columns")

# ─────────────────────────────────────────────
# 2. CLEANING & PREPROCESSING
# ─────────────────────────────────────────────
print("\n── Missing Values ──")
print(df.isnull().sum()[df.isnull().sum() > 0])

# Drop duplicates
before = len(df)
df.drop_duplicates(inplace=True)
print(f"Removed {before - len(df)} duplicate rows")

# Encode binary labels for display
df['HeartDiseaseLabel'] = df['HeartDisease'].map({0: 'No Disease', 1: 'Disease'})
df['SmokingLabel']      = df['Smoking'].map({0: 'Non-Smoker', 1: 'Smoker'})
df['AlcoholLabel']      = df['AlcoholConsumption'].map({0: 'Non-Drinker', 1: 'Drinker'})
df['AnginaLabel']       = df['ExerciseAngina'].map({0: 'No Angina', 1: 'Angina'})

print(f"\nFinal dataset shape: {df.shape}")

# ─────────────────────────────────────────────
# 3. SUMMARY KPIs
# ─────────────────────────────────────────────
total         = len(df)
diseased      = int(df['HeartDisease'].sum())
healthy       = total - diseased
disease_rate  = round(diseased / total * 100, 1)
avg_age       = round(df['Age'].mean(), 1)
avg_chol      = round(df['Cholesterol'].mean(), 1)
avg_bp        = round(df['RestingBP'].mean(), 1)
avg_bmi       = round(df['BMI'].mean(), 1)
smoker_pct    = round(df['Smoking'].mean() * 100, 1)
obese_pct     = round((df['BMICategory'] == 'Obese').mean() * 100, 1)
high_risk_age = df[df['HeartDisease'] == 1]['Age'].mean()

kpis = {
    "total_patients": total,
    "heart_disease_cases": diseased,
    "healthy_cases": healthy,
    "disease_rate_pct": disease_rate,
    "avg_age": avg_age,
    "avg_cholesterol": avg_chol,
    "avg_blood_pressure": avg_bp,
    "avg_bmi": avg_bmi,
    "smoker_pct": smoker_pct,
    "obese_pct": obese_pct,
    "high_risk_avg_age": round(high_risk_age, 1),
    "male_disease_rate": round(
        df[df['Gender']=='Male']['HeartDisease'].mean()*100, 1),
    "female_disease_rate": round(
        df[df['Gender']=='Female']['HeartDisease'].mean()*100, 1),
}
with open(os.path.join(OUTPUT_DIR, 'kpis.json'), 'w') as f:
    json.dump(kpis, f, indent=2)
print("\nKPIs saved.")

# ─────────────────────────────────────────────
# 4. AGE & GENDER DISTRIBUTION
# ─────────────────────────────────────────────
age_gender = (
    df.groupby(['AgeGroup', 'Gender'])['HeartDisease']
    .agg(['sum', 'count'])
    .reset_index()
)
age_gender.columns = ['age_group', 'gender', 'cases', 'total']
age_gender['rate'] = (age_gender['cases'] / age_gender['total'] * 100).round(1)

with open(os.path.join(OUTPUT_DIR, 'age_gender.json'), 'w') as f:
    json.dump(age_gender.to_dict(orient='records'), f, indent=2)

# ─────────────────────────────────────────────
# 5. CHOLESTEROL vs HEART DISEASE
# ─────────────────────────────────────────────
chol_bins = [0, 150, 200, 240, 280, 999]
chol_labels = ['<150', '150-200', '200-240', '240-280', '>280']
df['CholGroup'] = pd.cut(df['Cholesterol'], bins=chol_bins, labels=chol_labels)

chol_dist = (
    df.groupby(['CholGroup', 'HeartDiseaseLabel'])
    .size().reset_index(name='count')
)
with open(os.path.join(OUTPUT_DIR, 'cholesterol.json'), 'w') as f:
    json.dump(chol_dist.to_dict(orient='records'), f, indent=2)

# ─────────────────────────────────────────────
# 6. BLOOD PRESSURE ANALYSIS
# ─────────────────────────────────────────────
bp_bins   = [0, 90, 120, 140, 160, 999]
bp_labels = ['Low(<90)', 'Normal(90-120)', 'Pre-High(120-140)', 'High(140-160)', 'Crisis(>160)']
df['BPGroup'] = pd.cut(df['RestingBP'], bins=bp_bins, labels=bp_labels)

bp_dist = (
    df.groupby(['BPGroup', 'HeartDiseaseLabel'])
    .size().reset_index(name='count')
)
with open(os.path.join(OUTPUT_DIR, 'blood_pressure.json'), 'w') as f:
    json.dump(bp_dist.to_dict(orient='records'), f, indent=2)

# ─────────────────────────────────────────────
# 7. BMI ANALYSIS
# ─────────────────────────────────────────────
bmi_dist = (
    df.groupby(['BMICategory', 'HeartDiseaseLabel'])
    .size().reset_index(name='count')
)
with open(os.path.join(OUTPUT_DIR, 'bmi.json'), 'w') as f:
    json.dump(bmi_dist.to_dict(orient='records'), f, indent=2)

# ─────────────────────────────────────────────
# 8. LIFESTYLE FACTORS
# ─────────────────────────────────────────────
lifestyle = {
    'smoking': df.groupby('SmokingLabel')['HeartDisease'].agg(['sum','count']).reset_index().rename(columns={'SmokingLabel':'label','sum':'cases','count':'total'}).assign(rate=lambda x:(x.cases/x.total*100).round(1)).to_dict(orient='records'),
    'physical_activity': df.groupby('PhysicalActivity')['HeartDisease'].agg(['sum','count']).reset_index().rename(columns={'PhysicalActivity':'label','sum':'cases','count':'total'}).assign(rate=lambda x:(x.cases/x.total*100).round(1)).to_dict(orient='records'),
    'alcohol': df.groupby('AlcoholLabel')['HeartDisease'].agg(['sum','count']).reset_index().rename(columns={'AlcoholLabel':'label','sum':'cases','count':'total'}).assign(rate=lambda x:(x.cases/x.total*100).round(1)).to_dict(orient='records'),
    'stress': df.groupby('StressLevel')['HeartDisease'].agg(['sum','count']).reset_index().rename(columns={'StressLevel':'label','sum':'cases','count':'total'}).assign(rate=lambda x:(x.cases/x.total*100).round(1)).to_dict(orient='records'),
    'diet': df.groupby('DietQuality')['HeartDisease'].agg(['sum','count']).reset_index().rename(columns={'DietQuality':'label','sum':'cases','count':'total'}).assign(rate=lambda x:(x.cases/x.total*100).round(1)).to_dict(orient='records'),
}
with open(os.path.join(OUTPUT_DIR, 'lifestyle.json'), 'w') as f:
    json.dump(lifestyle, f, indent=2)

# ─────────────────────────────────────────────
# 9. REGIONAL ANALYSIS
# ─────────────────────────────────────────────
regional = (
    df.groupby('Region')['HeartDisease']
    .agg(['sum','count'])
    .reset_index()
    .rename(columns={'Region':'region','sum':'cases','count':'total'})
)
regional['rate'] = (regional['cases'] / regional['total'] * 100).round(1)
with open(os.path.join(OUTPUT_DIR, 'regional.json'), 'w') as f:
    json.dump(regional.to_dict(orient='records'), f, indent=2)

# ─────────────────────────────────────────────
# 10. CORRELATION HEATMAP DATA
# ─────────────────────────────────────────────
num_cols = ['Age','Cholesterol','RestingBP','BMI','MaxHR','STDepression',
            'SleepHours','FastingBS','Smoking','AlcoholConsumption',
            'ExerciseAngina','HeartDisease']
corr = df[num_cols].corr().round(3)

heatmap_data = []
for col1 in num_cols:
    for col2 in num_cols:
        heatmap_data.append({
            'x': col1,
            'y': col2,
            'value': float(corr.loc[col1, col2])
        })
with open(os.path.join(OUTPUT_DIR, 'correlation.json'), 'w') as f:
    json.dump(heatmap_data, f, indent=2)

# ─────────────────────────────────────────────
# 11. RISK FACTOR IMPORTANCE
# ─────────────────────────────────────────────
risk_factors = []
for col, label in [
    ('Smoking','Smoking'), ('ExerciseAngina','Exercise Angina'),
    ('STDepression','ST Depression'), ('FastingBS','Fasting Blood Sugar'),
    ('Age','Age>55'), ('Cholesterol','High Cholesterol'),
    ('RestingBP','High BP'), ('BMI','Obesity')
]:
    if col == 'Age':
        rate = df[df['Age'] > 55]['HeartDisease'].mean()
    elif col == 'Cholesterol':
        rate = df[df['Cholesterol'] > 240]['HeartDisease'].mean()
    elif col == 'RestingBP':
        rate = df[df['RestingBP'] > 140]['HeartDisease'].mean()
    elif col == 'BMI':
        rate = df[df['BMICategory'] == 'Obese']['HeartDisease'].mean()
    else:
        rate = df[df[col] == 1]['HeartDisease'].mean()
    risk_factors.append({'factor': label, 'disease_rate': round(rate*100, 1)})

risk_factors.sort(key=lambda x: x['disease_rate'], reverse=True)
with open(os.path.join(OUTPUT_DIR, 'risk_factors.json'), 'w') as f:
    json.dump(risk_factors, f, indent=2)

# ─────────────────────────────────────────────
# 12. CHEST PAIN TYPE
# ─────────────────────────────────────────────
chest = (
    df.groupby('ChestPainType')['HeartDisease']
    .agg(['sum','count']).reset_index()
    .rename(columns={'ChestPainType':'type','sum':'cases','count':'total'})
)
chest['rate'] = (chest['cases']/chest['total']*100).round(1)
with open(os.path.join(OUTPUT_DIR, 'chest_pain.json'), 'w') as f:
    json.dump(chest.to_dict(orient='records'), f, indent=2)

# ─────────────────────────────────────────────
# 13. AGE TREND (line chart)
# ─────────────────────────────────────────────
age_trend = (
    df.groupby('Age')['HeartDisease']
    .agg(['sum','count']).reset_index()
    .rename(columns={'Age':'age','sum':'cases','count':'total'})
)
age_trend['rate'] = (age_trend['cases']/age_trend['total']*100).round(1)
with open(os.path.join(OUTPUT_DIR, 'age_trend.json'), 'w') as f:
    json.dump(age_trend.to_dict(orient='records'), f, indent=2)

# ─────────────────────────────────────────────
# 14. SCATTER DATA (Age vs Cholesterol, colored by disease)
# ─────────────────────────────────────────────
scatter = df[['Age','Cholesterol','BMI','RestingBP','HeartDisease','HeartDiseaseLabel','Gender']].copy()
scatter = scatter.sample(min(500, len(scatter)), random_state=42)
with open(os.path.join(OUTPUT_DIR, 'scatter.json'), 'w') as f:
    json.dump(scatter.to_dict(orient='records'), f, indent=2)

print("\n✅ All analysis files saved to flask_app/static/data/")
print("\nFiles generated:")
for fn in os.listdir(OUTPUT_DIR):
    print(f"  {fn}")
