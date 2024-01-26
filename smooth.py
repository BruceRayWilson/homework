import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np

class SmoothData:
    def __init__(self, input_file_path: str, output_file_path: str):
        """
        Initialize the SmoothData class with input and output file paths.

        Args:
            input_file_path (str): The path to the CSV file containing the data to be processed.
            output_file_path (str): The path where the processed (smoothed) data will be saved.
        """
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.filtered_data = None
        self.smoothed_data = None

    def load_data(self):
        """
        Load the data from the CSV file specified in the input_file_path attribute.
        The data is stored in the filtered_data attribute and the first few rows are printed.
        """
        self.filtered_data = pd.read_csv(self.input_file_path)
        print(self.filtered_data.head())


    def plot_data(self):
        """
        Plot the original and smoothed acceleration data.
        The plot is saved to a file named 'smoothed_data_plot.png' and then closed.
        """
        plt.figure(figsize=(12, 6))
        # plt.plot(self.filtered_data['Time (s)'], self.filtered_data['Forward Acceleration (cm/s^2)'], label='Original Acceleration')
        plt.plot(self.filtered_data['Time (s)'], self.filtered_data['Smoothed Acceleration'], label='Smoothed Acceleration', color='red')

        # Determine the range for vertical lines
        time_min = np.floor(min(self.filtered_data['Time (s)']))
        time_max = np.ceil(max(self.filtered_data['Time (s)']))
        
        # Add vertical lines at every whole number
        for x in np.arange(time_min, time_max + 1):
            plt.axvline(x, color='grey', linestyle='--', linewidth=0.5)

        # Determine the range for horizontal lines
        accel_min = np.floor(min(self.filtered_data['Smoothed Acceleration']) / 20) * 20
        accel_max = np.ceil(max(self.filtered_data['Smoothed Acceleration']) / 20) * 20

        # Add horizontal lines at every multiple of 20
        for y in np.arange(accel_min, accel_max + 20, 20):
            plt.axhline(y, color='grey', linestyle='--', linewidth=0.5)

        plt.title('Original vs. Smoothed Acceleration Data')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (cm/s^2)')
        plt.legend()
        plt.grid(True)
        plt.savefig('smoothed_data_plot.png')
        plt.show()
        plt.close()


    def exec(self):
        """
        Execute the main workflow of the SmoothData class.
        This method loads the data using load_data, smooths it, generates a plot of the data,
        and then saves the smoothed data to the output_file_path.
        """
        self.load_data()

        # Check if data is loaded
        if self.filtered_data is None:
            print("Data not loaded. Please check the input file path.")
            return

        # Smoothing the data
        self.filtered_data['Smoothed Acceleration'] = savgol_filter(
            self.filtered_data['Forward Acceleration (cm/s^2)'], window_length=51, polyorder=3
        )

        # Plotting the data
        self.plot_data()

        # Making a copy of the smoothed data and saving it
        self.smoothed_data = self.filtered_data.copy()
        self.smoothed_data.to_csv(self.output_file_path, index=False)

# Usage
input_file_path = 'filtered.csv'
output_file_path = 'smoothed.csv'
smooth_data = SmoothData(input_file_path, output_file_path)
smooth_data.exec()


# Read the data
data = pd.read_csv(output_file_path)

# Initialize the 'Braking' and 'Propulsion' columns with zeros
data['Braking'] = 0
data['Propulsion'] = 0

# Loop through the dataset to set values for 'Braking' and 'Propulsion' based on the conditions
for i in range(1, len(data)):
    # Braking: transition from above zero to zero or less
    if data['Smoothed Acceleration'].iloc[i-1] > 0 and data['Smoothed Acceleration'].iloc[i] <= 0:
        data['Braking'].iloc[i] = 1

    # Propulsion: transition from below zero to zero or more
    if data['Smoothed Acceleration'].iloc[i-1] < 0 and data['Smoothed Acceleration'].iloc[i] >= 0:
        data['Propulsion'].iloc[i] = 1

# data.head()
print('data.head()')
print(data.head())







import matplotlib.pyplot as plt

# Save the modified data to a new CSV file
data.to_csv('updated_data.csv', index=False)

# Plotting the data
plt.figure(figsize=(10, 6))

# Plot '|' for Braking equal to 1 using 'Time (s)' column
braking_times = data['Time (s)'][data['Braking'] == 1]
plt.scatter(braking_times, [1] * len(braking_times), marker='|', color='r', label='Braking', s=100)  # s is the size of the marker

# Plot '+' for Propulsion equal to 1 using 'Time (s)' column
propulsion_times = data['Time (s)'][data['Propulsion'] == 1]
plt.scatter(propulsion_times, [1] * len(propulsion_times), marker='+', color='b', label='Propulsion', s=100)  # s is the size of the marker

plt.title('Braking and Propulsion Over Time (s)')
plt.xlabel('Time (s)')
plt.ylabel('Indicator')
plt.legend()

# Show the plot
plt.show()

# Close the plot
plt.close()
