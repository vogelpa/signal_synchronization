# This script was used to plot outlier flags for the images in the presentation.
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os
import sys

def plot_interactive_html(df1, df2, signal_column1, signal_column2, input_file1, input_file2, plot_settings):
    scaling_factor_reference = plot_settings['scaling_factor_reference']
    scaling_factor_align = plot_settings['scaling_factor_align']

    fig = go.Figure()

    # Plot original signal from input_file1
    fig.add_trace(go.Scatter(
        x=df1['timestamp'],
        y=df1[signal_column1] * scaling_factor_reference,
        mode='lines',
        name=f'{os.path.basename(input_file1)}'
    ))

    # Plot original signal from input_file2
    fig.add_trace(go.Scatter(
        x=df2['timestamp'],
        y=df2[signal_column2] * scaling_factor_align,
        mode='lines',
        name=f'{os.path.basename(input_file2)}',
        line=dict(color='orange')
    ))

    # Mark outliers for input_file1
    outliers_df1 = df1[df1['outlier'] == True]

    fig.add_trace(go.Scatter(
        x=outliers_df1['timestamp'],
        y=outliers_df1[signal_column1] * scaling_factor_reference,
        mode='markers',
        marker=dict(color='red', size=8),
        name='Outliers File 1'
    ))

    # Mark outliers for input_file2
    outliers_df2 = df2[df2['outlier'] == True]

    fig.add_trace(go.Scatter(
        x=outliers_df2['timestamp'],
        y=outliers_df2[signal_column2] * scaling_factor_align,
        mode='markers',
        marker=dict(color='purple', size=8),
        name='Outliers File 2'
    ))

    # Set plot title and labels
    fig.update_layout(
        title='Detected Outliers and Signal Comparison',
        xaxis_title='Timestamp',
        yaxis_title='1D Signal',
        template='plotly_white'
    )

    # Save and open the plot as an HTML file
    output_file = 'interactive_plot.html'
    pio.write_html(fig, file=output_file, auto_open=True)
    print(f"Plot saved to {output_file}.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python visualization.py file1.csv file2.csv")
        sys.exit(1)

    # Read input file paths
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    # Read CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Define signal column names and plot settings
    signal_column1 = '1d_signal'  # Adjust if your signal column has a different name
    signal_column2 = '1d_signal'  # Adjust if your signal column has a different name
    plot_settings = {
        'scaling_factor_reference': 1500,
        'scaling_factor_align': 1.0
    }

    # Call the plotting function
    plot_interactive_html(df1, df2, signal_column1, signal_column2, file1, file2, plot_settings)

if __name__ == '__main__':
    main()