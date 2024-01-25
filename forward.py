import pandas as pd

# Load the data from the Excel file
file_path = 'Gait_Analysis_Example.xlsx'
gait_data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
gait_data.head()



# Define the time ranges for analysis
time_ranges = [(16, 19.5), (22.5, 26.5)]

# Filter the data to include only the specified time ranges
filtered_data = gait_data[(gait_data['Time (s)'] >= time_ranges[0][0]) & (gait_data['Time (s)'] <= time_ranges[0][1]) |
                          (gait_data['Time (s)'] >= time_ranges[1][0]) & (gait_data['Time (s)'] <= time_ranges[1][1])]

# Check for any missing data
missing_data_info = filtered_data.isnull().sum()

filtered_data.head(), missing_data_info
print(f'filtered_data.head(): {filtered_data.head()}')
print(f'filtered data has {missing_data_info[0]} missing data points')





import matplotlib.pyplot as plt

# Plotting the filtered data
plt.figure(figsize=(12, 6))
plt.plot(filtered_data['Time (s)'], filtered_data['Forward Acceleration (cm/s^2)'], label='Forward Acceleration')
plt.title('Forward Acceleration vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Forward Acceleration (cm/s^2)')
plt.grid(True)
plt.legend()
plt.show()





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
