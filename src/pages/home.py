import streamlit as st

st.write("# Welcome to Nova Financial Solutions Stock Analyzer App 👋")

st.markdown(
    """
    The Nova Financial Solutions Stock Analyzer App is an intuitive tool designed for financial enthusiasts and investors who want to analyze and compare the top-performing 'Magnificent 7' stocks. 
    This app allows you to select a date range and retrieve historical stock data for these leading companies using Yahoo Finance. 
    You can perform in-depth financial analysis, generate insightful plots, and obtain portfolio recommendations and weight distributions based on the selected data.
    
    To get started, simply navigate to the 'Financial Analyzer' page, select your date range, and explore the data!
    """
)

if st.button("Get started!"):
    st.switch_page(page='pages/analyzer.py')