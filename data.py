import streamlit as st
import pandas as pd
@st.cache_data 
def display_data():
    st.header("Data Table")
    data = pd.read_excel('/Users/thanhngoc/Desktop/Testfile/Rounded_Farm_Data_with_Weather_Data 2.xlsx') 
    st.dataframe(data)