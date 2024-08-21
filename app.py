import streamlit as st
import os
import shutil
import subprocess
from datetime import datetime, date, timedelta

# Use the provided file paths
MASTER_FILE_PATH = "C:/ART_GALLERYHPWHITE/2023/NEW BILLS/New (100).xlsx"
BILLS_FOLDER = "C:/ART_GALLERYHPWHITE/2023/NEW BILLS"
LOGO_PATH = "C:/ART_GALLERYHPWHITE/Experiments/company_logo.jpg"

def create_new_bill(customer_name, suffix=''):
    file_name = f"{customer_name}_bill{suffix}.xlsx"
    new_file_path = os.path.join(BILLS_FOLDER, file_name)
    shutil.copy(MASTER_FILE_PATH, new_file_path)
    return new_file_path

def duplicate_bill(original_file, new_name):
    new_file_path = os.path.join(BILLS_FOLDER, f"{new_name}_bill.xlsx")
    shutil.copy(original_file, new_file_path)
    return new_file_path

def get_existing_bills(customer_name):
    existing_bills = []
    for file in os.listdir(BILLS_FOLDER):
        if file.startswith(f"{customer_name}_bill") and file.endswith(".xlsx"):
            existing_bills.append(file)
    return sorted(existing_bills)

def generate_unique_suffix(existing_bills):
    if not existing_bills:
        return ""
    max_suffix = 0
    for bill in existing_bills:
        parts = bill.split('_')
        if len(parts) > 2 and parts[-1].endswith('.xlsx'):
            try:
                suffix = int(parts[-1][:-5])  # Remove '.xlsx' and convert to int
                max_suffix = max(max_suffix, suffix)
            except ValueError:
                continue
    return f"_{max_suffix + 1}"

def open_in_excel(file_path):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # For macOS and Linux
            subprocess.call(('open', file_path))
        return True
    except Exception as e:
        st.error(f"Error opening file: {str(e)}")
        return False

def open_folder(folder_path):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(folder_path)
        elif os.name == 'posix':  # For macOS and Linux
            subprocess.call(('open', folder_path))
        return True
    except Exception as e:
        st.error(f"Error opening folder: {str(e)}")
        return False

def get_bills_for_date(folder_path, target_date):
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') and f != os.path.basename(MASTER_FILE_PATH)]
    date_files = []
    for f in files:
        file_path = os.path.join(folder_path, f)
        file_date = date.fromtimestamp(os.path.getctime(file_path))
        if file_date == target_date:
            date_files.append((f, os.path.getctime(file_path)))
    return sorted(date_files, key=lambda x: x[1], reverse=True)

def get_file_info(file_path):
    creation_time = os.path.getctime(file_path)
    modification_time = os.path.getmtime(file_path)
    return {
        "path": file_path,
        "created": datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S'),
        "modified": datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S'),
    }

def reset_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def main():
    global MASTER_FILE_PATH
    st.set_page_config(layout="wide")

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

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 'input'
    if 'customer_name' not in st.session_state:
        st.session_state.customer_name = ''

    # Sidebar
    sidebar = st.sidebar

    # Display logo
    if os.path.exists(LOGO_PATH):
        sidebar.image(LOGO_PATH, use_column_width=True)
    else:
        sidebar.error("Ek Nazar Khilona Art")

    sidebar.title("Billing System")

    # Display current Master File information
    sidebar.info(f"Master: {os.path.basename(MASTER_FILE_PATH)}")

    # Update Master File
    sidebar.markdown("## Update Master File")
    uploaded_file = sidebar.file_uploader("\n", type="xlsx")
    if uploaded_file is not None:
        # Save the uploaded file
        with open(os.path.join(BILLS_FOLDER, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        MASTER_FILE_PATH = os.path.join(BILLS_FOLDER, uploaded_file.name)
        sidebar.success(f"New master file selected: {uploaded_file.name}")

    # Placeholder for Analytics button
    if sidebar.button("Analytics"):
        sidebar.info("Analytics feature coming soon!")

    # Main content area
    st.title("Create New Bill")

    if st.session_state.step == 'input':
        st.session_state.customer_name = st.text_input("Enter customer name", value=st.session_state.customer_name)
        if st.button("Create and Open Bill"):
            if st.session_state.customer_name:
                existing_bills = get_existing_bills(st.session_state.customer_name)
                if existing_bills:
                    st.session_state.existing_bills = existing_bills
                    st.session_state.step = 'existing_bills_warning'
                    st.rerun()
                else:
                    new_file = create_new_bill(st.session_state.customer_name)
                    open_in_excel(new_file)
                    st.success(f"New bill created for {st.session_state.customer_name}")
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