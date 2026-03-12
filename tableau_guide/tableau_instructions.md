# Tableau Dashboard — Complete Build Guide

## Prerequisites
- Tableau Desktop 2022+ or Tableau Public (free)
- The generated CSV: `dataset/heart_disease_data.csv`

---

## Step 1: Connect to Data
1. Open Tableau Desktop → Connect → Text File
2. Browse to `heart_disease_data.csv`
3. In Data Source tab, review columns
4. Right-click `HeartDisease` → Change Data Type → String

---

## Step 2: Calculated Fields to Create

| Field Name | Formula |
|---|---|
| Disease Label | `IF [Heart Disease] = "1" THEN "Disease" ELSE "Healthy" END` |
| Age Group | `IF [Age]<35 THEN "25-34" ELSEIF [Age]<45 THEN "35-44" ELSEIF [Age]<55 THEN "45-54" ELSEIF [Age]<65 THEN "55-64" ELSE "65+" END` |
| BMI Category | `IF [Bmi]<18.5 THEN "Underweight" ELSEIF [Bmi]<25 THEN "Normal" ELSEIF [Bmi]<30 THEN "Overweight" ELSE "Obese" END` |
| Disease Rate | `SUM(IF [Heart Disease]="1" THEN 1 ELSE 0 END) / COUNT([Heart Disease])` |
| BP Group | `IF [Resting Bp]<90 THEN "Low" ELSEIF [Resting Bp]<120 THEN "Normal" ELSEIF [Resting Bp]<140 THEN "Pre-High" ELSEIF [Resting Bp]<160 THEN "High" ELSE "Crisis" END` |

---

## Step 3: Build 7 Worksheets

### Sheet 1 — Overview KPIs
- Add 4 text tiles: Total Patients, Disease Cases, Disease Rate %, Avg Age
- Add a Pie chart: Rows=Disease Label, Mark=Pie, Angle=CNT(Patients), Color=Disease Label

### Sheet 2 — Age × Gender (Grouped Bar)
- Cols: Age Group | Rows: Disease Rate
- Drag Gender to Color shelf
- Mark Type: Bar | Set Bar Width: 70%
- Add Quick Filter: Age Group, Gender

### Sheet 3 — Cholesterol Distribution
- Create Cholesterol Bins (size=20): Right-click Cholesterol → Create Bins
- Cols: Cholesterol Bins | Rows: CNT(Patients)
- Color: Disease Label
- Mark Type: Bar, Stacked

### Sheet 4 — Blood Pressure Heatmap
- Rows: BP Group | Cols: Resting ECG
- Mark Type: Square
- Color: Disease Rate (Red-Blue palette, reversed)
- Label: Disease Rate

### Sheet 5 — Lifestyle Dashboard (4 charts)
- Create 4 separate worksheets for: Smoking, Physical Activity, Stress Level, Diet Quality
- Each: Rows=Disease Rate | Cols=Category | Color=Risk level
- Combine all 4 into a single Lifestyle dashboard

### Sheet 6 — Scatter Plot
- Cols: Age | Rows: Cholesterol
- Mark Type: Circle
- Color: Disease Label | Size: BMI
- Analytics Pane → Drag Trend Line → Linear

### Sheet 7 — Regional Analysis
- Rows: Region | Cols: Disease Rate
- Mark Type: Bar
- Add Reference Line: Column Average
- Color: Disease Rate (red = high)

---

## Step 4: Create Main Dashboard
1. New Dashboard → Size: Fixed 1200×900
2. Layout:
   ```
   [Sheet 1 - KPIs: full width, height 150px]
   [Sheet 2 - Age/Gender | Sheet 3 - Cholesterol]
   [Sheet 5 - Lifestyle  | Sheet 7 - Regional   ]
   [Sheet 6 - Scatter: full width]
   ```
3. Add global Gender and Age Group filters
4. Enable "Use as Filter" on all chart tiles

---

## Step 5: Styling
- Background: Dark (#1a1a2e or similar)
- Text: White
- Accent: Red for Disease, Green for Healthy
- Font: Tableau Semibold 12pt for titles
- Remove grid lines where possible

---

## Step 6: Publish
- Tableau Public: Server → Save to Tableau Public
- Copy embed code for Flask integration
- Update `flask_app/templates/tableau.html` with your embed URL
