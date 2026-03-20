import io
import urllib

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine


# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(page_title="Retail Sales Data Analysis", layout="wide")


# ---------------------------------------------------------
# ## Retail Sales Data Analysis
# ---------------------------------------------------------
st.title("Retail Sales Data Analysis")

st.markdown("""
### Project Overview
This project focuses on performing an in-depth Exploratory Data Analysis (EDA) on clean retail sales dataset to uncover meaningful business insights related to sales performance, customer behavior, product categories, payment methods, and discount impact.

The objective is to generate data-driven insights that can help business stakeholders:
- Improve revenue and profitability
- Understand customer purchasing patterns
- Optimize product categories and pricing strategies
- Make informed decisions using analytics

*Note: Data cleaning and preprocessing were performed in a separate notebook and the clean dataset is used here strictly for analysis and visualization*
""")

st.markdown("---")

st.markdown("""
### Business Questions
1. Which product categories and items contribute the most to total revenue?
2. How does customer purchasing behavior vary across categories?
3. Which payment methods are most commonly used and most profitable?
4. Do discounts actually increase sales quantity and revenue?
5. How do online and in-store sales compare?
6. Are there seasonal or monthly trends in sales performance?
""")

st.markdown("---")

st.markdown("""
### Dataset Overview
The dataset contains transactional-level retail sales data where each row represents a single purchase transaction.

**Column Descriptions:**
- **transaction_id**: Unique identifier for each transaction
- **customer_id**: Unique identifier for each customer
- **category**: Product category (e.g., Food, Beverages, Butchers)
- **item**: Specific product purchased
- **price_per_unit**: Price of a single unit of the item
- **quantity**: Number of units purchased
- **total_spent**: Total amount spent on the transaction
- **payment_method**: Mode of payment (Cash, Credit Card, Digital Wallet)
- **location**: Sales channel (Online or In-store)
- **transaction_date**: Date of transaction
- **discount_applied**: Indicates whether a discount was applied
""")

st.markdown("---")


# ---------------------------------------------------------
# ### Connect Python to Azure SQL
# ---------------------------------------------------------
st.subheader("Connect Python to Azure SQL")

# Securely pull credentials from Streamlit Secrets
username = st.secrets["database"]["username"]
password = st.secrets["database"]["password"]
server = st.secrets["database"]["server"]
database = st.secrets["database"]["database_name"]


@st.cache_resource
def get_engine():
    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=90;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


@st.cache_data
def load_data():
    engine = get_engine()
    query = "SELECT * FROM retail_sales"
    return pd.read_sql(query, engine)


try:
    df = load_data()
    st.success("Data loaded successfully from Azure SQL.")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()


# ---------------------------------------------------------
# ### Data Loading and Initial Validation
# ---------------------------------------------------------
st.subheader("Data Loading and Initial Validation")

st.write("Preview data")
st.dataframe(df.head(10), use_container_width=True)

st.write("Count of rows and columns of the dataset:")
st.write(df.shape)

st.write("Structure of the data and non-null counts in each column")
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

st.write("Total number of missing values:")
st.dataframe(df.isna().sum().reset_index().rename(columns={"index": "column", 0: "missing_values"}), use_container_width=True)


# ---------------------------------------------------------
# ### Feature Engineering
# ---------------------------------------------------------
st.subheader("Feature Engineering")
st.write("To enable deeper analysis, additional time-based features are extracted from the transaction date.")

df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['transaction_year'] = df['transaction_date'].dt.year
df['transaction_month'] = df['transaction_date'].dt.month
df['transaction_month_name'] = df['transaction_date'].dt.month_name()
df['transaction_day'] = df['transaction_date'].dt.day

st.dataframe(df.head(), use_container_width=True)


# ---------------------------------------------------------
# ### Statistical Overview
# ---------------------------------------------------------
st.subheader("Statistical Overview")
st.write("This section provides an overall numerical understanding of pricing, quantity, and spending patterns.")
st.dataframe(df[['price_per_unit', 'quantity', 'total_spent']].describe(), use_container_width=True)


# ---------------------------------------------------------
# ### Business Driven Analysis and Visualization
# ---------------------------------------------------------
st.header("Business Driven Analysis and Visualization")


# ---------------------------------------------------------
# #### 1. Revenue Contribution by Product Category and Item
# ---------------------------------------------------------
st.subheader("1. Revenue Contribution by Product Category and Item")

st.markdown("""
Which product categories and items contribute the most to total revenue?

Understanding which categories and individual items drive the highest revenue helps businesses:
- Focus inventory planning
- Optimize pricing strategies
- Prioritize high-performing product lines
""")

st.markdown("##### 1.1 Business Analysis – Category Level")

category_revenue = (
    df.groupby('category')
      .agg(total_revenue=('total_spent', 'sum'))
)

st.dataframe(category_revenue, use_container_width=True)

st.markdown("##### Visualization – Category Revenue")

fig = px.bar(
    category_revenue.reset_index(),
    x='category',
    y='total_revenue',
    color='category',
    title='Total Revenue by Product Category',
    labels={
        'category': 'Product Category',
        'total_revenue': 'Total Revenue'
    },
    text_auto='.2s',
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_layout(
    title_x=0.5,
    xaxis_tickangle=-30,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Data insights**

- **Food** is the highest revenue-generating category with approximately **600k**, followed by **Beverages (400k)** and **Milk Products (300k)**.

- **Revenue distribution** across categories is **not evenly balanced**, as lower-performing categories such as **Furniture (17k)**, **Computers and electric accessories (59k)**, and **Electric household essentials (73k)** contribute significantly less compared to the top-performing categories.
""")

st.markdown("---")

st.markdown("##### 1.2 Business Analysis – Item Level (Top 10 items sold)")

top_items = (
    df.groupby('item')
      .agg(total_revenue=('total_spent', 'sum'))
      .sort_values(by='total_revenue', ascending=False)
      .head(10)
)

st.dataframe(top_items, use_container_width=True)

st.markdown("##### Visualization – Top Items")

fig = px.bar(
    top_items.reset_index(),
    x='item',
    y='total_revenue',
    title='Top 10 Revenue Generating Items',
    labels={
        'item': 'Item',
        'total_revenue': 'Total Revenue'
    },
    text_auto='.2s',
    color='total_revenue',
    color_continuous_scale='Blues'
)

fig.update_layout(title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Data insights**
- **Item_23_FOOD** leads item-level revenue at around **44k**, followed by **Item_27_FOOD (41k)** and **Item_25_FOOD (39k)**.

- The **revenue gap** between the top 10 items is relatively small (ranging from **31k to 44k**), suggesting **consistent performance across best-selling products rather than one dominant item**.
""")

st.markdown("---")


# ---------------------------------------------------------
# #### 2. Customer Purchasing Behavior Across Categories
# ---------------------------------------------------------
st.subheader("2. Customer Purchasing Behavior Across Categories")

st.markdown("""
How does customer purchasing behavior vary across categories?

This analysis helps identify:
- Categories with repeat purchases
- Categories with higher order values
- Customer engagement patterns
""")

st.markdown("##### Business Analysis")

customer_category_behavior = (
    df.groupby('category')
      .agg(
          avg_quantity=('quantity', 'mean'),
          avg_order_value=('total_spent', 'mean'),
          unique_customers=('customer_id', 'nunique')
      )
      .sort_values(by='avg_order_value', ascending=False)
)

st.dataframe(customer_category_behavior, use_container_width=True)

st.markdown("##### Visualization – Avg Order Value vs Customers")

fig = px.scatter(
    customer_category_behavior.reset_index(),
    x='unique_customers',
    y='avg_order_value',
    size='avg_quantity',
    color='category',
    title='Customer Purchasing Behavior Across Categories',
    labels={
        'unique_customers': 'Number of Unique Customers',
        'avg_order_value': 'Average Order Value'
    },
    size_max=40
)

fig.update_layout(title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Data insights**
- **Food** has the highest customer base with around **90 unique customers** and also records the **highest average order value** at approximately **152**, **Milk Products (90 customers, 148 AOV)** and **Beverages (90 customers, 149 AOV)** also show **strong customer engagement**.

- Categories such as **Butchers (40 customers, 151 AOV)** and **Patisserie (40 customers, 145 AOV)** have a **moderate** customer base, while **Computers and electric accessories (15 customers, 149 AOV)**, **Furniture (15 customers, 148 AOV)**, and **Electric household essentials (15 customers, 146 AOV)** have a **smaller** customer base but relatively comparable average order values.
""")

st.markdown("---")


# ---------------------------------------------------------
# #### 3. Payment Method Usage and Profitability
# ---------------------------------------------------------
st.subheader("3. Which payment methods are most commonly used and most profitable?")

st.markdown("##### Business Analysis")

payment_analysis = (
    df.groupby('payment_method')
      .agg(
          total_revenue=('total_spent', 'sum'),
          transaction_count=('transaction_id', 'count'),
          avg_order_value=('total_spent', 'mean')
      )
      .sort_values(by='total_revenue', ascending=False)
)

st.dataframe(payment_analysis, use_container_width=True)

st.markdown("##### Visualization - Payment Revenue Share")

fig = px.pie(
    payment_analysis.reset_index(),
    names='payment_method',
    values='total_revenue',
    title='Revenue Share by Payment Method',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(textinfo='percent+label')
fig.update_layout(title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Data Insights**
- **Digital Wallet** contributes the **highest revenue share (70.2%)**, followed by **Credit Card (19.9%)** and **Cash (9.92%)**

- Revenue is **heavily concentrated in Digital Wallet** payments, indicating a **strong dependency on this single payment mode** compared to others.
""")

st.markdown("---")


# ---------------------------------------------------------
# #### 4. Impact of Discounts on Sales Performance
# ---------------------------------------------------------
st.subheader("4. Impact of Discounts on Sales Performance")

st.markdown("""
Do discounts actually increase sales quantity and revenue?

Discount analysis is critical to evaluate whether promotions drive:
- Higher quantities
- Higher revenue
""")

st.markdown("##### Business Analysis")

discount_impact = (
    df.groupby('discount_applied')
      .agg(avg_quantity=('quantity', 'mean'))
)

st.dataframe(discount_impact, use_container_width=True)

st.markdown("##### Visualization – Discount Impact")

fig = px.bar(
    discount_impact.reset_index(),
    x='discount_applied',
    y='avg_quantity',
    color='discount_applied',
    title='Average Quantity Sold: Discount vs No Discount',
    labels={
        'discount_applied': 'Discount Applied',
        'avg_quantity': 'Average Quantity Sold'
    },
    text_auto='.2f',
    color_discrete_map={True: "#0d3894", False: "#7f87c0"}
)

fig.update_layout(title_x=0.5, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Data insights**

- **Average quantity sold** is significantly **higher for discounted transactions (9.99)** compared to **non-discounted transactions (4.97)**.

- This indicates that **discounts are strongly increasing purchase volume** in this dataset.
""")

st.markdown("---")


# ---------------------------------------------------------
# #### 5. Online vs In-Store Sales Performance
# ---------------------------------------------------------
st.subheader("5. Online vs In-Store Sales Performance")

st.markdown("""
How do online and in-store sales compare?
""")

st.markdown("##### Business Analysis")

channel_analysis = (
    df.groupby('location')
      .agg(total_revenue=('total_spent', 'sum'))
)

st.dataframe(channel_analysis, use_container_width=True)

st.markdown("##### Visualization – Channel Comparison")

fig = px.bar(
    channel_analysis.reset_index(),
    x='location',
    y='total_revenue',
    color='location',
    title='Revenue Comparison: Online vs In-Store',
    labels={
        'location': 'Sales Channel',
        'total_revenue': 'Total Revenue'
    },
    text_auto='.2s',
    color_discrete_sequence=['#1f77b4', '#ff7f0e']
)

fig.update_layout(title_x=0.5, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Data insights**
- **Online sales** generate **higher total revenue (1.1M)** compared to **In-store sales (600k)**.

- This suggests **customers strongly prefer online channels**, contributing nearly double the revenue compared to in-store purchases.
""")

st.markdown("---")


# ---------------------------------------------------------
# #### 6. Monthly and Seasonal Sales Trends
# ---------------------------------------------------------
st.subheader("6. Monthly and Seasonal Sales Trends")

st.markdown("""
Are there seasonal or monthly trends in sales performance?
""")

st.markdown("##### Business Analysis")

monthly_sales = (
    df.groupby(['transaction_year', 'transaction_month_name'])
      .agg(total_revenue=('total_spent', 'sum'))
      .reset_index()
)

monthly_sales = monthly_sales[:-1]

st.dataframe(monthly_sales, use_container_width=True)

st.markdown("##### Visualization – Monthly Trend")

fig = px.line(
    monthly_sales,
    x='transaction_month_name',
    y='total_revenue',
    markers=True,
    color='transaction_year',
    title='Monthly Sales Trend by Year',
    labels={
        'transaction_month_name': 'Month',
        'total_revenue': 'Total Revenue',
        'transaction_year': 'Year'
    },
    hover_data={
        'transaction_year': True,
        'total_revenue': ':.2f'
    }
)

fig.update_layout(
    title_x=0.5,
    xaxis={
        'categoryorder': 'array',
        'categoryarray': [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    }
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Data insights**

- **Monthly revenue** remains relatively **stable** across years, mostly ranging between **38k and 55k**, indicating **consistent sales performance**.

- **March 2023 (55k)** and **December 2023 (52k)** show some of the **highest revenue** levels, while **April 2022 (38k)** and **June 2024 (38k)** reflect noticeable dips, suggesting moderate seasonal fluctuations.

- Overall, revenue trends across **2022, 2023**, and **2024** show **steady performance with periodic peaks in mid-year and year-end months**.
""")

st.markdown("---")


# ---------------------------------------------------------
# ### Final business recommendations
# ---------------------------------------------------------
st.header("Final business recommendations")

st.markdown("""
- Since Food, Beverages, and Milk Products drive the majority of revenue, the business should **prioritize inventory planning and marketing efforts** toward these **high-performing categories to bring highest sales**.
- As revenue is heavily concentrated in Digital Wallet payments, the **business should strengthen partnerships, cashback offers, and loyalty programs within digital channels while gradually encouraging diversification** to reduce payment risk.
- Customers buy more when there are discounts, the **store should strategically use targeted discount campaigns during slow months to increase sales**.
- Since online sales significantly outperform in-store sales, the **business should further invest in optimizing the online experience, including faster checkout, personalized recommendations, and digital marketing**.
- **Sales** are usually **higher** in March and December, so **prepare more stock and offers during these months to earn more**.
""")

st.markdown("---")