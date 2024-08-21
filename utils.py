# utils.py

import os
from config import BILLS_FOLDER

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

def get_existing_customer_names():
    customer_names = set()
    for file in os.listdir(BILLS_FOLDER):
        if file.endswith("_bill.xlsx"):
            name = file.rsplit("_bill", 1)[0]
            customer_names.add(name)
    return sorted(list(customer_names))