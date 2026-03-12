"""
Heart Disease Data Analysis & Preprocessing
Generates all statistical insights and exports cleaned data for Flask API
"""
import pandas as pd
import numpy as np
import json
import os

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'dataset', 'heart_disease_data.csv')
OUT_DIR   = os.path.join(BASE_DIR, 'analysis', 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows | columns: {list(df.columns)}")

# ── 1. Basic cleaning ──────────────────────────────────────────────────────
df = df.drop_duplicates()
df['Smoking']         = df['Smoking'].map({1: 'Yes', 0: 'No'}) if df['Smoking'].dtype != object else df['Smoking']
df['ExerciseAngina']  = df['ExerciseAngina'].map({1: 'Yes', 0: 'No'}) if df['ExerciseAngina'].dtype != object else df['ExerciseAngina']
df['FastingBS']       = df['FastingBS'].map({1: 'Yes', 0: 'No'}) if df['FastingBS'].dtype != object else df['FastingBS']
df['HeartDisease_Label'] = df['HeartDisease'].map({1: 'Positive', 0: 'Negative'})

# ── 2. KPI Summary ─────────────────────────────────────────────────────────
total       = len(df)
positive    = int(df['HeartDisease'].sum())
negative    = total - positive
prevalence  = round(positive / total * 100, 1)
avg_age     = round(df['Age'].mean(), 1)
avg_chol    = round(df['Cholesterol'].mean(), 1)
avg_bp      = round(df['RestingBP'].mean(), 1)
avg_bmi     = round(df['BMI'].mean(), 1)
smoking_pct = round((df['Smoking'] == 'Yes').mean() * 100, 1)

kpi = {
    "total_patients": total,
    "positive_cases": positive,
    "negative_cases": negative,
    "prevalence_pct": prevalence,
    "avg_age": avg_age,
    "avg_cholesterol": avg_chol,
    "avg_bp": avg_bp,
    "avg_bmi": avg_bmi,
    "smoking_pct": smoking_pct
}
print(f"\n📊 KPIs:\n{json.dumps(kpi, indent=2)}")

# ── 3. Age-group distribution ──────────────────────────────────────────────
age_dist = (df.groupby(['AgeGroup', 'HeartDisease_Label'])
              .size()
              .reset_index(name='count')
              .sort_values('AgeGroup'))

# ── 4. Gender breakdown ────────────────────────────────────────────────────
gender_dist = (df.groupby(['Gender', 'HeartDisease_Label'])
                 .size()
                 .reset_index(name='count'))

# ── 5. Cholesterol bins ────────────────────────────────────────────────────
df['CholBin'] = pd.cut(df['Cholesterol'],
                       bins=[0, 200, 239, 270, 400],
                       labels=['<200 (Optimal)', '200-239 (Borderline)', '240-270 (High)', '>270 (Very High)'])
chol_dist = (df.groupby(['CholBin', 'HeartDisease_Label'])
               .size()
               .reset_index(name='count'))

# ── 6. BP bins ─────────────────────────────────────────────────────────────
df['BPBin'] = pd.cut(df['RestingBP'],
                     bins=[0, 120, 129, 139, 180, 300],
                     labels=['Normal (<120)', 'Elevated (120-129)', 'Stage1 HBP (130-139)', 'Stage2 HBP (140-180)', 'Crisis (>180)'])
bp_dist = (df.groupby(['BPBin', 'HeartDisease_Label'])
             .size()
             .reset_index(name='count'))

# ── 7. Lifestyle factors ───────────────────────────────────────────────────
lifestyle_factors = {}
for col in ['Smoking', 'PhysicalActivity', 'AlcoholConsumption', 'DietQuality']:
    tmp = (df.groupby([col, 'HeartDisease_Label'])
             .size()
             .reset_index(name='count'))
    lifestyle_factors[col] = tmp.to_dict('records')

# ── 8. BMI categories ─────────────────────────────────────────────────────
bmi_dist = (df.groupby(['BMICategory', 'HeartDisease_Label'])
              .size()
              .reset_index(name='count'))

# ── 9. Chest pain types ────────────────────────────────────────────────────
cp_dist = (df.groupby(['ChestPainType', 'HeartDisease_Label'])
             .size()
             .reset_index(name='count'))

# ── 10. Regional breakdown ─────────────────────────────────────────────────
regional = (df.groupby('Region')
              .agg(total=('HeartDisease', 'count'),
                   positive=('HeartDisease', 'sum'))
              .reset_index())
regional['rate'] = (regional['positive'] / regional['total'] * 100).round(1)

# ── 11. Correlation heatmap data ───────────────────────────────────────────
df['StressLevel_num'] = df['StressLevel'].map({'Low': 1, 'Medium': 2, 'High': 3}).fillna(2)
num_cols = ['Age', 'Cholesterol', 'RestingBP', 'BMI', 'MaxHR', 'STDepression',
            'SleepHours', 'StressLevel_num', 'HeartDisease']
corr_df  = df[num_cols].corr().round(3)
corr_data = []
for i in corr_df.columns:
    for j in corr_df.columns:
        corr_data.append({"x": i, "y": j, "value": float(corr_df.loc[i, j])})

# ── 12. Age vs Cholesterol scatter sample ─────────────────────────────────
scatter = df[['Age', 'Cholesterol', 'HeartDisease_Label', 'Gender']].sample(300, random_state=1)

# ── 13. Risk score per patient ─────────────────────────────────────────────
df['RiskScore'] = (
    ((df['Age'] > 55).astype(int) * 20) +
    ((df['Gender'] == 'Male').astype(int) * 10) +
    ((df['Cholesterol'] > 240).astype(int) * 15) +
    ((df['RestingBP'] > 140).astype(int) * 15) +
    ((df['Smoking'] == 'Yes').astype(int) * 20) +
    ((df['BMI'] > 30).astype(int) * 10) +
    ((df['PhysicalActivity'] == 'Low').astype(int) * 10)
).clip(0, 100)

risk_dist = (df.groupby('AgeGroup')['RiskScore']
               .mean()
               .reset_index()
               .rename(columns={'RiskScore': 'avg_risk'}))
risk_dist['avg_risk'] = risk_dist['avg_risk'].round(1)

# ── 14. Monthly trend simulation ──────────────────────────────────────────
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
np.random.seed(7)
monthly_cases = (np.random.normal(45, 8, 12) + np.sin(np.linspace(0, 2*np.pi, 12))*5).clip(20, 70).astype(int).tolist()

# ── Save all outputs ───────────────────────────────────────────────────────
outputs = {
    "kpi":               kpi,
    "age_distribution":  age_dist.to_dict('records'),
    "gender_distribution": gender_dist.to_dict('records'),
    "cholesterol_distribution": chol_dist.to_dict('records'),
    "bp_distribution":   bp_dist.to_dict('records'),
    "lifestyle_factors": lifestyle_factors,
    "bmi_distribution":  bmi_dist.to_dict('records'),
    "chest_pain":        cp_dist.to_dict('records'),
    "regional":          regional.to_dict('records'),
    "correlation":       corr_data,
    "scatter_sample":    scatter.to_dict('records'),
    "risk_by_age":       risk_dist.to_dict('records'),
    "monthly_trend":     [{"month": m, "cases": c} for m, c in zip(months, monthly_cases)]
}

json_path = os.path.join(OUT_DIR, 'analysis_results.json')
with open(json_path, 'w') as f:
    json.dump(outputs, f, indent=2)

# Also save cleaned CSV for Tableau
clean_path = os.path.join(OUT_DIR, 'heart_disease_clean.csv')
df.to_csv(clean_path, index=False)

print(f"\n✅ Analysis complete!")
print(f"   JSON  → {json_path}")
print(f"   CSV   → {clean_path}")
