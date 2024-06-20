import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title='E-commerce Dashboard', page_icon='📊')
st.title('📊 E-commerce Dashboard')

with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation, and editable dataframes for data interaction.')
    st.markdown('**How to use the app?**')
    st.warning('To engage with the app, 1. Select a data source and categories of interest, then 2. Select the date range from the slider widget. This should generate an updated editable DataFrame and a line plot.')

st.subheader('E-commerce Performance Analysis')


# Load datasets
flipkart_df = pd.read_excel('data/1.eTailing_Flipkart.xlsx')
amazon_df = pd.read_excel('data/2. eTailing_Amazon.xlsx')
meesho_df = pd.read_excel('data/3.SocialCommerce_Meesho.xlsx')

flipkart_df['Source'] = 'Flipkart'
amazon_df['Source'] = 'Amazon'

# Concatenate the datasets
combined_df = pd.concat([flipkart_df, amazon_df], ignore_index=True)



# Ensure 'Month' column is datetime
combined_df['Month'] = pd.to_datetime(combined_df['Month'], format='%b\'%y')

# Input widgets
## Source selection
source_list = combined_df['Source'].unique()
source_selection = st.multiselect('Select data source', source_list, source_list)

## Category selection (example categories, adjust as needed)
category_list = ['Mobiles (USD Mn)', 'Electronic Devices (USD Mn)', 'Large & Small Appliances (USD Mn)', 'Fashion (USD Mn)', 'Home (USD Mn)']
category_selection = st.multiselect('Select categories', category_list, category_list)

## Date range selection
date_min = combined_df['Month'].min()
date_max = combined_df['Month'].max()
date_selection = st.slider('Select date range', date_min, date_max, (date_min, date_max))

# Filter data based on selections
filtered_df = combined_df[(combined_df['Source'].isin(source_selection)) & (combined_df['Month'].between(date_selection[0], date_selection[1]))]

# Reshape data for display and charting
reshaped_df = filtered_df.pivot_table(index='Month', columns='Source', values=category_selection, aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='Month', ascending=False)

# Display DataFrame
df_editor = st.data_editor(reshaped_df, height=400, use_container_width=True)

# Display chart
df_chart = reshaped_df.reset_index().melt(id_vars='Month', var_name='Category', value_name='Value')
chart = alt.Chart(df_chart).mark_line().encode(
    x=alt.X('Month:T', title='Month'),
    y=alt.Y('Value:Q', title='Value (USD Mn)'),
    color='Category:N'
).properties(height=400)

st.altair_chart(chart, use_container_width=True)
