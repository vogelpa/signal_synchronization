# utils/data_loader.py
import os
import shutil
import pandas as pd
import numpy as np

# add function to create the 1d_signal column 

def load_data(input_file, time_column='time'):
    df = pd.read_csv(input_file)
    df = df.sort_values(by=time_column).reset_index(drop=True) # theoretically not needed, just making sure
    return df


def save_dataframe_to_csv(data, file_to_align, sensor_name_reference, prefix, output_folder_path):
    # Determine the directory structure
    aligned_dir = os.path.join(output_folder_path, f"aligned_to_{sensor_name_reference}")
    file_folder = os.path.splitext(os.path.basename(file_to_align))[0]  # Folder named after the file (without extension)
    target_dir = os.path.join(aligned_dir, file_folder)

    # Create the necessary directories
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Define the full path for the output file
    output_file = os.path.join(target_dir, f"{prefix}_{os.path.basename(file_to_align)}")

    # Save the DataFrame to the specified file
    data.to_csv(output_file, index=False)
    print(f"Data saved to: {output_file}")
    

def save_yaml(config_file_path, file_to_align, sensor_name_reference, output_folder_path):
    """
    Copies the original config file to the output folder.

    Parameters:
        config_file_path (str): Path to the original configuration YAML file.
        output_folder (str): Directory where the config file should be copied.
    """
    # Determine the directory structure
    aligned_dir = os.path.join(output_folder_path, f"aligned_to_{sensor_name_reference}")
    file_folder = os.path.splitext(os.path.basename(file_to_align))[0]  # Folder named after the file (without extension)
    target_dir = os.path.join(aligned_dir, file_folder)

    # Create the necessary directories
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Define the full path for the output file
    config_file = os.path.join(target_dir, "config.yaml")

    shutil.copy(config_file_path, config_file)
    print(f"Config file copied to: {config_file}")

def create_1D_signal(df, sensor_name):
    # Determine how to create the 1d_signal column based on the sensor type
    if 'corsano' == sensor_name:
        df['1d_signal'] = df[['accX', 'accY', 'accZ']].abs().sum(axis=1)
    elif 'cosinuss' == sensor_name:
        df['1d_signal'] = df[['acc_x', 'acc_y', 'acc_z']].abs().sum(axis=1)
    elif 'vivalink' == sensor_name:
        df['1d_signal'] = df[['x', 'y', 'z']].abs().sum(axis=1)
    elif 'sensomative' == sensor_name:
        df['1d_signal'] = df[['device1_value0', 'device1_value1', 'device1_value2', 'device1_value3', 'device1_value4',
                              'device1_value5', 'device1_value6', 'device1_value7', 'device1_value8', 'device1_value9',
                              'device1_value10', 'device1_value11', 'device1_value12']].abs().sum(axis=1)
    else:
        raise ValueError("Unknown file type in the input path")

    return df

def calculate_1D_signal_derivative(df, signal_column):
    df['1d_signal_derivative'] = df[signal_column].diff().fillna(0)
    return df

def resample(df_aligned, reference_df, time_column='time', signal_column='1d_signal'):
    reference_times = reference_df[time_column]
    resampled_signal = np.interp(reference_times, df_aligned[time_column], df_aligned[signal_column])
    resampled_df = pd.DataFrame({time_column: reference_times, signal_column: resampled_signal})
    return resampled_df

def annotate_events(data, events, event_column='event_id'):
    data[event_column] = pd.NA
    for event in events:
        data.loc[event['indices'], event_column] = event['event_id']
    return data