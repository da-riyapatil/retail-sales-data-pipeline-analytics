# Project Summary

## Retail Sales Data Pipeline & Analytics

### Project Overview
This project is an end-to-end retail sales analytics workflow built using MySQL, Python, Azure services, and Power BI.

It starts with raw retail sales data in CSV format, processes the data through cleaning and preprocessing in Python, stores the refined data in Azure SQL Database, and uses it for analysis and reporting.

### Business Problem
Retail transaction data is often stored in raw files, which makes reporting and analysis difficult.

This project was built to create a simple data pipeline that moves raw sales data into a structured cloud database and helps answer important business questions around revenue, product performance, customer behavior, discounts, and sales channels.

### Pipeline Summary
- Raw retail sales data collected in CSV format
- Loaded into MySQL for initial storage
- Cleaned and preprocessed using Python
- Exported as cleaned CSV
- Uploaded to Azure Blob Storage
- Moved through Azure Data Factory into Azure SQL Database
- Used Azure SQL data for Python EDA and Power BI dashboard reporting

### Tools Used
- MySQL
- Python
- Pandas
- Jupyter Notebook
- Azure Blob Storage
- Azure Data Factory
- Azure SQL Database
- Power BI
- Power BI Service

### Key Analysis Areas
- Revenue trends and overall sales performance
- Product category performance
- Payment method contribution
- Discount impact on quantity sold
- Online vs in-store sales comparison
- Customer purchase patterns

### Key Insights
- Clothing and Electronics were among the strongest revenue-contributing categories
- Card and digital payment methods contributed a major share of total sales
- Discounted transactions generally showed higher purchase quantity compared to non-discounted sales
- Online and in-store channels showed visible differences in sales contribution
- Monthly sales trends helped identify stronger and weaker performing periods

### Final Outcome
This project demonstrates my ability to:
- build a simple end-to-end data pipeline
- clean and prepare raw business data using Python
- move data through cloud storage and data integration services
- analyze structured data using SQL, Python, and Power BI
- present business-focused insights in a clear and practical way