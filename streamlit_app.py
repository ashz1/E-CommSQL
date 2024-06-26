import sqlite3
import streamlit as st
import pandas as pd
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')
conn = sqlite3.connect('ecom.db')
st.title("SQL Database Operations Demo by Aashay")
st.write("""Introduction:
I've created a simple CRUD SQL demo app using SQLite3 to demonstrate SQL queries. This data is based on my experience as a business and data analyst in India, although I've altered it significantly for demonstration purposes.

App Overview:
The app, built using Python's Streamlit library, allows users to perform basic CRUD (Create, Read, Update, Delete) operations on two datasets: one from Flipkart and one from Amazon. It provides an interactive interface for viewing, searching, updating, and deleting data, along with the SQL queries used. 
The code can be viewed on github, under the MIT license, feel free to use it for your own projects and please do not hesitate to drop me an email if you find any errors or have feedback, I'll appreciate it.
""")


# Function to create database and insert data from CSV
def create_database():
    fdf.to_sql('flipkart', conn, if_exists="replace", index=False)
    adf.to_sql('amazon', conn, if_exists="replace", index=False)
    conn.commit()

# Function to search data in the database
def search_data(table, column, value):
    if table == 'both':
        query_flipkart = f"SELECT * FROM flipkart WHERE {column} LIKE ?"
        query_amazon = f"SELECT * FROM amazon WHERE {column} LIKE ?"
        result_flipkart = pd.read_sql(query_flipkart, conn, params=[f'%{value}%'])
        result_amazon = pd.read_sql(query_amazon, conn, params=[f'%{value}%'])
        return pd.concat([result_flipkart, result_amazon])
    else:
        query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
        return pd.read_sql(query, conn, params=[f'%{value}%'])

# Function to view all data in a table
def view_data(table):
    if table == 'both':
        query_flipkart = f"SELECT * FROM flipkart"
        query_amazon = f"SELECT * FROM amazon"
        result_flipkart = pd.read_sql(query_flipkart, conn)
        result_amazon = pd.read_sql(query_amazon, conn)
        return pd.concat([result_flipkart, result_amazon])
    else:
        query = f"SELECT * FROM {table}"
        return pd.read_sql(query, conn)

# Function to delete data from the database
def delete_data(table, column, value):
    query = f"DELETE FROM {table} WHERE {column} = ?"
    cur = conn.cursor()
    cur.execute(query, (value,))
    conn.commit()
    cur.close()

# Function to aggregate data in the database
def aggregate_data(table, columns, method):
    cols = ", ".join([f'"{col}"' for col in columns])
    agg_query = ", ".join([f'{method}("{col}") AS {method}_{col.replace(" ", "_").replace("(", "").replace(")", "")}' for col in columns])
    if table == 'both':
        query_flipkart = f'SELECT {agg_query} FROM flipkart'
        query_amazon = f'SELECT {agg_query} FROM amazon'
        result_flipkart = pd.read_sql(query_flipkart, conn)
        result_amazon = pd.read_sql(query_amazon, conn)
        return pd.concat([result_flipkart, result_amazon])
    else:
        query = f'SELECT {agg_query} FROM {table}'
        return pd.read_sql(query, conn)
    
# Main Streamlit app
def main():
    

    # Create database and insert data from CSV if not already created
    create_database()

    # View operations
    st.sidebar.header("View Operations: 'SELECT * FROM {table}'")
    table_to_view = st.sidebar.selectbox("Choose a table to view", ["flipkart", "amazon", "both"], key="view_table")

    if st.sidebar.button("Click here to view"):
        result = view_data(table_to_view)
        st.header(f"Data in {table_to_view} Table:")
        st.write(result)

    # Search operations
    st.sidebar.header("Search Operations: 'SELECT * FROM {table} WHERE {column} LIKE ?'")
    table = st.sidebar.selectbox("Choose a table", ["flipkart", "amazon", "both"])
    column = st.sidebar.selectbox("Choose a column", fdf.columns.tolist())
    value = st.sidebar.text_input("Search value")

    if st.sidebar.button("Click here to search"):
        result = search_data(table, column, value)
        st.header(f"Search Results in {table} for '{value}' in column '{column}':")
        st.write(result)

    # Update operations
    st.sidebar.header("Update Operations: 'UPDATE {table} SET {column} = ? WHERE {column} = ?'")
    table_to_update = st.sidebar.selectbox("Choose a table to update", ["flipkart", "amazon"], key="update_table")
    column_to_update = st.sidebar.selectbox("Choose a column to update", fdf.columns.tolist(), key="update_column")
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
    column_to_delete = st.sidebar.selectbox("Choose a column to delete from", fdf.columns.tolist(), key="delete_column")
    value_to_delete = st.sidebar.text_input("Value to delete")

    if st.sidebar.button("Click here to delete"):
        delete_data(table_to_delete, column_to_delete, value_to_delete)
        st.sidebar.text("Data deleted successfully")
        result = view_data(table_to_delete)
        st.write(result)

    # Aggregation operations
    st.sidebar.header("Aggregation Operations")
    table_to_aggregate = st.sidebar.selectbox("Choose a table to aggregate", ["flipkart", "amazon", "both"], key="aggregate_table")
    columns_to_aggregate = st.sidebar.multiselect("Choose columns to aggregate", fdf.columns.tolist())
    aggregation_method = st.sidebar.selectbox("Choose an aggregation method", ["SUM", "AVG", "COUNT"])

    if st.sidebar.button("Aggregate"):
        result = aggregate_data(table_to_aggregate, columns_to_aggregate, aggregation_method)
        st.header(f"Aggregation Results for {table_to_aggregate} from January 21 to March 22:")
        st.write(result)
    conn.close()
    
if __name__ == '__main__':
    main()
