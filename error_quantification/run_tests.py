# this is a script to run the synchronization pipeline on the test data
# test data is defined in the test_run_configurations.json file to be present in the same directory
# it will run the pipeline for each user and reference file with all files in the specified align folder

import os
import json
import yaml
import subprocess

def generate_config(reference_file, sensor_name_reference, file_to_align, sensor_name_align, output_dir="configs"):
    """
    Generate a config.yaml file for a given reference and file to align.
    """
    os.makedirs(output_dir, exist_ok=True)
    config = {
        "reference_file": reference_file,
        "file_to_align": file_to_align,
        "sensor_name_reference": sensor_name_reference,
        "sensor_name_align": sensor_name_align,
        "outlier_neighbors_cosinuss": 400, # 400
        "outlier_neighbors_corsano": 200, # 200
        "outlier_neighbors_vivalink": 50, # 50
        "outlier_neighbors_sensomative": 20, # 20
        "min_time_event": 0.5,
        "min_outlier_fraction_event": 0.5,
        "max_time_gap_events": 2.0, # 3s
        "dtw_distance_threshold_accelerator": 150, # 150
        "dtw_distance_threshold_sensomative": 150, # 150
        "normalization_window_duration": 10,
        "save_output_files": True,
        "output_folder_path": os.path.dirname(file_to_align),
        "plotting": False,
        "scaling_factor_reference": 1.0,
        "scaling_factor_align": 1.0,
    }

    config_file_name = f"{os.path.basename(reference_file)}_{os.path.basename(file_to_align)}.yaml"
    config_file_path = os.path.join(output_dir, config_file_name)
    with open(config_file_path, "w") as config_file:
        yaml.dump(config, config_file)

    return config_file_path

def run_program(config_file):
    """
    Run the main.py script with the given config file.
    """
    print(f"Running program with config: {config_file}")
    subprocess.run(["python", "../synchronization_pipeline/main.py", "--config", config_file], check=True)


def get_files_in_folder(folder_path):
    """
    Get all .csv files in a folder.
    """
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist!")
        return []

    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith(".csv")
    ]


def process_user_data(user_data, user_name):
    """
    Process the data for a single user.
    """
    print(f"Processing data for user: {user_name}")

    for reference_data in user_data:
        reference_file = reference_data["reference_file"]
        sensor_name_reference = reference_data["sensor_name_reference"]

        for alignment in reference_data["alignments"]:
            sensor_name_align = alignment["sensor_name_align"]
            files_folder = alignment["files_folder"]

            # Get all files in the specified folder
            files_to_align = get_files_in_folder(files_folder)

            for file_to_align in files_to_align:
                print(f"Aligning {file_to_align} with {reference_file}")
                config_file = generate_config(reference_file, sensor_name_reference, file_to_align, sensor_name_align)
                run_program(config_file)


def main():
    # Load JSON input file
    input_json_path = "test_run_configurations.json"
    with open(input_json_path, "r") as json_file:
        data = json.load(json_file)
    for user, user_data in data.items():
        process_user_data(user_data, user)


if __name__ == "__main__":
    main()
