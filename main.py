# Imports required ---
import streamlit as st
import sqlite3 as sqlite
import pandas as pd
# import plotly.express as px 

## Instructions:
# Go in Shell (on the right)
# write "pip install --upgrade streamlit"
# launch with "streamlit run main.py"

@st.cache_data
# Fetching data function
def get_data():
    con = sqlite.connect("Fake_sales_data.db")
    data = pd.read_sql_query("SELECT * from  SalesA", con)
    con.close() # close the database connection
    return data


# Fetching data
data = get_data()
data['company'] = data['company'].astype('string')
data['cat'] = data['cat'].astype('string')

st.title('Sales Dashboard')
st.write(f"We have {len(data)} datapoints")

# Company selection
company = st.selectbox("Select a Company", data["company"].unique(), index=0)

# Category selection
category = st.multiselect("Select a Category", data["cat"].unique(), default="Young")

# Data filtering
data_selection = data.query("company == @company & cat == @category")

# 1st Chart for Products Sold
st.write(f"Products Sold for {company} of {category} category:")

st.write(f"We have {len(data_selection)} datapoints")

no_prod_sold = data_selection[['cat', 'price']].value_counts().reset_index()
no_prod_sold.columns = [*no_prod_sold.columns[:-1], 'count']

st.bar_chart(no_prod_sold,x='price',y='count')
# plot_bar = px.bar(no_prod_sold,
#                   x='price',
#                   y='count',
#                   color='cat',
#                   title='<b>Number of Units Sold for Different Products</b>',
#                   labels={
#                       "price": "Product Price",
#                       "count": "Number of Units Sold"
#                   })
# st.plotly_chart(plot_bar)

# ----------------------------------------------------------------------------------------
st.write(f"Volume of Sales for {category} :")
volume = data_selection["price"].count()
st.write(volume)

# ----------------------------------------------------------------------------------------
#revenue
st.write(f"Revenue for {category} :")
data_selection['price'] = data['price'].astype('float')
revenue = data_selection["price"].sum()
st.write(revenue)

# Volume of sales
volume_per_week = data_selection.groupby(["week"])["price"].count().reset_index()

# The revenues
sum_per_week = data_selection.groupby(["week"])["price"].sum().reset_index()

# ----------------------------------------------------------------------------------------
# plot volume & revenue through time
tab1, tab2 = st.tabs(["Volume", "Revenue"])

with tab1:
    figvol = st.line_chart(volume_per_week,
                   x="week",
                   y="price")
    # st.plotly_chart(figvol)

with tab2:
    figrev = st.line_chart(sum_per_week,
                   x="week",
                   y="price")
    # st.plotly_chart(figrev)





