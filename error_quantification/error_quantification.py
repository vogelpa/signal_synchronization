# This script was used to quantify the error in the synchronizated data and ground truth data.
# It goes through the current folder structure, looks for an 'aligned_' file, finds the corresponding ground truth file and then
# calculates the (absolute) time difference between the aligned data and the ground truth data.
# It plots the found points, calculates the average, standard deviation and RMSE of the time differences 
# and saves the results in the error_quantification.csv

# Note: vivalink folder must have same structure as the other folders, so not vivalink/yyyymmdd/drifted/... but vivalink/yyyymmdd/drifted/...

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def find_gt_file(sensor_folder, start_or_end):
    for root, _, files in os.walk(sensor_folder):
        for file in files:
            if start_or_end in file and 'synched_to' in file:
                return os.path.join(root, file)
    return None

def find_aligned_file(aligned_subfolder):
    for file in os.listdir(aligned_subfolder):
        if file.startswith("aligned_"):
            return os.path.join(aligned_subfolder, file)
    return None

def process_aligned_and_gt_files(aligned_file, gt_file, time_differences, sensor_type, drift_level):
    df_gt = pd.read_csv(gt_file)
    df_aligned = pd.read_csv(aligned_file)

    synch_points = df_gt[df_gt['alignment_point'] == 1]

    for _, row in synch_points.iterrows():
        index = row.name
        gt_time = row['time']

        if index < len(df_aligned):
            aligned_time = df_aligned.loc[index, 'time']
            time_difference = abs(gt_time - aligned_time)

            if sensor_type not in time_differences:
                time_differences[sensor_type] = {}
            if drift_level not in time_differences[sensor_type]:
                time_differences[sensor_type][drift_level] = []

            # if 'vivalnk' in aligned_file:
            #     print(f"Time difference for {aligned_file} \n {gt_file}s: {time_difference}")

            time_differences[sensor_type][drift_level].append(time_difference)

def calculate_statistics(time_differences):
    results = {}
    for sensor_type, drift_data in time_differences.items():
        results[sensor_type] = {}
        for drift_level, differences in drift_data.items():
            if differences:
                average_difference = np.mean(np.abs(differences))
                std_dev_difference = np.std(differences)
                rmse_difference = np.sqrt(np.mean(np.array(differences) ** 2))

                results[sensor_type][drift_level] = {
                    'MAE': round(average_difference, 3),
                    'Standard Deviation': round(std_dev_difference, 3),
                    'RMSE': round(rmse_difference, 3),
                    'Differences': differences  # Store differences for plotting
                }
    return results

def print_statistics(results):
    for sensor_type, drift_data in results.items():
        print(f"\n=== Statistics for {sensor_type} ===")
        for drift_level, stats in sorted(drift_data.items()):
            print(f"Drift (in s): {drift_level}")
            print(f"  MAE: {stats['MAE']:.4f}")
            print(f"  Standard Deviation: {stats['Standard Deviation']:.4f}")
            print(f"  RMSE: {stats['RMSE']:.4f}")

def write_results_to_csv(results, output_file):
    rows = []
    for sensor_type, drift_data in results.items():
        for drift_level, stats in drift_data.items():
            rows.append({
                'Sensor Type': sensor_type,
                'Drift (in s)': drift_level,
                'MAE': stats['MAE'],
                'Standard Deviation': stats['Standard Deviation'],
                'RMSE': stats['RMSE']
            })
    df_results = pd.DataFrame(rows)
    df_results.to_csv(output_file, index=False)

def plot_results(results):
    num_plots = sum(len(drift_data) for drift_data in results.values())
    cols = 4  # Number of columns in the subplot grid
    rows = (num_plots + cols - 1) // cols  # Calculate rows needed based on total plots

    fig, axes = plt.subplots(rows, cols, figsize=(20, 2 * rows))  # Adjusted the height to make more vertical space for titles
    fig.suptitle('Absolute Synchronization Error between Sensor with Timedrift and Ground Truth', fontsize=16)  # Added overall super title
    axes = axes.flatten()
    plot_index = 0

    all_differences = [diff for drift_data in results.values() for stats in drift_data.values() for diff in stats['Differences']]
    min_diff, max_diff = min(all_differences), max(all_differences)

    for sensor_type, drift_data in results.items():
        for drift_level, stats in sorted(drift_data.items()):
            differences = stats['Differences']
            ax = axes[plot_index]
            unique_values, counts = np.unique(differences, return_counts=True)
            ax.scatter(unique_values, [0] * len(unique_values), s=counts * 20)
            ax.set_xlim(min_diff, max_diff)  # Keep x-axis constant for all plots
            ax.set_yticks([])  # Remove y-axis since it is not needed
            ax.set_xlabel('Absolute Time Difference (s)')
            ax.set_title(f'{sensor_type} {drift_level}s', fontsize=12)
            ax.grid(True)
            plot_index += 1

    # Hide any unused subplots
    for i in range(plot_index, len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('error_quantification_plots.png')
    plt.show()

def main(base_folder):
    time_differences = {}
    for user_folder in os.listdir(base_folder):
        user_path = os.path.join(base_folder, user_folder)
        
        if os.path.isdir(user_path):
            for sensor_folder in os.listdir(user_path):
                sensor_path = os.path.join(user_path, sensor_folder)

                if os.path.isdir(sensor_path):
                    sensor_type = "Pressure Mat" if "sensomative" in sensor_folder.lower() else "Accelerometer"

                    drifted_folder_path = os.path.join(sensor_path, 'drifted')
                    if os.path.isdir(drifted_folder_path):
                        for start_end_folder in os.listdir(drifted_folder_path):
                            start_end_path = os.path.join(drifted_folder_path, start_end_folder)
                            
                            if os.path.isdir(start_end_path):
                                start_or_end = "start" if "start" in start_end_folder.lower() else "end"

                                for aligned_to_folder in [f for f in os.listdir(start_end_path) if os.path.isdir(os.path.join(start_end_path, f))]:
                                    aligned_to_path = os.path.join(start_end_path, aligned_to_folder)
                                    for drift_folder in os.listdir(aligned_to_path):
                                        drift_folder_path = os.path.join(aligned_to_path, drift_folder)
                                        
                                        if os.path.isdir(drift_folder_path):
                                            drift_level = drift_folder.split("_")[-1].replace("timedrift", "").replace("s", "")

                                            aligned_file = find_aligned_file(drift_folder_path)
                                            if aligned_file:
                                                sensor_parent_folder = os.path.abspath(os.path.join(aligned_to_path, "../../../"))
                                                gt_file = find_gt_file(sensor_parent_folder, start_or_end)
                                                if gt_file:
                                                    process_aligned_and_gt_files(aligned_file, gt_file, time_differences, sensor_type, drift_level)
                                                else:
                                                    print(f"No GT file found for {sensor_parent_folder} matching '{start_or_end}'")
                                            else:
                                                print(f"No aligned file found in {drift_folder_path}")
    print(time_differences)
    results = calculate_statistics(time_differences)
    print_statistics(results)
    write_results_to_csv(results, 'error_quantification.csv')
    plot_results(results)

if __name__ == "__main__":
    base_folder = "../data"
    main(base_folder)
