import pandas as pd


# First, let's load the data from the provided file to understand its structure and contents.
import pandas as pd

# Load the data from the file
file_path = 'filtered.csv'
filtered_data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
filtered_data.head()


import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Smoothing the acceleration data using Savitzky-Golay filter
filtered_data['Smoothed Acceleration'] = savgol_filter(filtered_data['Forward Acceleration (cm/s^2)'], window_length=51, polyorder=3)

# Plotting the original and smoothed acceleration data
plt.figure(figsize=(12, 6))
plt.plot(filtered_data['Time (s)'], filtered_data['Forward Acceleration (cm/s^2)'], label='Original Acceleration')
plt.plot(filtered_data['Time (s)'], filtered_data['Smoothed Acceleration'], label='Smoothed Acceleration', color='red')
plt.title('Original vs. Smoothed Acceleration Data')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (cm/s^2)')
plt.legend()
plt.grid(True)
plt.show()
