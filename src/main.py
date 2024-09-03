import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)


pages = {
    "🏠 Home": [
        st.Page("pages/home.py", title="Welcome & Overview"),
    ],
    "Financial Analyzer 📊": [
        st.Page("pages/analyzer.py", title="Financial Analyzer"),
    ]
}


pg = st.navigation(pages)
pg.run()