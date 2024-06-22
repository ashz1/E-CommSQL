import sqlite3
import streamlit as st
import pandas as pd
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')
conn = sqlite3.connect('ecom.db')



# Function to create database and insert data from CSV
def create_database():
    fdf.to_sql('flipkart', conn, if_exists="fail", index=False)
    adf.to_sql('amazon', conn, if_exists="fail", index=False)
    conn.commit()

# Function to search data in the database
def search_data(table, column, value):
    query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
    return pd.read_sql(query, conn, params=[f'%{value}%'])

# Function to view all data in a table
def view_data(table):
    query = f"SELECT * FROM {table}"
    return pd.read_sql(query, conn)

# Main Streamlit app
def main():
    st.title("E-commerce Database App")

    # Create database and insert data from CSV if not already created
    create_database()



    # Search operations
    st.sidebar.header("Search Operations")
    table = st.sidebar.selectbox("Choose a table", ["flipkart", "amazon"])
    column = st.sidebar.selectbox("Choose a column", [
    "Month",
    "Gross Transactions (Mn)",
    "Shipped Transactions (Mn)",
    "Checkout GMV (USD Mn)",
    "Shipped GMV (USD Mn)",
    "Fulfilled GMV i.e. GMV post Return (USD Mn)",
    "Average Order Value per transaction  (USD)",
    "ASP per item (USD)",
    "Mobiles (USD Mn)",
    "Electronic Devices (USD Mn)",
    "Large & Small Appliances (USD Mn)",
    "% COD",
    "% Prepaid",
    "Orders shipped per day Lacs",
    "% Returns(RTO+RVP)",
    "% share of Captive",
    "% share of 3PL",
    "% Metro",
    "% Tier-I",
    "% Others",
    "Revenue from Operations (Take Rate + Delivery Charges ) (USD Mn)",
    "Other Revenue (USD Mn)",
    "Total Revenue (USD Mn)",
    "Supply Chain Costs (Fixed and Variable Included) (USD Mn)",
    "Payment Gateway Costs (Only on the Pre-paid orders) (USD Mn)",
    "Marketing Expediture (USD Mn)",
    "Contribution Margin (as % of Fulfilled GMV)",
    "Tech & Admin/Employee Costs and other costs (USD Mn)",
    "Cash Burn (USD Mn)"
])  
    value = st.sidebar.text_input("Search value")

    if st.sidebar.button("Search"):
        result = search_data(table, column, value)
        st.header(f"Search Results in {table} for '{value}' in column '{column}':")
        st.write(result)

    # View operations
    st.sidebar.header("View Operations")
    table_to_view = st.sidebar.selectbox("Choose a table to view", ["flipkart", "amazon"], key="view_table")

    if st.sidebar.button("View"):
        result = view_data(table_to_view)
        st.header(f"Data in {table_to_view} Table:")
        st.write(result)

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()