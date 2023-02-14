# Imports required ---
import streamlit as st
import sqlite3 as sqlite
import pandas as pd

## Instructions 
#streamlit run main.py
@st.cache_data
def get_data():
  
  con = sqlite.connect("Fake_sales_data.db")
  data = pd.read_sql_query("SELECT * from SalesA",con)
  return data
  
data = get_data()  

st.title('sales Dashboard')

st.write(f"we have{len(data)} datapoints")

choice = st.selectbox("select a company",
data["company"].unique(),index=0)


new_data = data[data["company"] == choice]

st.write(new_data.head())
st.write(f"sum of sales{choice}:")
sperweek = new_data.groupby("week")["price"].sum()

st.write(sperweek)
st.write(new_data["price"].sum())
st.line_chart(sperweek, y="price")

options =st.multiselect()


