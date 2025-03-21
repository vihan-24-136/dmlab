import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data creation with specific product names
def create_sample_data():
    years = np.arange(2018, 2024)
    products = [
        ("Smartphone", "Electronics"),
        ("Laptop", "Electronics"),
        ("Tablet", "Electronics"),
        ("T-shirt", "Clothing"),
        ("Jeans", "Clothing"),
        ("Jacket", "Clothing"),
        ("Pizza", "Food"),
        ("Pasta", "Food"),
        ("Soda", "Food"),
        ("Fiction Book", "Books"),
        ("Non-Fiction Book", "Books"),
        ("Textbook", "Books"),
        ("Headphones", "Electronics"),
        ("Smartwatch", "Electronics"),
        ("Sneakers", "Clothing"),
        ("Chips", "Food"),
        ("Candy", "Food"),
        ("Novel", "Books"),
        ("Cookbook", "Books"),
        ("Dress", "Clothing")
    ]
    
    sales_data = {
        "Year": np.repeat(years, len(products)),
        "Product": [product[0] for product in products for _ in years],
        "Type": [product[1] for product in products for _ in years],
        "Sales": np.random.randint(100, 1000, size=len(years) * len(products))
    }
    return pd.DataFrame(sales_data)

# Load sample data
data = create_sample_data()

# Set page title and icon
st.set_page_config(page_title="Retail Sales Analysis", page_icon="🏬")

# Sidebar for user input
st.sidebar.title("Filter Sales Data")

# Slider for year selection
selected_year = st.sidebar.selectbox("Select Year", options=data["Year"].unique())

# Slider for minimum sales value
min_sales = st.sidebar.slider("Minimum Sales", min_value=0, max_value=int(data["Sales"].max()), value=200)

# Slider for number of products to display
num_products = st.sidebar.slider("Number of Products to Display", min_value=1, max_value=20, value=5)

# Multi-select for product types
selected_types = st.sidebar.multiselect("Select Product Types", options=data["Type"].unique(), default=data["Type"].unique())

# Filter data based on user input
filtered_data = data[(data["Year"] == selected_year) & (data["Sales"] >= min_sales) & (data["Type"].isin(selected_types))]
filtered_data = filtered_data.head(num_products)  # Limit to the selected number of products

# Main title
st.title("Retail Sales Analysis App")

# Display filtered results
st.write(f"**Filtered Results for Year {selected_year} with Minimum Sales {min_sales}:**")
st.dataframe(filtered_data)

# Create tabs for different visualizations
tabs = st.tabs(["Sales Bar Chart", "Sales Line Chart"])

with tabs[0]:
    st.subheader("Sales Bar Chart")
    sales_summary = filtered_data.groupby("Product").sum().reset_index()
    fig, ax = plt.subplots()
    ax.bar(sales_summary["Product"], sales_summary["Sales"], color='orange')
    ax.set_xlabel("Product")
    ax.set_ylabel("Sales")
    ax.set_title("Sales by Product")
    st.pyplot(fig)

with tabs[1]:
    st.subheader("Sales Line Chart")
    sales_trend = data[data["Product"].isin(filtered_data["Product"])].groupby("Year").sum().reset_index()
    fig2, ax2 = plt.subplots()
    ax2.plot(sales_trend["Year"], sales_trend["Sales"], marker='o', color='green')
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Sales")
    ax2.set_title("Sales Trend Over Years")
    st.pyplot(fig2)

# Footer
st.write("Analysing sales data made easy! ")
