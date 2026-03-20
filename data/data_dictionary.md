# Data Dictionary

This document describes the structure and meaning of the dataset used in the Retail Sales Data Pipeline & Analytics project.

| Column Name        | Description                                      | Data Type |
|-------------------|--------------------------------------------------|----------|
| transaction_id    | Unique identifier for each transaction           | Integer  |
| customer_id       | Unique identifier for each customer              | Integer  |
| category          | Product category (e.g., Food, Beverages)         | String   |
| item              | Name of the product/item purchased               | String   |
| price_per_unit    | Price of a single unit of the product            | Float    |
| quantity          | Number of units purchased in the transaction     | Integer  |
| total_spent       | Total amount spent in the transaction            | Float    |
| payment_method    | Mode of payment (e.g., Cash, Card, Wallet)       | String   |
| location          | Sales channel or store type (Online / In-store)  | String   |
| transaction_date  | Date when the transaction occurred               | Date     |
| discount_applied  | Indicates whether a discount was applied (Yes/No)| String   |

---

## Notes

- Additional time-based features such as **year**, **month**, and **month_name** were created from `transaction_date` during analysis.
- The dataset is transaction-level, meaning each row represents one sales transaction.