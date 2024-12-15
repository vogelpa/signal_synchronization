# This script aligns the sensor data to the reference sensor data based on two synchronization points.
# The synchronization points are read from the synching CSV file (for format see 'synching_times.csv').
# Usage: python align.py <input_file> <reference_file> <synching_times_file> 


import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def main(input_file_path, reference_file_path, sync_times_file_path):
    # Load synchronization times from CSV file
    sync_times = pd.read_csv(sync_times_file_path)
    if sync_times.empty:
        print(f"Synchronization times file {sync_times_file_path} is empty.")
        return

    # Get the input file name from the path
    input_filename = os.path.basename(input_file_path)

    # Find the row corresponding to the input file, user, and sensor in the filepath
    sync_row = sync_times[(sync_times['filename'] == input_filename) &
                          (sync_times['user'].apply(lambda x: x in input_file_path)) &
                          (sync_times['sensor'].apply(lambda x: x in input_file_path))]
    if sync_row.empty:
        print(f"No synchronization data found for {input_filename}")
        return

    # Extract synchronization parameters from the row
    try:
        align_p1 = sync_row['Start synching point'].values[0]
        align_p2 = sync_row['End synching point'].values[0]
        if pd.isna(align_p1) or pd.isna(align_p2):
          raise
    except:
        print(f"Synchronization points for align file {input_filename} are not available.")
        return

    # Load synchronization times for reference file
    reference_filename = os.path.basename(reference_file_path)
    reference_row = sync_times[(sync_times['filename'] == reference_filename) &
                               (sync_times['user'].apply(lambda x: x in reference_file_path)) &
                               (sync_times['sensor'].apply(lambda x: x in reference_file_path))]
    if reference_row.empty:
        print(f"No synchronization data found for reference file {reference_filename}")
        return

    # Extract reference synchronization parameters from the row
    try:
        reference_p1 = reference_row['Start synching point'].values[0]
        reference_p2 = reference_row['End synching point'].values[0]
        if pd.isna(reference_p1) or pd.isna(reference_p2):
            raise
    except:
        print(f"Synchronization points for reference file {reference_filename} are not available.")
        return

    # Load the sensor data
    data = pd.read_csv(input_file_path)
    if data.empty:
        print(f"Input file {input_file_path} is empty.")
        return

    # Add alignment_point column to mark synchronization points
    data['alignment_point'] = pd.NA

    # Mark the alignment points in the alignment_point column before timeshift
    data.loc[data['time'] == align_p1, 'alignment_point'] = 1
    data.loc[data['time'] == align_p2, 'alignment_point'] = 1

    # Plot original signal
    plt.figure(figsize=(10, 6))
    plt.plot(data['time'], data['1d_signal'], label='Drifted Signal', color='blue')

    # Step 1: Shift all timepoints by 'reference_p1 - align_p1'
    shift_amount = reference_p1 - align_p1
    print(shift_amount)
    data['time'] = data['time'] + shift_amount

    # Step 2: Stretch points by the ratio of 'reference_p2 - reference_p1' / 'align_p2 - align_p1'
    scaling_factor = (reference_p2 - reference_p1) / (align_p2 - align_p1)
    data['time'] = reference_p1 + (data['time'] - reference_p1) * scaling_factor
    data['timestamp'] = pd.to_datetime(data['time'], unit='s')

    # Save the adjusted data to a new CSV file
    reference_sensor = reference_row['sensor'].values[0]
    output_file = input_file_path.replace(".csv", f"_synched_to_{reference_sensor.split('_', 1)[0]}.csv")
    data.to_csv(output_file, index=False)

    print(f"Alignment complete. Data saved to '{output_file}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synchronize sensor data based on synching points from a CSV file.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file containing sensor data.')
    parser.add_argument('reference_file', type=str, help='Path to the reference CSV file for synchronization.')
    parser.add_argument('sync_times_file', type=str, help='Path to the CSV file containing synchronization times.')
    args = parser.parse_args()

    main(args.input_file, args.reference_file, args.sync_times_file)
