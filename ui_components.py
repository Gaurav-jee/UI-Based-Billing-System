# ui_components.py

import os
import streamlit as st
from datetime import date, timedelta, datetime
from file_operations import get_bills_for_date, open_in_excel, open_folder, get_file_info
from config import BILLS_FOLDER

def display_sidebar(master_file_path, logo_path):
    with st.sidebar:
        if os.path.exists(logo_path):
            st.image(logo_path, use_column_width=True)
        else:
            st.error("Logo not found")

        st.info(f"Master: {os.path.basename(master_file_path)}")
        st.markdown("## Update Master File")
        uploaded_file = st.file_uploader("Upload new master file", type="xlsx")
        if uploaded_file is not None:
            new_master_path = os.path.join(BILLS_FOLDER, uploaded_file.name)
            with open(new_master_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"New master file selected: {uploaded_file.name}")
            return new_master_path
        return master_file_path

def display_bill_creation(clear_callback):
    st.subheader("Create New Bill")
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        customer_name = st.text_input("Enter customer name", value=st.session_state.get('customer_name', ''), key="customer_name")
    with col2:
        if st.button("Create and Open Bill", type="primary"):
            st.session_state.create_bill = True
    with col3:
        st.button("Clear Input", on_click=clear_callback)
    return customer_name

def display_existing_bills_warning(customer_name, existing_bills):
    st.markdown(f'<p class="red-warning">Bills for {customer_name} already exist.</p>', unsafe_allow_html=True)
    for bill in existing_bills:
        file_path = os.path.join(BILLS_FOLDER, bill)
        file_info = get_file_info(file_path)
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(bill)
        with col2:
            st.write(f"Created: {file_info['created']}")
        with col3:
            if st.button(f"Open", key=f"open_{bill}"):
                st.session_state.open_file = file_path

    if st.button("Create New Bill Anyway"):
        st.session_state.create_anyway = True

def display_daily_bills():
    st.subheader("View Recent Bills")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Today's Bills", type="secondary"):
            st.session_state.show_bills = 'today'
    with col2:
        if st.button("Show Yesterday's Bills", type="secondary"):
            st.session_state.show_bills = 'yesterday'
    with col3:
        if st.button("Open Created Bills Folder", type="secondary"):
            success, message = open_folder(BILLS_FOLDER)
            if not success:
                st.error(f"Failed to open folder: {message}")

    if 'show_bills' in st.session_state:
        if st.session_state.show_bills == 'today':
            display_date = date.today()
        elif st.session_state.show_bills == 'yesterday':
            display_date = date.today() - timedelta(days=1)
        
        st.write(f"Bills Created on {display_date.strftime('%Y-%m-%d')}")
        bills = get_bills_for_date(BILLS_FOLDER, display_date)
        
        if bills:
            for bill, creation_time in bills:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(bill)
                with col2:
                    st.text(datetime.fromtimestamp(creation_time).strftime('%I:%M:%S %p'))
                with col3:
                    if st.button(f"Open", key=f"open_daily_{bill}"):
                        st.session_state.open_file = os.path.join(BILLS_FOLDER, bill)
        else:
            st.info("No bills found for the selected date.")