import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Leg:
    """
    A class to analyze leg stance phases from roll angle data.

    Attributes:
        file_path (str): The path to the CSV file containing the data.
        data (pd.DataFrame): The loaded data from the CSV file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the Leg class with the file path of the data.
        """
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """
        Load data from the CSV file into a pandas DataFrame.
        """
        self.data = pd.read_csv(self.file_path)

    def detect_batches(self, time_column: str, gap_threshold: float = 1):
        """
        Detect batches in the data based on a specified time gap threshold.

        Args:
            time_column (str): The column name in the DataFrame that contains time data.
            gap_threshold (float): The threshold in time units to detect a new batch.
        """
        time_diff = self.data[time_column].diff()
        batch_indices = time_diff > gap_threshold
        self.data['Batch'] = np.cumsum(batch_indices).fillna(0)

    def mark_leg_in_segments(self, roll_column: str):
        """
        Mark which leg the subject is standing on during different segments.

        Args:
            roll_column (str): The column name in the DataFrame that contains roll angle data.
        """
        # Initialize and compute the required columns
        self.data['Leg'] = ''
        self.data['Roll_diff'] = self.data[roll_column].diff()

        # Process each batch separately
        for batch in self.data['Batch'].unique():
            batch_data = self.data[self.data['Batch'] == batch]

            # Identify right and left leg stance segments
            self._process_leg_segments(batch_data, roll_column)

    def _process_leg_segments(self, batch_data: pd.DataFrame, roll_column: str):
        """
        Helper method to process leg segments within a batch of data.

        Args:
            batch_data (pd.DataFrame): The data for the current batch.
            roll_column (str): The column name for roll angle data.
        """
        # Right Foot Down Segments
        right_start_indices = batch_data[(batch_data['Roll_diff'].shift(-1) > 0) & 
                                         (batch_data['Roll_diff'] <= 0) & 
                                         (batch_data[roll_column] < -1.5)].index
        for start_idx in right_start_indices:
            end_idx = batch_data.loc[start_idx:][batch_data['Roll (deg)'] >= 0].first_valid_index()
            if end_idx is not None:
                self.data.loc[start_idx:end_idx, 'Leg'] = 'Right'

        # Left Foot Down Segments
        left_start_indices = batch_data[(batch_data['Roll_diff'].shift(-1) <= 0) & 
                                        (batch_data['Roll_diff'] > 0) & 
                                        (batch_data[roll_column] > 2.5)].index
        for start_idx in left_start_indices:
            end_idx = batch_data.loc[start_idx:][batch_data['Roll (deg)'] <= 0].first_valid_index()
            if end_idx is not None:
                self.data.loc[start_idx:end_idx, 'Leg'] = 'Left'

    def plot_data(self):
        """
        Plot the roll angle data with colors indicating the stance leg.
        """
        plt.figure(figsize=(12, 6))

        # Plot each data point
        for index, row in self.data.iterrows():
            color = 'red' if row['Leg'] == 'Right' else 'black' if row['Leg'] == 'Left' else 'yellow'
            plt.scatter(row['Time (s)'], row['Roll (deg)'], color=color, s=5)

        plt.xlabel('Time (s)')
        plt.ylabel('Roll (deg)')
        plt.title('Roll Angle Over Time with Leg Stance Phases')
        plt.savefig('leg.png')
        plt.show()
        plt.close()


    def calculate_max_deviation(self) -> pd.DataFrame:
        """
        Calculate the maximum angular roll deviation for each contiguous set of rows
        during single leg stance phases.

        Returns:
            pd.DataFrame: A DataFrame containing the max deviation data for each stance segment.
        """
        max_deviation_data = []

        # Iterate through each batch
        for batch in self.data['Batch'].unique():
            batch_data = self.data[self.data['Batch'] == batch]

            # Process for each leg
            for leg in ['Right', 'Left']:
                leg_data = batch_data[batch_data['Leg'] == leg]

                # Find contiguous segments within the leg data
                # A segment changes when there is a break in the index sequence
                segments = leg_data['Roll (deg)'].groupby((leg_data.index.to_series().diff() != 1).cumsum())

                # Calculate max deviation for each segment
                for segment_num, segment_data in segments:
                    if not segment_data.empty:
                        time_start = segment_data.index.min()
                        time_end = segment_data.index.max()
                        max_deviation = segment_data.abs().max()

                        # Append this information to the max_deviation_data list
                        max_deviation_data.append({
                            'Batch': batch, 
                            'Leg': leg, 
                            'Segment': segment_num,
                            'Time Start': self.data.loc[time_start, 'Time (s)'],
                            'Time End': self.data.loc[time_end, 'Time (s)'],
                            'Max Deviation': max_deviation
                        })

        return pd.DataFrame(max_deviation_data)

    def save_data(self, output_file_path: str):
        """
        Save the modified data to a CSV file.

        Args:
            output_file_path (str): Path to save the output CSV file.
        """
        self.data.to_csv(output_file_path, index=False)

    def exec(self):
        """
        Execute the entire process of data loading, processing, plotting, and saving.
        """
        self.load_data()
        self.detect_batches('Time (s)')
        self.mark_leg_in_segments('Roll (deg)')
        self.plot_data()
        max_deviation_df = self.calculate_max_deviation()
        max_deviation_df.to_csv('max_deviation_data.csv', index=False)

# Usage
leg = Leg('filtered_roll.csv')
leg.exec()
