# This script reads in the modified labels file from the Sensei-V2 project, calculates precise times for the synchronization 
# events at the start and end of the dataset. It then and saves the results to a new Excel file called 'Sensei-V2 - Exact-Synching-Times'.
# The exact times are computed based on the difference between specified frames and their corresponding exact start and end times (according 
# to the Guide.txt file from the dataset). The output includes the calculated start and end times for each of the three sit down events each user.

import os
import pandas as pd
from datetime import datetime, timedelta

# Define path to Sensei-V2 dataset
path_to_sensei_v2_dataset = 'C:/Users/pasca/Documents/SemesterThesisData/'
path_to_sensei_v2_dataset = 'C:/Users/hrkuc/Documents/Semester Project/SemesterThesisData/'

excel_file = os.path.join(path_to_sensei_v2_dataset, 'Sensei-V2 - Modified-Labels.xlsx')

# Read in the Excel file
df = pd.read_excel(excel_file)

# Function to convert time to timedelta
def time_to_timedelta(time):
    return timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

# Function to calculate exact time for each user
def calculate_exact_time(row, frame_column):
    frame_laptop_time_START = time_to_timedelta(row['frame_laptop_time_START'])
    frame_laptop_time_END = time_to_timedelta(row['frame_laptop_time_END'])
    first_frame_of_second_START = row['first_frame_of_second_START']
    first_frame_of_second_END = row['first_frame_of_second_END']
    video_frame_touchpad_value = row[frame_column]

    # Calculate the exact time referring to the given frame
    delta_time = (
        (video_frame_touchpad_value - first_frame_of_second_START) *
        (frame_laptop_time_END - frame_laptop_time_START) /
        (first_frame_of_second_END - first_frame_of_second_START)
    )
    exact_time = frame_laptop_time_START + delta_time
    return (datetime.min + exact_time).time()

# Calculate exact times for each relevant column
df['start_1'] = df.apply(lambda row: calculate_exact_time(row, 'VideoFrame_Touchpad_START_1'), axis=1)
df['start_2'] = df.apply(lambda row: calculate_exact_time(row, 'VideoFrame_Touchpad_START_2'), axis=1)
df['start_3'] = df.apply(lambda row: calculate_exact_time(row, 'VideoFrame_Touchpad_START_3'), axis=1)
df['end_1'] = df.apply(lambda row: calculate_exact_time(row, 'VideoFrame_Touchpad_END_1'), axis=1)
df['end_2'] = df.apply(lambda row: calculate_exact_time(row, 'VideoFrame_Touchpad_END_2'), axis=1)
df['end_3'] = df.apply(lambda row: calculate_exact_time(row, 'VideoFrame_Touchpad_END_3'), axis=1)

# Save the updated DataFrame with only the User and the calculated times to a new Excel file
output_file = os.path.join(path_to_sensei_v2_dataset, 'Sensei-V2 - Exact-Synching-Times.xlsx')
df[['User', 'start_1', 'start_2', 'start_3', 'end_1', 'end_2', 'end_3']].to_excel(output_file, index=False)