import sqlite3
import streamlit as st
import pandas as pd
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')
conn = sqlite3.connect('ecom.db')



# Function to create database and insert data from CSV
def create_database():
    fdf.to_sql('flipkart', conn, if_exists="append", index=False)
    adf.to_sql('amazon', conn, if_exists="append", index=False)
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

    # Display existing data
    st.write("Existing Data:")
    st.write("Flipkart Table:")
    st.write(view_data('flipkart'))
    st.write("Amazon Table:")
    st.write(view_data('amazon'))

    # Search operations
    st.sidebar.header("Search Operations")
    table = st.sidebar.selectbox("Choose a table", ["flipkart", "amazon"])
    column = st.sidebar.selectbox("Choose a column", ["name", "price"])  # Adjust according to your table schema
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