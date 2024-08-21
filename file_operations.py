# file_operations.py

import os
import shutil
import subprocess
from datetime import datetime, date
from config import MASTER_FILE_PATH, BILLS_FOLDER

def create_new_bill(customer_name, suffix=''):
    file_name = f"{customer_name}_bill{suffix}.xlsx"
    new_file_path = os.path.join(BILLS_FOLDER, file_name)
    if os.path.exists(new_file_path):
        raise FileExistsError(f"A bill for {customer_name} already exists.")
    shutil.copy(MASTER_FILE_PATH, new_file_path)
    return new_file_path

def get_existing_bills(customer_name):
    existing_bills = []
    for file in os.listdir(BILLS_FOLDER):
        if file.startswith(f"{customer_name}_bill") and file.endswith(".xlsx"):
            existing_bills.append(file)
    return sorted(existing_bills)

def get_bills_for_date(folder_path, target_date):
    target_date = target_date.strftime('%Y-%m-%d')
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') and f != os.path.basename(MASTER_FILE_PATH)]
    date_files = []
    for f in files:
        file_path = os.path.join(folder_path, f)
        file_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d')
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

def open_in_excel(file_path):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # For macOS and Linux
            subprocess.call(('open', file_path))
        return True, ""
    except Exception as e:
        return False, str(e)

def open_folder(folder_path):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(folder_path)
        elif os.name == 'posix':  # For macOS and Linux
            subprocess.call(('open', folder_path))
        return True, ""
    except Exception as e:
        return False, str(e)

def duplicate_bill(original_file, new_name):
    new_file_path = os.path.join(BILLS_FOLDER, f"{new_name}_bill.xlsx")
    shutil.copy(original_file, new_file_path)
    return new_file_path