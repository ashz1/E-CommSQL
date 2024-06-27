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
# Add a new column to identify the source
fdf['Source'] = 'Flipkart'
adf['Source'] = 'Amazon'
# Reorder columns to place 'Source' after 'Month'
cols = fdf.columns.tolist()
cols.insert(cols.index('Month') + 1, cols.pop(cols.index('Source')))
fdf = fdf[cols]
adf = adf[cols]
# Function to create database and insert data from CSV
def create_database():
    fdf.to_sql('flipkart', conn, if_exists="replace", index=False)
    adf.to_sql('amazon', conn, if_exists="replace", index=False)
    conn.commit()

def search_data(table, column, value):
    if table == 'both':
        query_flipkart = f"SELECT * FROM flipkart WHERE {column} LIKE ?"
        query_amazon = f"SELECT * FROM amazon WHERE {column} LIKE ?"
        result_flipkart = pd.read_sql(query_flipkart, conn, params=[f'%{value}%'])
        result_amazon = pd.read_sql(query_amazon, conn, params=[f'%{value}%'])
        result = pd.concat([result_flipkart, result_amazon])
    else:
        query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
        result = pd.read_sql(query, conn, params=[f'%{value}%'])
    return result[['Month', 'Source'] + [col for col in result.columns if col not in ['Month', 'Source']]]

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

def aggregate_data(table, columns, method):
    cols = ", ".join([f'"{col}"' for col in columns])
    agg_query = ", ".join([f'{method}("{col}") AS {method}_{col.replace(" ", "_").replace("(", "").replace(")", "")}' for col in columns])
    if table == 'both':
        query_flipkart = f'SELECT "Month", "Source", {agg_query} FROM flipkart'
        query_amazon = f'SELECT "Month", "Source", {agg_query} FROM amazon'
        result_flipkart = pd.read_sql(query_flipkart, conn)
        result_amazon = pd.read_sql(query_amazon, conn)
        return pd.concat([result_flipkart, result_amazon])
    else:
        query = f'SELECT "Month", "Source", {agg_query} FROM {table}'
        return pd.read_sql(query, conn)
    
# Function to update data in the database
def update_data(table, column, old_value, new_value):
    query = f"UPDATE {table} SET {column} = ? WHERE {column} = ?"
    cur = conn.cursor()
    cur.execute(query, (new_value, old_value))
    conn.commit()
    cur.close()

def join_data(join_type):
    # Add prefixes to the columns of each table
    fdf_prefixed = fdf.add_prefix('FLP_')
    adf_prefixed = adf.add_prefix('AMZN_')

    # Merge the datasets
    fdf_prefixed.to_sql('flipkart_prefixed', conn, if_exists="replace", index=False)
    adf_prefixed.to_sql('amazon_prefixed', conn, if_exists="replace", index=False)

    if join_type == "RIGHT JOIN":
        join_query = f"""
        SELECT amazon_prefixed.AMZN_Month as Month, flipkart_prefixed.*, amazon_prefixed.AMZN_Month, amazon_prefixed.*
        FROM amazon_prefixed
        LEFT JOIN flipkart_prefixed
        ON flipkart_prefixed.FLP_Month = amazon_prefixed.AMZN_Month
        """
    elif join_type == "FULL OUTER JOIN":
        join_query = f"""
        SELECT flipkart_prefixed.FLP_Month as Month, flipkart_prefixed.*, amazon_prefixed.AMZN_Month, amazon_prefixed.*
        FROM flipkart_prefixed
        LEFT JOIN amazon_prefixed
        ON flipkart_prefixed.FLP_Month = amazon_prefixed.AMZN_Month
        UNION
        SELECT amazon_prefixed.AMZN_Month as Month, flipkart_prefixed.*, amazon_prefixed.AMZN_Month, amazon_prefixed.*
        FROM amazon_prefixed
        LEFT JOIN flipkart_prefixed
        ON flipkart_prefixed.FLP_Month = amazon_prefixed.AMZN_Month
        """
    else:
        join_query = f"""
        SELECT flipkart_prefixed.FLP_Month as Month, flipkart_prefixed.*, amazon_prefixed.AMZN_Month, amazon_prefixed.*
        FROM flipkart_prefixed
        {join_type} amazon_prefixed
        ON flipkart_prefixed.FLP_Month = amazon_prefixed.AMZN_Month
        """
    
    result = pd.read_sql(join_query, conn)
    
    # Remove duplicate 'Month' columns and 'Source' columns
    result = result.loc[:, ~result.columns.duplicated()]
    result = result.drop(columns=['FLP_Source', 'AMZN_Source'], errors='ignore')
    
    return result, join_query

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
        with st.container():
         st.write("""
            SQL CREATE VIEW Statement
             
                 In SQL, a view is a virtual table based on the result-set of an SQL statement.

             
                 A view contains rows and columns, just like a real table. The fields in a view are fields from one or more real tables in the database.

                 You can add SQL statements and functions to a view and present the data as if the data were coming from one single table. """)
         st.write("""
            A view is created with the CREATE VIEW statement. 
                 CREATE VIEW Syntax
                 CREATE VIEW view_name AS
                 SELECT column1, column2, ...
                 FROM table_name
                 WHERE condition;""")
         st.write(""" 
                 Note: A view always shows up-to-date data! The database engine recreates the view, every time a user queries it.""")
        st.write(result)

    # Search operations
    st.sidebar.header("Search Operations: 'SELECT * FROM {table} WHERE {column} LIKE ?'")
    table = st.sidebar.selectbox("Choose a table", ["flipkart", "amazon", "both"])
    column = st.sidebar.selectbox("Choose a column", fdf.columns.tolist())
    value = st.sidebar.text_input("Search value")

    if st.sidebar.button("Click here to search"):
        result = search_data(table, column, value)
        st.header(f"Search Results in {table} for '{value}' in column '{column}':")
        st.write("""
            The SQL LIKE Operator
                     The LIKE operator is used in a WHERE clause to search for a specified pattern in a column.
                     There are two wildcards often used in conjunction with the LIKE operator: 
                     The percent sign % represents zero, one, or multiple characters. The underscore sign _ represents one, single character
            Syntax
                     SELECT column1, column2, ...
                     FROM table_name
                     WHERE columnN LIKE pattern;
            Contains
                     To return records that contains a specific letter or phrase, add the % both before and after the letter or phrase.
            Combine Wildcards
                     Any wildcard, like % and _ , can be used in combination with other wildcards.       
            Without Wildcard 
                     If no wildcard is specified, the phrase has to have an exact match to return a result.
                 """)
        st.write(result)


    # Update operations
    st.sidebar.header("Update Operations: 'UPDATE {table} SET {column} = ? WHERE {column} = ?'")
    table_to_update = st.sidebar.selectbox("Choose a table to update", ["flipkart", "amazon"], key="update_table")
    column_to_update = st.sidebar.selectbox("Choose a column to update", [
        "Month", "Source", "Gross Transactions (Mn)", "Shipped Transactions (Mn)", "Checkout GMV (USD Mn)", "Shipped GMV (USD Mn)", 
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
        "Month", "Source", "Gross Transactions (Mn)", "Shipped Transactions (Mn)", "Checkout GMV (USD Mn)", "Shipped GMV (USD Mn)", 
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
    st.sidebar.header("Aggregate Operations: 'SELECT {aggregation}({column}) FROM {table}'")
    table_to_aggregate = st.sidebar.selectbox("Choose a table to aggregate", ["flipkart", "amazon", "both"], key="aggregate_table")
    columns_to_aggregate = st.sidebar.multiselect("Choose columns to aggregate", [col for col in fdf.columns.tolist() if col not in ['Month', 'Source']])
    method = st.sidebar.selectbox("Choose an aggregation method", ["SUM", "AVG", "COUNT", "MAX", "MIN"])

    if st.sidebar.button("Click here to aggregate"):
        result = aggregate_data(table_to_aggregate, columns_to_aggregate, method)
        st.header(f"Aggregation Results in {table_to_aggregate} using '{method}':")
        st.write(result)

    # Join operations
    st.sidebar.header("Join Operations")
    st.sidebar.write("Different types of JOIN operations:")
    st.sidebar.write("1. INNER JOIN: Selects records that have matching values in both tables.")
    st.sidebar.write("2. LEFT JOIN: Selects all records from the left table, and the matched records from the right table.")
    st.sidebar.write("3. RIGHT JOIN: Selects all records from the right table, and the matched records from the left table (simulated).")
    st.sidebar.write("4. FULL OUTER JOIN: Selects all records when there is a match in either left or right table (simulated).")

    join_type_dict = {
        "INNER JOIN": "INNER JOIN",
        "LEFT JOIN": "LEFT JOIN",
        "RIGHT JOIN": "RIGHT JOIN",
        "FULL OUTER JOIN": "FULL OUTER JOIN"
    }

    if st.sidebar.button("Perform INNER JOIN"):
        result, query = join_data(join_type_dict["INNER JOIN"])
        st.header("INNER JOIN Results:")
        st.subheader("Query:")
        st.code(query, language='sql')
        st.write(result)

    if st.sidebar.button("Perform LEFT JOIN"):
        result, query = join_data(join_type_dict["LEFT JOIN"])
        st.header("LEFT JOIN Results:")
        st.subheader("Query:")
        st.code(query, language='sql')
        st.write(result)

    if st.sidebar.button("Perform RIGHT JOIN"):
        result, query = join_data("RIGHT JOIN")
        st.header("RIGHT JOIN Results:")
        st.subheader("Query:")
        st.code(query, language='sql')
        st.write(result)

    if st.sidebar.button("Perform FULL OUTER JOIN"):
        result, query = join_data("FULL OUTER JOIN")
        st.header("FULL OUTER JOIN Results:")
        st.subheader("Query:")
        st.code(query, language='sql')
        st.write(result)


    
    conn.close()
    
if __name__ == '__main__':
    main()
