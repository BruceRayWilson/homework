import pandas as pd
import matplotlib.pyplot as plt

class ExtractData:
    def __init__(self, file_name):
        self.file_name = file_name
        self.gait_data = None
        self.filtered_data = None
        self.missing_data_info = None

    def load_data(self):
        self.gait_data = pd.read_excel(self.file_name)
        print(self.gait_data.head())  # Display the first few rows

    def filter_data(self, time_ranges):
        self.filtered_data = self.gait_data[
            (self.gait_data['Time (s)'] >= time_ranges[0][0]) & (self.gait_data['Time (s)'] <= time_ranges[0][1]) |
            (self.gait_data['Time (s)'] >= time_ranges[1][0]) & (self.gait_data['Time (s)'] <= time_ranges[1][1])
        ]

    def check_missing_data(self):
        self.missing_data_info = self.filtered_data.isnull().sum()
        print(self.filtered_data.head())  # Display the first few rows of filtered data
        print(f'Filtered data has {self.missing_data_info[0]} missing data points')

    def plot_data(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.filtered_data['Time (s)'], self.filtered_data['Forward Acceleration (cm/s^2)'], label='Forward Acceleration')
        plt.title('Forward Acceleration vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Forward Acceleration (cm/s^2)')
        plt.grid(True)
        plt.legend()
        plt.show()

    def exec(self):
        self.load_data()
        time_ranges = [(16, 19.5), (22.5, 26.5)]
        self.filter_data(time_ranges)
        self.check_missing_data()
        self.plot_data()
        return self.filtered_data, self.missing_data_info

# Example usage
extractor = ExtractData('Gait_Analysis_Example.xlsx')
filtered_data, missing_data_info = extractor.exec()





import numpy as np

# Calculate the derivative (rate of change) of the forward acceleration
filtered_data['Acceleration Derivative'] = np.gradient(filtered_data['Forward Acceleration (cm/s^2)'], filtered_data['Time (s)'])

# Function to detect phase changes
def detect_phase_changes(data):
    braking_phase_starts = []
    propulsion_phase_starts = []

    # Iterate through the data to find where the derivative changes sign
    for i in range(1, len(data)):
        # Detect start of braking phase (positive to negative derivative)
        if data['Acceleration Derivative'].iloc[i-1] > 0 and data['Acceleration Derivative'].iloc[i] <= 0:
            braking_phase_starts.append(data['Time (s)'].iloc[i])

        # Detect start of propulsion phase (negative to positive derivative)
        if data['Acceleration Derivative'].iloc[i-1] < 0 and data['Acceleration Derivative'].iloc[i] >= 0:
            propulsion_phase_starts.append(data['Time (s)'].iloc[i])

    return braking_phase_starts, propulsion_phase_starts

# Detecting phase changes in the filtered data
braking_phase_starts, propulsion_phase_starts = detect_phase_changes(filtered_data)

# braking_phase_starts, propulsion_phase_starts

# This replaces the first print statement                                                                                                                    
for col in filtered_data.columns:                                                                                                                            
    print(f'{col}: {filtered_data[col].head().tolist()}')                                                                                                    
                                                                                                                                                            
# This replaces the second print statement                                                                                                                   
print(f'filtered data has {missing_data_info[0]} missing data points')       
