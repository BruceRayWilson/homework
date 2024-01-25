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
        self.time_ranges = None

    def get_time_ranges(self):
        """
        Generate time ranges for gait analysis data.
        """

        # Sort self.concatenated_df by 'Toe-Off'
        self.concatenated_df.sort_values(by='Toe-Off', inplace=True)

        # Calculate a new column named 'Time' which is 'COM Above Toe' minus 'Toe-Off'
        self.concatenated_df['Time'] = self.concatenated_df['COM Above Toe'] - self.concatenated_df['Toe-Off']

        # Calculate gap_check equals the max of 'Time' times margin
        margin = 1.5
        gap_check = self.concatenated_df['Time'].max() * margin

        # Calculate a new column named 'Next COM Above Toe'
        self.concatenated_df['Next COM Above Toe'] = self.concatenated_df['COM Above Toe'].shift(-1)

        # Begin generating the time ranges for the gait analysis data
        # Use 'Next COM Above Toe' and gap_check to find the time ranges of the gait analysis data
        # Store the time ranges in self.time_ranges: list[tuple[float, float]]
        self.time_ranges = []
        start_time = self.concatenated_df.iloc[0]['Toe-Off']
        for index, row in self.concatenated_df.iterrows():
            if index < len(self.concatenated_df) - 1:
                current_time = row['COM Above Toe']
                next_time = row['Next COM Above Toe']
                if next_time - current_time > gap_check:
                    self.time_ranges.append((start_time, current_time))
                    next_index = index + 1
                    start_time = self.concatenated_df.iloc[next_index]['Toe-Off']
            else:
                self.time_ranges.append((start_time, self.concatenated_df.iloc[-1]['COM Above Toe']))
        # End generating the time ranges for the gait analysis data

        # Print self.time_ranges
        print(self.time_ranges)

    def concatenate_dataframes(self):
        """
        Concatenate two dataframes vertically after verifying the column names match.
        Initially, remove the postfix '.1' from each of the column names in self.right_side_df.
        """
        # print(f'self.left_side_df columns: {self.left_side_df.columns}')

        # Removing the postfix '.1' from each column name in self.right_side_df
        self.right_side_df.columns = [col.replace('.1', '') for col in self.right_side_df.columns]
        # print(f'self.right_side_df columns: {self.right_side_df.columns}')

        # Check if the columns in both dataframes match
        if list(self.left_side_df.columns) == list(self.right_side_df.columns):
            # Columns match, proceed with concatenation
            self.concatenated_df = pd.concat([self.left_side_df, self.right_side_df], axis=0)

            # Drop rows with NaN values
            self.concatenated_df.dropna(inplace=True)
        else:
            # Handle the case where columns do not match
            print("Column names do not match. Cannot concatenate dataframes.")
            print(f'Left side dataframe columns: {self.left_side_df.columns}')
            print(f'Right side dataframe columns: {self.right_side_df.columns}')
            # Optionally, you can implement logic here to reconcile the column names
            # For example, you might rename columns or drop non-matching ones
            # Then, perform the concatenation after handling the mismatch
            # self.concatenated_df = pd.concat([adjusted_left_side_df, adjusted_right_side_df], axis=0)

        print("\nConcatenated Data Head:")
        if hasattr(self, 'concatenated_df'):
            # print(self.concatenated_df.head())  # Display the first few rows of concatenated_df
            print(self.concatenated_df)
        else:
            print("Concatenated dataframe not created due to column mismatch.")

    def load_data(self):
        """
        Load data from an Excel file, create different dataframes, and print their contents.
        The column names for the Left and Right sides are assumed to be on the second row.
        """
        # Load the entire dataset, setting the first row as header
        self.gait_data = pd.read_excel(self.file_name, header=0)
        print("Initial Data Head:")
        print(self.gait_data.head())  # Display the first few rows

        # Creating the dataframe with the first three columns
        self.gait_data_df = self.gait_data.iloc[:, :3]
        print("\nGait Data Head:")
        print(self.gait_data_df.head())  # Display the first few rows of gait_data_df

        # Load the entire dataset, setting the second row as header
        self.gait_data = pd.read_excel(self.file_name, header=1)
        print("Second Data Head:")
        print(self.gait_data.head())  # Display the first few rows

        # Drop the first four columns from the gait_data
        self.gait_data = self.gait_data.iloc[:, 4:]

        # Collect the first four columns in self.left_side_df
        self.left_side_df = self.gait_data.iloc[:, :4]

        # Drop rows with NaN values
        self.left_side_df.dropna(inplace=True)
        print("\n\nLeft Side Data Head:")
        print(self.left_side_df.head())  # Display the first few rows of left_side_df

        # Drop the first five columns from the gait_data (total drop is now nine columns)
        self.gait_data = self.gait_data.iloc[:, 5:]

        # Collect the first four columns in self.right_side_df
        self.right_side_df = self.gait_data.iloc[:, :4]

        # Drop rows with NaN values
        self.right_side_df.dropna(inplace=True)
        print("\n\nRight Side Data Head:")
        print(self.right_side_df.head())  # Display the first few rows of right_side_df

        # Creating the concatenated dataframe
        self.concatenate_dataframes()

        # Load the entire dataset, setting the first row as header
        self.gait_data = pd.read_excel(self.file_name, header=0)
        # print("Final Data Head:")
        # print(self.gait_data.head())  # Display the first few rows


    def filter_data(self):
        """
        Filter the data based on time ranges.
        """
        self.filtered_data = self.gait_data[
            (self.gait_data['Time (s)'] >= self.time_ranges[0][0]) & (self.gait_data['Time (s)'] <= self.time_ranges[0][1]) |
            (self.gait_data['Time (s)'] >= self.time_ranges[1][0]) & (self.gait_data['Time (s)'] <= self.time_ranges[1][1])
        ]

    def check_missing_data(self):
        """
        Check for any missing data in the filtered dataset.
        """
        self.missing_data_info = self.filtered_data.isnull().sum()
        print('\nself.filtered_data:')
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
        self.time_ranges = [(15, 19), (22, 25), (29, 32), (35, 38)]
        # self.get_time_ranges()
        self.filter_data()
        self.check_missing_data()
        self.plot_data()
        return self.filtered_data, self.missing_data_info

# Example usage
extractor = ExtractData('Gait_Analysis_Example.xlsx')
filtered_data, missing_data_info = extractor.exec()
