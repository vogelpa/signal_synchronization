# This script processes sensor data from multiple users by extracting data within specific timestamp ranges.
# It reads user-specific timestamps from an Excel file and extracts corresponding data from CSV files located in
# subfolders. The extracted data is saved in a new output folder, while preserving the original subfolder structure.
# The script performs the following steps:
# 1. Reads the Excel files containing timestamp information and the starting dates for each user.
# 2. Iterates over all user folders, processes CSV files, and extracts data within specified timestamp ranges (with +30 seconds at start end +35 seconds at the end).
# 3. Skips files without a 'time' column or files where no data is found in the specified ranges.
# 4. Saves the extracted data (if at least 50 datapoints are available) while maintaining the original subfolder structure.

import os
import pandas as pd
from datetime import datetime, timedelta
import re

# Define path to Sensei-V2 dataset
#path_to_sensei_v2_dataset = 'C:/Users/pasca/Documents/SemesterThesisData/'
path_to_sensei_v2_dataset = 'C:/Users/hrkuc/Documents/Semester Project/SemesterThesisData/'

# Step 1: Read the Excel file to get the timestamps and the starting date
excel_file = os.path.join(path_to_sensei_v2_dataset, 'Sensei-V2 - Modified-Labels.xlsx')
date_file = os.path.join(path_to_sensei_v2_dataset, 'SCAI-SENSEI-V2/Pilot-Tests - Device Logs.xlsx')
df_labels = pd.read_excel(excel_file)
df_dates = pd.read_excel(date_file, header=1)  # Use the second row as header

# Step 2: Iterate over all user folders and process CSV files in subfolders
input_folder = os.path.join(path_to_sensei_v2_dataset, 'SCAI-SENSEI-V2')
output_folder = os.path.join(path_to_sensei_v2_dataset, 'SCAI-SENSEI-V2/start_end_data/')
os.makedirs(output_folder, exist_ok=True)

for index, row in df_labels.iterrows():
    user_id = row['User']
    start_time_1 = row['Timestamp_Touchpad_START_1']
    end_time_1 = row['Timestamp_Touchpad_START_3']
    start_time_3 = row['Timestamp_Touchpad_END_1']
    end_time_3 = row['Timestamp_Touchpad_END_3']

    # Get the starting date for the user from the date file
    user_date_row = df_dates[df_dates['Participant ID'] == user_id]
    if user_date_row.empty:
        print(f"Starting date for user {user_id} not found, skipping...")
        continue
    starting_date_str = user_date_row.iloc[0]['Starting Date and Time']

    # Extract only the date part from the starting date string
    starting_date_str = re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', starting_date_str).group()
    starting_date = datetime.strptime(starting_date_str, '%d.%m.%Y').date()

    # Combine date and time to get full datetime
    start_datetime_1 = datetime.combine(starting_date, start_time_1) - timedelta(seconds=30)
    end_datetime_1 = datetime.combine(starting_date, end_time_1) + timedelta(seconds=35)
    start_datetime_3 = datetime.combine(starting_date, start_time_3) - timedelta(seconds=30)
    end_datetime_3 = datetime.combine(starting_date, end_time_3) + timedelta(seconds=35)

    # Convert to Unix timestamp
    start_unix_1 = int(start_datetime_1.timestamp())
    end_unix_1 = int(end_datetime_1.timestamp())
    start_unix_3 = int(start_datetime_3.timestamp())
    end_unix_3 = int(end_datetime_3.timestamp())

    user_folder = os.path.join(input_folder, user_id)  # Assuming the folder is named by the user ID
    print(user_folder)
    if not os.path.exists(user_folder):
        print(f"User folder {user_folder} not found, skipping...")
        continue

    for root, dirs, files in os.walk(user_folder):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                
                try:
                    df_csv = pd.read_csv(csv_file_path)
                except:
                    print(f"Could not read file {csv_file_path}, skipping...")
                    continue
                    
                # Check if 'time' column exists
                if 'time' not in df_csv.columns:
                    print(f"No 'time' column in file {csv_file_path}, skipping...")
                    continue

                # Step 3: Extract the data within the specified timestamp ranges
                extracted_data_1 = df_csv[(df_csv['time'] >= start_unix_1) & (df_csv['time'] <= end_unix_1)]
                extracted_data_2 = df_csv[(df_csv['time'] >= start_unix_3) & (df_csv['time'] <= end_unix_3)]

                # Skip if no data is found in the time interval or if less than 50 datapoints are available
                if len(extracted_data_1) < 50 and len(extracted_data_2) < 50:
                    print(f"Not enough data points found in the specified time intervals for file {csv_file_path}, skipping...")
                    continue

                # Step 4: Preserve the subfolder structure and save the extracted data to new files
                relative_path = os.path.relpath(root, input_folder)
                user_output_folder = os.path.join(output_folder, relative_path)
                os.makedirs(user_output_folder, exist_ok=True)

                if len(extracted_data_1) >= 50:
                    output_file_path_1 = os.path.join(user_output_folder, f'start_{file}')
                    extracted_data_1.to_csv(output_file_path_1, index=False)
                    print(f"Extracted data for start range saved to {output_file_path_1}")

                if len(extracted_data_2) >= 50:
                    output_file_path_2 = os.path.join(user_output_folder, f'end_{file}')
                    extracted_data_2.to_csv(output_file_path_2, index=False)
                    print(f"Extracted data for end range saved to {output_file_path_2}")