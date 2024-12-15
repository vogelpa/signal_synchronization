# This script was used to plot the derivative of the 1D signal and the original 1D signal.

import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def main(input_file):
    # Load the CSV into a DataFrame
    df = pd.read_csv(input_file)

    # Convert timestamp to datetime and extract only the time part
    df['time'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S.%f')

    # Calculate the derivative of '1d_signal'
    df['1d_signal_derivative'] = df['1d_signal'].diff()

    # Plot the '1d_signal' column and its derivative with time as the x-axis
    fig, ax = plt.subplots(figsize=(14, 8))

    # Original signal plot
    ax.plot(df['time'], df['1d_signal'], label='1D Signal', color='b')

    # Derivative signal plot
    ax.plot(df['time'], df['1d_signal_derivative'], label='Derivative of 1D Signal', color='g')

    # Set x-axis major ticks every 100th timestamp
    ax.set_xticks(df['time'][::10])
    ax.set_xlabel('Time')
    ax.set_ylabel('Signal / Derivative')
    ax.set_title('1D Signal and Derivative over Time')
    ax.legend()
    ax.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)