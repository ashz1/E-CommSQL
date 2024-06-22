import sqlite3
import streamlit as st
import pandas as pd

def create_database():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    # Check if 'customers' table exists in the database
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='customers'")
    if c.fetchone()[0] == 0:
        c.execute('''CREATE TABLE customers
                     (name text, address text, phone text)''')
        conn.commit()
    conn.close()

def import_csv_to_database(csv_file):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect('customers.db')
    df.to_sql('customers', conn, if_exists='append', index=False)
    conn.close()

# Streamlit UI
st.title("CSV to SQLite Importer")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    create_database()
    import_csv_to_database(uploaded_file)
    st.success("CSV data imported successfully!")
