# 🚗 Vehicle Recall Data Analysis Project

## 📌 Project Overview
This project focuses on analyzing vehicle recall data to identify patterns, high-risk components, affected manufacturers, and time-based trends. The goal is to understand safety issues in vehicles using data analysis and visualization techniques.

---

## 🎯 Objectives
- Analyze vehicle recall trends over time  
- Identify top manufacturers with highest recalls  
- Find most affected vehicle components  
- Understand impact of recalls on vehicles  
- Build an interactive dashboard for insights  

---

## 📊 Dataset Information
- Total Records: ~115,981  
- Features: 14 columns  
- Key Fields:
  - Vehicle Make  
  - Model Year  
  - Recall Type  
  - Main Component  
  - Recall Notification Date  
  - Estimated Units Affected  

---

## 🧹 Data Cleaning & Preprocessing
Performed using Python (Pandas):

- Removed missing/invalid values  
- Fixed incorrect date format (YYYYMMDD → datetime)  
- Handled incorrect model year (e.g., 9999 removed)  
- Created new feature: `Recall Year`  
- Standardized recall categories  

---

## 📈 Analysis Performed

### 1. Recall Type Analysis
- Classified recalls into VEHICLE, EQUIPMENT, TIRE  
- Found VEHICLE category dominates recalls  

### 2. Manufacturer Analysis
- Identified top manufacturers with highest recalls  
- Ford, GM, Chrysler among top contributors  

### 3. Component Analysis
- Airbags, Electrical System, Engine are most affected  

### 4. Impact Analysis
- Measured recalls based on estimated affected units  
- Airbags affect highest number of vehicles  

### 5. Trend Analysis
- Year-wise recall trend shows peak between 2014–2016  

---

## 📊 Dashboard (Power BI)
An interactive dashboard was built using Microsoft Power BI Desktop.

### Visuals Used:
- KPI Cards (Total Recalls, Total Units Affected)  
- Donut Chart (Recall Type Distribution)  
- Bar Chart (Top Components)  
- Treemap (Vehicle Make Distribution)  
- Impact Analysis (Affected Units)  
- Line Chart (Recall Trend Over Years)  

### Filters:
- Model Year  
- Recall Type  
- Vehicle Make  

---

## 🧠 Key Insights
- Airbags have highest safety impact  
- Electrical systems are frequently recalled  
- Ford and GM have highest recall counts  
- 2014–2016 saw peak recall activity  
- Vehicle recalls dominate overall dataset  

---

## 🛠️ Tools Used
- Python (Pandas, NumPy)  
- Microsoft Power BI Desktop  
- Excel (initial exploration)  

---

## 📌 Conclusion
This project helps understand vehicle safety trends and highlights critical components requiring attention. It demonstrates the use of data cleaning, analysis, and visualization to extract meaningful business insights.

---

## 👨‍💻 Author
Goutam Khatri  
Data Analyst Project