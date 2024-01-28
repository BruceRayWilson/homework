import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Leg:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.file_path)

    def detect_batches(self, time_column, gap_threshold=1):
        time_diff = self.data[time_column].diff()
        batch_indices = time_diff > gap_threshold
        self.data['Batch'] = np.cumsum(batch_indices).fillna(0)

    def mark_leg_in_segments(self, roll_column):
        self.data['Leg'] = ''  # Initializing the Leg column
        self.data['Roll_diff'] = self.data[roll_column].diff()

        # Iterate through each batch
        for batch in self.data['Batch'].unique():
            batch_data = self.data[self.data['Batch'] == batch]

            # Right Foot Down Segments
            right_start_indices = batch_data[(batch_data['Roll_diff'].shift(-1) > 0) & (batch_data['Roll_diff'] <= 0) & (batch_data[roll_column] < -1.5)].index
            for start_idx in right_start_indices:
                end_idx = batch_data.loc[start_idx:][batch_data['Roll (deg)'] >= 0].first_valid_index()
                if end_idx is not None:
                    self.data.loc[start_idx:end_idx, 'Leg'] = 'Right'

            # Left Foot Down Segments
            left_start_indices = batch_data[(batch_data['Roll_diff'].shift(-1) <= 0) & (batch_data['Roll_diff'] > 0) & (batch_data[roll_column] > 2.5)].index
            for start_idx in left_start_indices:
                # end_idx = batch_data.loc[start_idx:][batch_data['Roll (deg)'] >= 0].first_valid_index()
                end_idx = batch_data.loc[start_idx:][batch_data['Roll (deg)'] <= 0].first_valid_index()
                if end_idx is not None:
                    self.data.loc[start_idx:end_idx, 'Leg'] = 'Left'

    def plot_data(self):
        plt.figure(figsize=(12, 6))

        # Plotting each point with small circles
        for index, row in self.data.iterrows():
            if row['Leg'] == 'Right':
                color = 'red'
            elif row['Leg'] == 'Left':
                color = 'black'
            else:
                color = 'yellow'
            
            plt.scatter(row['Time (s)'], row['Roll (deg)'], color=color, s=5)  # s=5 for small circles

        # Setting plot labels and title
        plt.xlabel('Time (s)')
        plt.ylabel('Roll (deg)')
        plt.title('Roll Angle Over Time with Updated Right and Left Foot Down Segments (Small Circles)')

        # Saving the plot to a file in PNG format
        plt.savefig('leg.png')

        # Closing the plot to free up memory
        plt.close()


    def exec(self):
        self.load_data()
        self.detect_batches('Time (s)')
        self.mark_leg_in_segments('Roll (deg)')
        self.plot_data()

# Usage
leg = Leg('filtered_roll.csv')
leg.exec()
