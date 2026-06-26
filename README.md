# 🛍️ Shopper Spectrum: E-Commerce Intelligence App

An end-to-end data science application that performs predictive customer segmentation and builds a product recommendation engine using transactional data from an e-commerce platform. The final interactive application is built and deployed using Streamlit.

## 🎯 Project Overview
This project solves a critical business problem for online retailers: identifying highly valuable customers and boosting sales via smart cross-selling. 

### Key Deliverables:
1. **Data Preprocessing & Cleaning:** Managed missing values, eliminated multi-line duplicates, handled returned/cancelled orders, and filtered structural noise out of raw transaction logs.
2. **Exploratory Data Analysis (EDA):** Uncovered business trends including top-selling stock items, country-wide revenue generation, and monthly sales graphs.
3. **Customer Segmentation (RFM Analysis):** Categorized buyers mathematically using Recency, Frequency, and Monetary parameters into 4 cohorts (High Value, Regular, Occasional, and At-Risk).
4. **Product Recommendation System:** Built a Next-Best-Item prediction module utilizing a Co-occurrence Matrix to find patterns in products frequently bought together.
5. **Interactive UI Dashboard:** A lightweight web application for marketing teams to quickly analyze user IDs or get item recommendations instantly.

---

## 🛠️ Tech Stack & Libraries
- **Language:** Python
- **Data Engineering:** Pandas, NumPy
- **Visualizations:** Matplotlib, Seaborn
- **UI & Web Deployment:** Streamlit
- **Storage/Serialization:** Pickle

---

## 📂 Project Structure
```text
├── data.csv                # Raw e-commerce transactions dataset
├── eda.py                  # Script for initial data exploration & insights
├── pipeline.py             # Data processing, RFM scoring, and modeling pipeline
├── app.py                  # Live Streamlit application file
├── requirements.txt        # Production environment dependencies 
└── README.md               # Repository documentation homepage
