# app_utils.py

import streamlit as st
from datetime import datetime

def clear_input():
    st.session_state.customer_name = ""

def reset_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def display_header():
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        st.title("Billing System")
    with col2:
        st.markdown(f"<h3 style='text-align: center;'>{datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}</h3>", unsafe_allow_html=True)
    with col3:
        if st.button("Reset"):
            reset_state()

# Custom CSS for colored warning
st.markdown("""
<style>
    .red-warning {
        color: red;
        font-weight: bold;
    }
    .stApp > header {
        background-color: #0E1117;
        padding: 1rem 0;
    }
    .main-content {
        padding-top: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)