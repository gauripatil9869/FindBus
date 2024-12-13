import mysql.connector
import streamlit as st

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="redbus",
        port=3307
    )
    if connection.is_connected():
        st.title("Connected to the Database!")
        db_info = connection.get_server_info()
        st.info(f"Connected to MySQL server version: {db_info}")
except mysql.connector.Error as e:
    st.error(f"MySQL Error: {e}")
except Exception as e:
    st.error(f"General Error: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        st.info("Database connection closed.")
