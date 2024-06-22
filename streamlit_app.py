import sqlite3
import streamlit as st
import pandas as pd
fdf = pd.read_csv('data/1.csv')
adf = pd.read_csv('data/2.csv')
conn = sqlite3.connect('ecom.db')

fdf.to_sql('flipkart', conn, if_exists="append")
adf.to_sql('amazon', conn, if_exists="append")

st.write("Existing Data:")
st.write("SELECT * FROM flipkart")
st.write(pd.read_sql('SELECT * FROM flipkart', conn))
st.write("SELECT * FROM amazon")
st.write(pd.read_sql('SELECT * FROM amazon', conn))

def add_customer(name, address, phone):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("INSERT INTO customers VALUES (?, ?, ?)", (name, address, phone))
    conn.commit()
    conn.close()

def delete_customer(name):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE name=?", (name,))
    conn.commit()
    conn.close()

def update_customer(name, address, phone):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("UPDATE customers SET address = ?, phone = ? WHERE name = ?", (address, phone, name))
    conn.commit()
    conn.close()

def view_customers():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    customers = c.fetchall()
    conn.close()
    return customers

def search_customer(name, phone):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE name=? OR phone=?", (name, phone))
    customers = c.fetchall()
    conn.close()
    return customers


def main():
    st.title("Customer Database App")
    
    
    create_database()

    name = st.text_input("Name")
    address = st.text_input("Address")
    phone = st.text_input("Phone Number")
    st.sidebar.header("Click for operations")
    if st.sidebar.button("Add"):
        add_customer(name, address, phone)

    if st.sidebar.button("Delete"):
        delete_customer(name)

    if st.sidebar.button("Update"):
        update_customer(name, address, phone)


    if st.sidebar.button("Search"):
        customers = search_customer(name, phone)
        st.header("Customers File")
        st.table(customers)   

    if st.sidebar.button("View"):
        customers = view_customers()
        st.header("Customers File")
        st.table(customers)

if __name__ == '__main__':
    main()
