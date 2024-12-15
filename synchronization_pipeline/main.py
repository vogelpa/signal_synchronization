# This is the main entry point for the synchronization pipeline. 
# It reads the configuration file, processes the input files, and runs the synchronization pipeline. 
# The pipeline consists of the following main steps:
# 1. aggregate the multichannel data into a single 1D signal (absolute sum of channels)
# 2. detect outliers in the signal
# 3. identify events based on the outliers detected
# 4. calculate event information, such as the extremas of the event, the start time, and the normalized event data

# main.py
import pandas as pd
import yaml
import argparse

from pipeline_steps.outlier_detection import detect_outliers
from pipeline_steps.event_detection import identify_events
from pipeline_steps.event_information import extract_event_information
from pipeline_steps.event_comparison import compare_events_dtw, compare_events_cca
from pipeline_steps.signal_alignment import align_signals
from utils.data_utils import load_data, save_dataframe_to_csv, save_yaml, create_1D_signal, calculate_1D_signal_derivative, resample, annotate_events
from utils.visualization import plot_interactive_html


def process_signal(input_file, sensor_name, outlier_neighbors, diverse_settings):
    #assert time column
    threshold = diverse_settings['min_time_event']
    min_outlier_percentage = diverse_settings['min_outlier_fraction_event']
    normalization_window_duration = diverse_settings['normalization_window_duration']
    signal_column = '1d_signal'

    df = load_data(input_file)
    df = create_1D_signal(df, sensor_name)

    if sensor_name == 'sensomative':
        df = calculate_1D_signal_derivative(df, '1d_signal')
        signal_column = '1d_signal_derivative'

    outlier_flags = detect_outliers(df, signal_column, n_neighbors=outlier_neighbors)
    
    events = identify_events(df, outlier_flags, time_column='time', threshold=threshold, min_outlier_percentage=min_outlier_percentage)

    event_stats = extract_event_information(df, events, signal_column, normalization_window_duration, time_column='time')
    df = annotate_events(df, events)
    return df, event_stats, signal_column


def run_synchronization_pipeline(reference_file, file_to_align, sensor_name_reference, sensor_name_align, outlier_neighbors_reference, outlier_neighbors_align, diverse_settings, plotting, plot_settings):
    df1, reference_event, reference_signal = process_signal(reference_file, sensor_name_reference, outlier_neighbors_reference, diverse_settings)
    df2, align_events, align_signal = process_signal(file_to_align, sensor_name_align, outlier_neighbors_align, diverse_settings)
    
    max_time_gap_events = diverse_settings["max_time_gap_events"]
    if sensor_name_reference == 'sensomative' or sensor_name_align == 'sensomative':
        comparison_results = compare_events_dtw(reference_event, align_events, max_time_gap_events) # could be replaced by better method
        dtw_distance_threshold = diverse_settings['dtw_distance_threshold_sensomative']
    else:
        comparison_results = compare_events_dtw(reference_event, align_events, max_time_gap_events)
        dtw_distance_threshold = diverse_settings['dtw_distance_threshold_accelerator']
    
    for result in comparison_results:
        print(f"Reference File Event ID: {result['event1_id']} best matches with File to Align Event ID: {result['best_match_event2_id']}, dtw_distance: {result['dtw_distance']}")

    # Align the signals
    original_df2, df2_aligned = align_signals(df1, df2, comparison_results, sensor_name_reference, sensor_name_align, dtw_distance_threshold)
    df2_aligned['timestamp'] = pd.to_datetime(df2_aligned['time'], unit='s')

    #align_signal = '1d_signal' # comment out if you want the derivative (for sensomative) in the plot and saved files
    # Resample the aligned signal to match the reference frequency and timestamps
    resampled_df2 = resample(df2_aligned, df1, signal_column=align_signal)
    resampled_df2['timestamp'] = pd.to_datetime(resampled_df2['time'], unit='s')
    
    if diverse_settings['save_output_files']:
        output_folder_path = diverse_settings['output_folder_path']
        # Save updated versions of the dataframes to output_folder_path
        save_dataframe_to_csv(df1, file_to_align, sensor_name_reference, "updated", output_folder_path)
        save_dataframe_to_csv(df2_aligned, file_to_align, sensor_name_reference, "aligned", output_folder_path)
        save_dataframe_to_csv(resampled_df2, file_to_align, sensor_name_reference, "resampled", output_folder_path)
    
    if plotting:
        # Plot combined figures interactively using visualization module
        plot_interactive_html(
            df1,
            original_df2, 
            resampled_df2, 
            reference_signal,
            align_signal,  
            reference_file, 
            file_to_align, 
            plot_settings
            )

def main():
    parser = argparse.ArgumentParser(description="Run event detection and signal alignment.")
    parser.add_argument("--config", required=True, help="Path to the configuration YAML file.")
    args = parser.parse_args()

    # Load configuration from the specified config file
    with open(args.config, 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Dynamic settings
    reference_file = config['reference_file']
    file_to_align = config['file_to_align']
    sensor_name_reference = config['sensor_name_reference']
    sensor_name_align = config['sensor_name_align']
 
    # Static settings
    outlier_settings = {
        'cosinuss': config['outlier_neighbors_cosinuss'],
        'corsano': config['outlier_neighbors_corsano'],
        'vivalink': config['outlier_neighbors_vivalink'],
        'sensomative': config['outlier_neighbors_sensomative']
    }

    outlier_neighbors_reference = outlier_settings[sensor_name_reference]
    outlier_neighbors_align = outlier_settings[sensor_name_align]

    diverse_settings = {
        'min_time_event': config['min_time_event'],
        'min_outlier_fraction_event': config['min_outlier_fraction_event'],
        'max_time_gap_events': config['max_time_gap_events'],
        'dtw_distance_threshold_accelerator': config['dtw_distance_threshold_accelerator'],
        'dtw_distance_threshold_sensomative': config['dtw_distance_threshold_sensomative'],
        'normalization_window_duration': config['normalization_window_duration'],
        'save_output_files': config['save_output_files'],
        'output_folder_path': config['output_folder_path']
    }

    # Plotting
    plotting = config['plotting']
    plot_settings = {
        'scaling_factor_reference': config['scaling_factor_reference'],
        'scaling_factor_align': config['scaling_factor_align']
    }

    print(f"Processing files: {reference_file} (Sensor: {sensor_name_reference}) and {file_to_align} (Sensor: {sensor_name_align})")

    run_synchronization_pipeline(
        reference_file, 
        file_to_align, 
        sensor_name_reference,
        sensor_name_align, 
        outlier_neighbors_reference, 
        outlier_neighbors_align,
        diverse_settings,
        plotting,
        plot_settings
        )

    if diverse_settings['save_output_files']:
        # copy config yaml to output folder
        save_yaml(args.config, file_to_align, sensor_name_reference, diverse_settings["output_folder_path"])

if __name__ == "__main__":
    main()
