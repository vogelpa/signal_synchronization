# This script was used to move files in the 'drifted' folder to 'start' and 'end' folders based on their prefix.
# Just for convenience and better order. 
import os
import shutil

def organize_drifted_folders(base_directory):
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(base_directory):
        if 'drifted' in dirs:
            drifted_path = os.path.join(root, 'drifted')
            start_path = os.path.join(drifted_path, 'start')
            end_path = os.path.join(drifted_path, 'end')

            # Create 'start' and 'end' folders
            os.makedirs(start_path, exist_ok=True)
            os.makedirs(end_path, exist_ok=True)

            # Iterate over files in the 'drifted' folder
            for file_name in os.listdir(drifted_path):
                file_path = os.path.join(drifted_path, file_name)
                # Skip directories
                if not os.path.isfile(file_path):
                    continue

                # Move files based on their prefix
                if file_name.startswith('start'):
                    shutil.move(file_path, os.path.join(start_path, file_name))
                elif file_name.startswith('end'):
                    shutil.move(file_path, os.path.join(end_path, file_name))

# Specify the base directory
base_directory = "C:/Users/pasca/Meine Ablage (vogelpa@ethz.ch)/Semester Thesis/data_synchronized"

# Call the function
organize_drifted_folders(base_directory)
