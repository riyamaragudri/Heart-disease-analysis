use heart_db;
select * from heart_new2_tb;

-- check values--
SELECT *
FROM heart_new2_tb
WHERE BMI IS NULL 
OR HeartDisease IS NULL;

-- Check Duplicate record--
SELECT *, COUNT(*)
FROM heart_new2_tb
GROUP BY 
HeartDisease,BMI,Smoking,AlcoholDrinking,Stroke,
PhysicalHealth,MentalHealth,DiffWalking,Sex,
AgeCategory,Race,Diabetic,PhysicalActivity,
GenHealth,SleepTime,Asthma,KidneyDisease,SkinCancer
HAVING COUNT(*) > 1;

-- validate categrial value--
SELECT DISTINCT Smoking
FROM heart_new2_tb;

-- checking numerical Range--
SELECT MIN(BMI), MAX(BMI)
FROM heart_new2_tb; 

-- Check outlier--
SELECT *
FROM heart_new2_tb
WHERE BMI > 60 OR BMI < 10;

-- creting new view tableau--
CREATE VIEW heart_clean AS
SELECT 
HeartDisease,BMI,Smoking,AlcoholDrinking,Stroke,PhysicalHealth,
MentalHealth,DiffWalking,Sex,AgeCategory,Race,Diabetic,
PhysicalActivity,GenHealth,SleepTime,Asthma,KidneyDisease,SkinCancer
FROM heart_new2_tb
WHERE BMI IS NOT NULL
AND BMI BETWEEN 10 AND 60;

-- Craete new table with unique records--
CREATE TABLE heart_clean_tb AS
SELECT DISTINCT *
FROM heart_new2_tb;


-- Final query--
SELECT *
FROM heart_clean_tb;





