import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

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
