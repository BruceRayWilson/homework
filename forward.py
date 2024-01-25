import pandas as pd
import matplotlib.pyplot as plt

class ExtractData:
    def __init__(self, file_name: str):
        """
        Initialize the ExtractData class with the specified file name.

        Args:
        file_name (str): The name of the file containing the gait analysis data.
        """
        self.file_name = file_name
        self.gait_data_df = None
        self.left_side_df = None
        self.right_side_df = None
        self.concatenated_df = None
        self.filtered_data = None
        self.missing_data_info = None


    def load_data(self):
        """
        Load data from an Excel file, create different dataframes, and print their contents.
        The column names for the Left and Right sides are assumed to be on the second row.
        """
        # Load the entire dataset, setting the second row as header
        self.gait_data = pd.read_excel(self.file_name)
        print("Initial Data Head:")
        print(self.gait_data.head())  # Display the first few rows

        # Creating the dataframe with the first three columns
        self.gait_data_df = self.gait_data.iloc[:, :3]
        print("\nGait Data Head:")
        print(self.gait_data_df.head())  # Display the first few rows of gait_data_df

        # Identifying columns for Left and Right sides
        left_cols = [col for col in self.gait_data.columns if 'Left' in col]
        right_cols = [col for col in self.gait_data.columns if 'Right' in col]

        # Creating the dataframes for Left and Right sides
        self.left_side_df = self.gait_data[left_cols]
        print("\nLeft Side Data Head:")
        print(self.left_side_df.head())  # Display the first few rows of left_side_df

        self.right_side_df = self.gait_data[right_cols]
        print("\nRight Side Data Head:")
        print(self.right_side_df.head())  # Display the first few rows of right_side_df

        # Creating the concatenated dataframe
        self.concatenated_df = pd.concat([self.left_side_df, self.right_side_df], axis=1)
        print("\nConcatenated Data Head:")
        print(self.concatenated_df.head())  # Display the first few rows of concatenated_df


    def filter_data(self, time_ranges: list[tuple[float, float]]):
        """
        Filter the data based on provided time ranges.

        Args:
        time_ranges (list of tuples): Each tuple contains the start and end of a time range.
        """
        self.filtered_data = self.gait_data[
            (self.gait_data['Time (s)'] >= time_ranges[0][0]) & (self.gait_data['Time (s)'] <= time_ranges[0][1]) |
            (self.gait_data['Time (s)'] >= time_ranges[1][0]) & (self.gait_data['Time (s)'] <= time_ranges[1][1])
        ]

    def check_missing_data(self):
        """
        Check for any missing data in the filtered dataset.
        """
        self.missing_data_info = self.filtered_data.isnull().sum()
        print(self.filtered_data.head())  # Display the first few rows of filtered data
        print(f'Filtered data has {self.missing_data_info[0]} missing data points')

    def plot_data(self):
        """
        Plot the filtered data.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.filtered_data['Time (s)'], self.filtered_data['Forward Acceleration (cm/s^2)'], label='Forward Acceleration')
        plt.title('Forward Acceleration vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Forward Acceleration (cm/s^2)')
        plt.grid(True)
        plt.legend()
        plt.show()

    def exec(self) -> tuple[pd.DataFrame, pd.Series]:
        """
        Execute the data extraction and processing flow and return the filtered data and missing data info.

        Returns:
        tuple: Contains the filtered data as a DataFrame and missing data information as a Series.
        """
        self.load_data()
        time_ranges = [(16, 19.5), (22.5, 26.5)]
        self.filter_data(time_ranges)
        self.check_missing_data()
        self.plot_data()
        return self.filtered_data, self.missing_data_info

# Example usage
extractor = ExtractData('Gait_Analysis_Example.xlsx')
filtered_data, missing_data_info = extractor.exec()
