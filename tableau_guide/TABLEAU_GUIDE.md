# Tableau Dashboard Design Guide — HeartWatch Analytics

## Overview
Use `analysis/outputs/heart_disease_clean.csv` as your Tableau data source.

## Recommended Sheets

### Sheet 1: Age Group Bar Chart
- **Columns:** AgeGroup
- **Rows:** COUNT([HeartDisease])
- **Color:** HeartDisease (Positive/Negative)
- **Chart Type:** Stacked Bar
- **Title:** "Heart Disease by Age Group"

### Sheet 2: Gender Donut
- **Columns:** Gender
- **Angle:** COUNT([PatientId])
- **Color:** HeartDisease
- **Chart Type:** Pie/Donut

### Sheet 3: Cholesterol Heatmap
- **Rows:** CholBin
- **Columns:** AgeGroup
- **Color:** AVG(HeartDisease) → continuous color scale
- **Chart Type:** Highlight Table (Heatmap)

### Sheet 4: BP Analysis
- **Columns:** BPBin
- **Rows:** COUNT([HeartDisease])
- **Color:** HeartDisease
- **Chart Type:** Grouped Bar

### Sheet 5: Lifestyle Factors
- **Rows:** Smoking, PhysicalActivity, DietQuality (separate sheets)
- **Columns:** COUNT([HeartDisease])
- **Color:** HeartDisease
- **Chart Type:** Horizontal Bar

### Sheet 6: Regional Map
- **Mark Type:** Map (if regions are geographic)
- **Color:** SUM([HeartDisease]) / COUNT([HeartDisease]) * 100
- **Tooltip:** Region, Total Patients, Positive Rate

### Sheet 7: Scatter (Age vs Cholesterol)
- **Columns:** Age
- **Rows:** Cholesterol
- **Color:** HeartDisease
- **Size:** BMI
- **Chart Type:** Scatter Plot

### Sheet 8: Correlation (Manual Heatmap)
- Use a cross-join calculated field approach in Tableau
- Or import the correlation data from `analysis_results.json`

## Dashboard Layout (1400×900)

```
┌─────────────────────────────────────────────────────────┐
│  [KPI: Total]  [KPI: Positive]  [KPI: Prevalence %]    │
├──────────────────────┬──────────────────────────────────┤
│  Age Group Bar       │  Gender Donut                    │
├──────────────────────┼──────────────────────────────────┤
│  Cholesterol Heatmap │  Blood Pressure Bar              │
├──────────────────────┴──────────────────────────────────┤
│  Lifestyle Factors (Smoking / Activity / Diet)          │
├─────────────────────────────────────────────────────────┤
│  Regional Map                                           │
└─────────────────────────────────────────────────────────┘
```

## Interactivity
1. **Filter Action:** Dashboard → Actions → Filter  
   Source: Any sheet | Target: All sheets | Filter: AgeGroup
2. **Highlight Action:** Source: Any | Target: All | Fields: HeartDisease
3. **URL Action:** For patient drill-through (optional)

## Color Palette
- Positive (Heart Disease): `#E84B6A` (red)
- Negative (Healthy): `#4ECDC4` (teal)
- KPI Accent: `#A78BFA` (purple)
- Neutral: `#8892B0` (gray)
