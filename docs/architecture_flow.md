# Architecture & Data Flow

## Overview

This project follows a simple end-to-end data pipeline that moves retail sales data from a local environment to the cloud and then uses it for analysis and reporting.

---

## Data Flow Steps

1. **Raw Data (CSV)**
   - Retail sales data was initially available in CSV format.

2. **MySQL (Local Database)**
   - The raw CSV file was loaded into MySQL on localhost.
   - This step simulates storing raw data in a structured database.

3. **Python (Data Cleaning & Preparation)**
   - Data was extracted from MySQL into Python.
   - Cleaning and preprocessing were performed using Pandas.
   - A cleaned dataset was created for further use.

4. **Cleaned Data (CSV)**
   - The processed dataset was saved as a cleaned CSV file.

5. **Azure Blob Storage**
   - The cleaned CSV file was uploaded to Azure Blob Storage.
   - This acts as cloud storage for the pipeline.

6. **Azure Data Factory (ADF)**
   - ADF was used to move data from Blob Storage to Azure SQL Database.
   - This step represents cloud-based data movement and orchestration.

7. **Azure SQL Database**
   - The final cleaned dataset was stored in Azure SQL Database.
   - This serves as the main data source for analysis and reporting.

8. **Analysis & Reporting**
   - Python (Jupyter Notebook) was used for exploratory data analysis.
   - Power BI was used to create dashboards and business reports.

---

## Key Takeaway

This project demonstrates how data can move across local systems, cloud storage, and cloud databases, and then be used for both analysis and business reporting in a structured workflow.