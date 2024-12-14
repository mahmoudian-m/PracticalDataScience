# **Loan Risk Analysis with Moving Averages and Exponential Moving Averages**

## **Project Overview**
This project focuses on calculating moving averages (MA) and exponential moving averages (EMA) to analyze loan application data from 2007 onwards. The primary goal is to extract insights from the "Risk_Score" column for better financial decision-making.

### **What Are MA and EMA?**
- **Moving Average (MA):** A simple statistical technique that smooths time-series data by calculating the average of data points over a specific window size. For instance, a 50-day MA averages the past 50 days' data.
- **Exponential Moving Average (EMA):** A weighted version of MA, where more recent data points have greater significance. This makes EMA more responsive to recent changes than MA.

### **Why Use MA and EMA?**
- **Trend Identification:** Both help detect trends in time-series data by filtering out short-term noise.
- **Prediction Support:** They are commonly used in financial analysis and predictive modeling to monitor patterns and forecast future behavior.
- **Risk Management:** By calculating these metrics, we can understand the stability of data trends, essential in assessing risk levels.

---

## **Implemented Tasks**

### **Task 1: Moving Average (MA50) Calculation for 2007**
- **Objective:** Calculate the 50-day moving average (MA50) for the "Risk_Score" column using Bash and Python.
- **Methodology:**
  - Extract 2007 data.
  - Compute the MA50 over the "Risk_Score" column.
  - Save the results into a CSV file.

### **Task 2: Enhanced Analysis**
- **Objective:** 
  - Calculate MA50 for 2007.
  - Compute a 100-day moving average (MA100) for data from 2009 onwards.

### **Task 3: EMA50 Implementation**
- **Objective:** Replace the MA50 for 2007 with an EMA50 using both Bash and Python.

---

## **Tools and Technologies**
- **Programming Languages:** Python, Bash.
- **Libraries:** Pandas.
- **Techniques:** Rolling window for MA and EMA calculations.
- **Storage:** Results are stored in CSV format for further analysis.

---

## **How to Run the Code**
1. **Prerequisites:**
   - Install Python and Pandas.
   - Place the dataset `rejected_2007_to_2018Q4.csv` in the appropriate directory(MovingAverageAnalysis).

2. **Steps:**
   - **Python Implementation:**
     - Run the Python script to calculate MA50 for 2007 (`Task1`).
     - Modify parameters for MA100 and EMA50 calculations in subsequent Tasks.
   - **Bash Implementation:**
     - Execute the Bash script to replicate the Python process for MA50 and EMA50.

3. **Output:**
   - A CSV file (`mv_result.csv`) containing the "Risk_Score" column with calculated MA and EMA.

---

## **Results**
- **Insights:** These calculations help reveal trends in loan risk scores over time, enabling more informed financial decisions.
- **Impact:** By identifying trends, financial institutions can better evaluate risk and optimize strategies.

---


## ** Dataset**
The dataset used for this analysis, rejected_2007_to_2018Q4.csv, contains loan application data from 2007 to 2018. You can access it directly from Kaggle:

Loan Application Data: 2007-2018 on Kaggle

---
