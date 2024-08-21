# config.py
import os

# File paths using correct string format
MASTER_FILE_PATH = "C:\\ART_GALLERYHPWHITE\\2023\\NEW BILLS\\New (100).xlsx"
BILLS_FOLDER = "C:\\ART_GALLERYHPWHITE\\2023\\NEW BILLS"
LOGO_PATH = "C:\\ART_GALLERYHPWHITE\\Experiments\\company_logo.jpg"

# Ensure the BILLS_FOLDER exists
os.makedirs(BILLS_FOLDER, exist_ok=True)