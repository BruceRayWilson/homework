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
        self.time_ranges = None

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
        # Initialize an empty DataFrame for filtered data
        self.filtered_data = pd.DataFrame()

        # Loop through each time range in self.time_ranges
        for start, end in self.time_ranges:
            # Apply the filter for the current time range
            current_filtered = self.gait_data_df[(self.gait_data_df['Time (s)'] >= start) & (self.gait_data_df['Time (s)'] <= end)]

            # Combine the filtered data from the current time range with the previous ones
            self.filtered_data = pd.concat([self.filtered_data, current_filtered])

    def plot_roll(self, filtered_data: pd.DataFrame, filename: str):
        """
        Plot the data and save the plot to a file.

        Args:
        filtered_data (pd.DataFrame): The DataFrame containing the data to be plotted.
        filename (str): The name of the file to save the plot, including .png extension.
        """
        # Create a new figure with specific size
        plt.figure(figsize=(12, 6))

        # Plotting the 'Roll' against 'Time'
        plt.plot(filtered_data['Time (s)'], filtered_data['Roll (deg)'], label='Roll')

        # Setting the title of the plot
        plt.title('Roll vs Time')

        # Setting labels for x and y axes
        plt.xlabel('Time (s)')
        plt.ylabel('Roll (degrees)')

        # Enabling grid for better readability
        plt.grid(True)

        # Displaying the legend
        plt.legend()

        # Saving the plot to a file in PNG format
        plt.savefig(filename)

        # Displaying the plot
        plt.show()

        # Closing the plot to free up memory
        plt.close()

    def plot_acceleration(self, filtered_data: pd.DataFrame, filename: str):
        """
        Plot the data and save the plot to a file.

        Args:
        filtered_data (pd.DataFrame): The DataFrame containing the data to be plotted.
        filename (str): The name of the file to save the plot, including .png extension.
        """
        # Create a new figure with specific size
        plt.figure(figsize=(12, 6))

        # Plotting the 'Forward Acceleration' against 'Time'
        plt.plot(filtered_data['Time (s)'], filtered_data['Forward Acceleration (cm/s^2)'], label='Forward Acceleration')

        # Setting the title of the plot
        plt.title('Forward Acceleration vs Time')

        # Setting labels for x and y axes
        plt.xlabel('Time (s)')
        plt.ylabel('Forward Acceleration (cm/s^2)')

        # Enabling grid for better readability
        plt.grid(True)

        # Displaying the legend
        plt.legend()

        # Saving the plot to a file in PNG format
        plt.savefig(filename)

        # Displaying the plot
        plt.show()

        # Closing the plot to free up memory
        plt.close()


    def save_data(self, filtered_data: pd.DataFrame, filename: str):
        """
        Save the filtered data to a file.

        Args:
        filtered_data (pd.DataFrame): The DataFrame containing the data to be saved.
        filename (str): The name of the file to save the data, including file extension.
        """
        # Saving the DataFrame to a file
        filtered_data.to_csv(filename, index=False)


    def exec(self) -> tuple[pd.DataFrame, pd.Series]:
        """
        Execute the data extraction and processing flow and return the filtered data and missing data info.

        Returns:
        tuple: Contains the filtered data as a DataFrame and missing data information as a Series.
        """
        self.load_data()
        self.time_ranges = [(15, 19), (22, 26), (29, 32), (35, 38)]
        self.filter_data()
        self.plot_acceleration(self.filtered_data, 'filtered_acceleration.png')
        self.save_data(self.filtered_data, 'filtered_acceleration.csv')

        self.load_data()
        self.time_ranges = [(15, 19.5), (22.5, 26.5), (29, 33), (35, 39)]
        self.filter_data()
        self.plot_roll(self.filtered_data, 'filtered_roll.png')
        self.save_data(self.filtered_data, 'filtered_roll.csv')

# Example usage
extractor = ExtractData('Gait_Analysis_Example.xlsx')
extractor.exec()
