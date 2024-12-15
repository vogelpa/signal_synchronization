import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read data from CSV file
data = pd.read_csv('error_quantification.csv')

# Extracting data for Accelerometer and Pressure Mat, and sorting by Drift (in s)
accelerometer_data = data[data['Sensor Type'] == 'Accelerometer'].sort_values(by='Drift (in s)')
pressure_mat_data = data[data['Sensor Type'] == 'Pressure Mat'].sort_values(by='Drift (in s)')

# Plotting the figures

# Plot MAE with Standard Deviation
plt.figure(figsize=(10, 6))
plt.errorbar(accelerometer_data['Drift (in s)'], accelerometer_data['MAE'], yerr=accelerometer_data['Standard Deviation'], label="Accelerometer", marker='o', capsize=5)
plt.errorbar(pressure_mat_data['Drift (in s)'], pressure_mat_data['MAE'], yerr=pressure_mat_data['Standard Deviation'], label="Pressure Mat", marker='o', capsize=5)

plt.xlabel("Drift (s)")
plt.ylabel("MAE (s)")
plt.title("Drift vs MAE (with Standard Deviation)")
plt.legend()
plt.grid(True)

# Ensure y-axis doesn't go below zero
plt.ylim(bottom=0)

# Save the plot in the current directory
plt.savefig("drift_level_vs_average_time_difference_with_std_dev.png")
plt.close()

# Plot RMSE
plt.figure(figsize=(10, 6))
plt.plot(accelerometer_data['Drift (in s)'], accelerometer_data['RMSE'], label="Accelerometer", marker='o')
plt.plot(pressure_mat_data['Drift (in s)'], pressure_mat_data['RMSE'], label="Pressure Mat", marker='o')

plt.xlabel("Drift (s)")
plt.ylabel("RMSE (s)")
plt.title("Drift vs RMSE")
plt.legend()
plt.grid(True)

# Ensure y-axis doesn't go below zero
plt.ylim(bottom=0)

# Save the plot in the current directory
plt.savefig("drift_level_vs_rmse.png")
plt.close()
