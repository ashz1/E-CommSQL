import sqlite3
import streamlit as st
import pandas as pd
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')
conn = sqlite3.connect('ecom.db')



# Function to create database and insert data from CSV
def create_database():
    fdf.to_sql('flipkart', conn, if_exists="replace", index=False)
    adf.to_sql('amazon', conn, if_exists="replace", index=False)
    conn.commit()

# Function to search data in the database
def search_data(table, column, value):
    query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
    return pd.read_sql(query, conn, params=[f'%{value}%'])

# Function to view all data in a table
def view_data(table):
    query = f"SELECT * FROM {table}"
    return pd.read_sql(query, conn)

# Function to update data in the database
def update_data(table, column, old_value, new_value):
    query = f"UPDATE {table} SET {column} = ? WHERE {column} = ?"
    cur = conn.cursor()
    cur.execute(query, (new_value, old_value))
    conn.commit()
    cur.close()

# Function to delete data from the database
def delete_data(table, column, value):
    query = f"DELETE FROM {table} WHERE {column} = ?"
    cur = conn.cursor()
    cur.execute(query, (value,))
    conn.commit()
    cur.close()
def aggregate_data(table, operation, column):
    try:
        query = f"SELECT {operation}({column}) as result FROM {table}"
        print(f"Executing query: {query}")
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error executing query: {query}\nException: {e}")
        return None

# Function to perform join queries
def join_data():
    query = """
    SELECT f.*, a.*
    FROM flipkart f
    JOIN amazon a ON f.Month = a.Month
    """
    return pd.read_sql(query, conn)

# Main Streamlit app
def main():
    st.title("SQL Database Operations Demo by Aashay")

    # Create database and insert data from CSV if not already created
    create_database()

    # View operations
    st.sidebar.header("View Operations: 'SELECT * FROM {table}'")
    table_to_view = st.sidebar.selectbox("Choose a table to view", ["flipkart", "amazon"], key="view_table")

    if st.sidebar.button("Click here to view"):
        result = view_data(table_to_view)
        st.header(f"Data in {table_to_view} Table:")
        st.write(result)

    # Search operations
    st.sidebar.header("Search Operations: 'SELECT * FROM {table} WHERE {column} LIKE ?'")
    table = st.sidebar.selectbox("Choose a table", ["flipkart", "amazon"])
    column = st.sidebar.selectbox("Choose a column", ["Month", "Gross Transactions (Mn)", "Shipped Transactions (Mn)", "Checkout GMV (USD Mn)", "Shipped GMV (USD Mn)", "Fulfilled GMV i.e. GMV post Return (USD Mn)", "Average Order Value per transaction (USD)", "ASP per item (USD)", "Mobiles (USD Mn)", "Electronic Devices (USD Mn)", "Large & Small Appliances (USD Mn)", "% COD", "% Prepaid", "Orders shipped per day Lacs", "% Returns(RTO+RVP)", "% share of Captive", "% share of 3PL", "% Metro", "% Tier-I", "% Others", "Revenue from Operations (Take Rate + Delivery Charges ) (USD Mn)", "Other Revenue (USD Mn)", "Total Revenue (USD Mn)", "Supply Chain Costs (Fixed and Variable Included) (USD Mn)", "Payment Gateway Costs (Only on the Pre-paid orders) (USD Mn)", "Marketing Expediture (USD Mn)", "Contribution Margin (as % of Fulfilled GMV)", "Tech & Admin/Employee Costs and other costs (USD Mn)", "Cash Burn (USD Mn)"])  # Adjust according to your table schema
    value = st.sidebar.text_input("Search value")

    if st.sidebar.button("Click here to search"):
        result = search_data(table, column, value)
        st.header(f"Search Results in {table} for '{value}' in column '{column}':")
        st.write(result)

    # Update operations
    st.sidebar.header("Update Operations: 'UPDATE {table} SET {column} = ? WHERE {column} = ?'")
    table_to_update = st.sidebar.selectbox("Choose a table to update", ["flipkart", "amazon"], key="update_table")
    column_to_update = st.sidebar.selectbox("Choose a column to update", [
        "Month", "Gross Transactions (Mn)", "Shipped Transactions (Mn)", "Checkout GMV (USD Mn)", "Shipped GMV (USD Mn)", 
        "Fulfilled GMV i.e. GMV post Return (USD Mn)", "Average Order Value per transaction (USD)", "ASP per item (USD)", 
        "Mobiles (USD Mn)", "Electronic Devices (USD Mn)", "Large & Small Appliances (USD Mn)", "% COD", "% Prepaid", 
        "Orders shipped per day Lacs", "% Returns(RTO+RVP)", "% share of Captive", "% share of 3PL", "% Metro", "% Tier-I", 
        "% Others", "Revenue from Operations (Take Rate + Delivery Charges ) (USD Mn)", "Other Revenue (USD Mn)", 
        "Total Revenue (USD Mn)", "Supply Chain Costs (Fixed and Variable Included) (USD Mn)", 
        "Payment Gateway Costs (Only on the Pre-paid orders) (USD Mn)", "Marketing Expediture (USD Mn)", 
        "Contribution Margin (as % of Fulfilled GMV)", "Tech & Admin/Employee Costs and other costs (USD Mn)", "Cash Burn (USD Mn)"
    ], key="update_column")
    old_value = st.sidebar.text_input("Old value")
    new_value = st.sidebar.text_input("New value")

    if st.sidebar.button("Click here to update"):
        update_data(table_to_update, column_to_update, old_value, new_value)
        st.sidebar.text("Data updated successfully")
        result = view_data(table_to_update)
        st.write(result)

    # Delete operations
    st.sidebar.header("Delete Operations: 'DELETE FROM {table} WHERE {column} = ?'")
    table_to_delete = st.sidebar.selectbox("Choose a table to delete from", ["flipkart", "amazon"], key="delete_table")
    column_to_delete = st.sidebar.selectbox("Choose a column to delete from", [
        "Month", "Gross Transactions (Mn)", "Shipped Transactions (Mn)", "Checkout GMV (USD Mn)", "Shipped GMV (USD Mn)", 
        "Fulfilled GMV i.e. GMV post Return (USD Mn)", "Average Order Value per transaction (USD)", "ASP per item (USD)", 
        "Mobiles (USD Mn)", "Electronic Devices (USD Mn)", "Large & Small Appliances (USD Mn)", "% COD", "% Prepaid", 
        "Orders shipped per day Lacs", "% Returns(RTO+RVP)", "% share of Captive", "% share of 3PL", "% Metro", "% Tier-I", 
        "% Others", "Revenue from Operations (Take Rate + Delivery Charges ) (USD Mn)", "Other Revenue (USD Mn)", 
        "Total Revenue (USD Mn)", "Supply Chain Costs (Fixed and Variable Included) (USD Mn)", 
        "Payment Gateway Costs (Only on the Pre-paid orders) (USD Mn)", "Marketing Expediture (USD Mn)", 
        "Contribution Margin (as % of Fulfilled GMV)", "Tech & Admin/Employee Costs and other costs (USD Mn)", "Cash Burn (USD Mn)"
    ], key="delete_column")
    value_to_delete = st.sidebar.text_input("Value to delete")

    if st.sidebar.button("Click here to delete"):
        delete_data(table_to_delete, column_to_delete, value_to_delete)
        st.sidebar.text("Data deleted successfully")
        result = view_data(table_to_delete)
        st.write(result)
    
    # Aggregation operations
    st.sidebar.header("Aggregation Operations: 'SELECT {operation}({column}) FROM {table}'")
    agg_operation = st.sidebar.selectbox("Choose an aggregation operation", ["SUM", "AVG", "MAX", "MIN", "COUNT"], key="agg_operation")
    agg_table = st.sidebar.selectbox("Choose a table", ["flipkart", "amazon"], key="agg_table")
    agg_column = st.sidebar.selectbox("Choose a column to aggregate", fdf.columns.tolist() if agg_table == "flipkart" else adf.columns.tolist(), key="agg_column")

    if st.sidebar.button("Click here to aggregate"):
        result = aggregate_data(agg_table, agg_operation, agg_column)
        if result is not None:
            st.header(f"Aggregation Result in {agg_table} for '{agg_operation}({agg_column})':")
            st.write(result)

    # Join operations
    st.sidebar.header("Join Operations: 'SELECT * FROM flipkart JOIN amazon ON flipkart.Month = amazon.Month'")
    if st.sidebar.button("Click here to join"):
        result = join_data()
        st.header(f"Join Result between Flipkart and Amazon Tables:")
        st.write(result)
    conn.close()

if __name__ == '__main__':
    main()