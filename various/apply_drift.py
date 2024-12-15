# This script modifies the input file by applying a time drift and clock rate change (given in percent) to the time (and timestamps).
# If no clock drift time and clock rate change is given, create files with 2s and 4s drift with 0.5%, 1% and 2% clock rate change.
# Usage: python script.py <input_file> [<time_drift_seconds> <clock_rate_change>]

import pandas as pd
import sys
import os

def apply_time_drift_and_clock_rate_change(input_file, time_drift_seconds, clock_rate_change):
    # Load the data from the input file
    df = pd.read_csv(input_file)
    
    # Ensure the required columns are present
    if 'time' not in df.columns or 'timestamp' not in df.columns:
        print("Input file must contain 'time' and 'timestamp' columns.")
        return

    # Apply time drift and clock rate change
    first_time = df['time'].iloc[0]
    df['time'] = df['time'].apply(lambda x: x + time_drift_seconds + clock_rate_change * (x - first_time))

    # Update the 'timestamp' column based on new 'time' column
    df['timestamp'] = pd.to_datetime(df['time'], unit='s')

    # Generate output directory and create if it doesn't exist
    output_dir = os.path.join(os.path.dirname(input_file), 'drifted')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate output file name based on input parameters
    output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.csv', f'_timedrift{time_drift_seconds}s.csv'))#_clockrate{clock_rate_change*100}%.csv'))
    
    # Save the updated DataFrame to the output file
    df.to_csv(output_file, index=False)
    print(f"File updated and saved as {output_file}")

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        # If no time drift and clock rate change are provided, create multiple output files with predefined values
        predefined_time_drifts = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
        predefined_clock_rate_changes = [0] # 0.5%, 1%, 2%

        for time_drift in predefined_time_drifts:
            for clock_rate in predefined_clock_rate_changes:
                apply_time_drift_and_clock_rate_change(input_file, time_drift, clock_rate)
    elif len(sys.argv) == 4:
        input_file = sys.argv[1]
        time_drift_seconds = float(sys.argv[2])
        clock_rate_change = float(sys.argv[3])

        # Run the function to apply time drift and clock rate change
        apply_time_drift_and_clock_rate_change(input_file, time_drift_seconds, clock_rate_change)
    else:
        print("Usage: python script.py <input_file> [<time_drift_seconds> <clock_rate_change>]")
        sys.exit(1)

