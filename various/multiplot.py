# This script creates an interactive plot of the column 1d_signals from one or multiple CSV files 
# with optional scaling factors applied.
# Assumes that the CSV files have a 'timestamp' column and a '1d_signal' column. If not, you should run "edit.py" on the files first.
# Usage: python multiplot.py <file1> <file2> ... <fileN> --scaling_factors <factor1> <factor2> ... <factorN>

import pandas as pd
import plotly.graph_objects as go
import argparse
import os

def plot_signals(file_paths, scaling_factors):
    """
    Plots signals from given CSV files with scaling factors applied.

    Parameters:
    file_paths (list of str): Paths to the CSV files to be plotted.
    scaling_factors (list of float): Scaling factors to apply to each corresponding CSV file.
    """
    # Create a Plotly figure for interactive plot
    fig = go.Figure()

    # Loop through each file and add traces to the Plotly figure
    for file, factor in zip(file_paths, scaling_factors):
        # Load the CSV into a pandas DataFrame
        data = pd.read_csv(file)
                
        # Prepare y-values by applying the scaling factor
        y_values = data['1d_signal'] * factor

        # Add a trace to the Plotly figure
        fig.add_trace(go.Scatter(x=data['timestamp'], y=y_values, mode='lines', name=f"{os.path.basename(file)} (factor: {factor})", hovertext=file))

    # Set the layout for the Plotly figure
    fig.update_layout(
        title='Signal Plot from CSV Files',
        xaxis_title='Timestamp',
        yaxis_title='1D Signal',
        legend_title='Devices',
        xaxis=dict(tickformat='%Y-%m-%d %H:%M:%S'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            traceorder="normal",
            font=dict(size=10),
            itemwidth=100
        )
    )

    # Save the interactive HTML plot
    fig.write_html('interactive_plot.html')

    # Show the interactive plot
    fig.show()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Plot signals from CSV files with scaling factors.')
    parser.add_argument('file_paths', nargs='+', help='Paths to the CSV files to be plotted.')
    parser.add_argument('--scaling_factors', nargs='*', type=float, default=None, help='Scaling factors to apply to each corresponding CSV file.')

    # Parse the arguments
    args = parser.parse_args()

    # If scaling factors are not provided, use 1 for each file
    if args.scaling_factors is None:
        args.scaling_factors = [1.0] * len(args.file_paths)

    # Ensure the number of file paths matches the number of scaling factors
    if len(args.file_paths) != len(args.scaling_factors):
        raise ValueError("The number of file paths must match the number of scaling factors.")

    # Call the function to plot signals
    plot_signals(args.file_paths, args.scaling_factors)
