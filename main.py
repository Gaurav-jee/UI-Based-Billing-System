import streamlit as st
import os
from datetime import datetime, date, timedelta
from config import BILLS_FOLDER, MASTER_FILE_PATH, LOGO_PATH
from file_operations import create_new_bill, get_existing_bills, open_in_excel, get_file_info, open_folder, get_bills_for_date, duplicate_bill
from utils import generate_unique_suffix
from app_utils import reset_state

def main():
    st.set_page_config(layout="wide", page_title="Billing System")

    # Top right section for date/time and reset button
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write("")  # Empty column for spacing
    with col2:
        st.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    with col3:
        if st.button("Reset"):
            reset_state()
            st.rerun()

    # Sidebar
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_column_width=True)
        else:
            st.error("Logo not found")

        st.title("Billing System")
        st.info(f"Master: {os.path.basename(MASTER_FILE_PATH)}")

        st.markdown("## Update Master File")
        uploaded_file = st.file_uploader("Upload new master file", type="xlsx")
        if uploaded_file is not None:
            new_master_path = os.path.join(BILLS_FOLDER, uploaded_file.name)
            with open(new_master_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"New master file selected: {uploaded_file.name}")

    # Main content
    st.title("Create New Bill")

    if 'step' not in st.session_state:
        st.session_state.step = 'input'

    if st.session_state.step == 'input':
        customer_name = st.text_input("Enter customer name", value=st.session_state.get('customer_name', ''))
        if st.button("Create and Open Bill"):
            if customer_name:
                existing_bills = get_existing_bills(customer_name)
                if existing_bills:
                    st.session_state.existing_bills = existing_bills
                    st.session_state.customer_name = customer_name
                    st.session_state.step = 'existing_bills_warning'
                    st.rerun()
                else:
                    new_file = create_new_bill(customer_name)
                    open_in_excel(new_file)
                    st.success(f"New bill created for {customer_name}")
            else:
                st.error("Please enter a customer name")

    elif st.session_state.step == 'existing_bills_warning':
        st.warning(f"Bills for {st.session_state.customer_name} already exist.")
        for bill in st.session_state.existing_bills:
            file_info = get_file_info(os.path.join(BILLS_FOLDER, bill))
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(bill)
            with col2:
                st.write(f"Created: {file_info['created']}")
            with col3:
                if st.button(f"Open", key=f"open_{bill}"):
                    open_in_excel(file_info['path'])

        if st.button("Create New Bill Anyway"):
            suffix = generate_unique_suffix(st.session_state.existing_bills)
            new_file = create_new_bill(st.session_state.customer_name, suffix)
            open_in_excel(new_file)
            st.success(f"New bill created for {st.session_state.customer_name} with suffix '{suffix}'")
            st.session_state.step = 'input'
            st.session_state.customer_name = ''
            st.rerun()

    st.markdown("---")

    # Buttons for today's bills, yesterday's bills, and open folder
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Today's Bills"):
            st.session_state.show_bills = 'today'
    with col2:
        if st.button("Show Yesterday's Bills"):
            st.session_state.show_bills = 'yesterday'
    with col3:
        if st.button("Open Created Bills Folder"):
            open_folder(BILLS_FOLDER)

    # Display bills based on button clicks
    if 'show_bills' in st.session_state:
        if st.session_state.show_bills == 'today':
            st.subheader(f"Bills Created Today ({date.today().strftime('%Y-%m-%d')})")
            bills = get_bills_for_date(BILLS_FOLDER, date.today())
        elif st.session_state.show_bills == 'yesterday':
            yesterday = date.today() - timedelta(days=1)
            st.subheader(f"Bills Created Yesterday ({yesterday.strftime('%Y-%m-%d')})")
            bills = get_bills_for_date(BILLS_FOLDER, yesterday)
        
        if bills:
            for bill, creation_time in bills:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(bill)
                with col2:
                    st.text(datetime.fromtimestamp(creation_time).strftime('%H:%M:%S'))
                with col3:
                    if st.button(f"Open", key=f"open_daily_{bill}"):
                        open_in_excel(os.path.join(BILLS_FOLDER, bill))
                with col4:
                    if st.button(f"Duplicate", key=f"duplicate_daily_{bill}"):
                        st.session_state.duplicate_file = os.path.join(BILLS_FOLDER, bill)
                        st.session_state.show_duplicate_input = bill
                
                # Show duplication input inline
                if 'show_duplicate_input' in st.session_state and st.session_state.show_duplicate_input == bill:
                    with st.container():
                        new_name = st.text_input("Enter new customer name", key=f"new_name_{bill}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Create Duplicate", key=f"create_duplicate_{bill}"):
                                if new_name:
                                    new_file = duplicate_bill(st.session_state.duplicate_file, new_name)
                                    open_in_excel(new_file)
                                    st.success(f"Duplicated bill created for: {new_name}")
                                    st.session_state.show_duplicate_input = None
                                    st.rerun()
                                else:
                                    st.error("Please enter a name for the duplicated bill")
                        with col2:
                            if st.button("Cancel", key=f"cancel_duplicate_{bill}"):
                                st.session_state.show_duplicate_input = None
                                st.rerun()
        else:
            st.info("No bills found for the selected date.")

if __name__ == "__main__":
    main()