import pandas as pd
import numpy as np

class GenRollData:
    def __init__(self, filename):
        self.filename = filename
        self.data = pd.read_csv(filename)
    
    def exec(self):
        all_copies = []  # List to hold all modified copies

        for i in range(10):
            modified_data = self.data.copy()
            
            # Adding offset to the 'Time (s)' column
            time_offset = 40 * i
            modified_data['Time (s)'] += time_offset

            # Multiplying the 'Roll (deg)' column by a random factor for copies after the first
            if i > 0:
                roll_factor = np.random.uniform(0.95, 1.05)
                modified_data['Roll (deg)'] *= roll_factor

            # Append the modified copy to the list
            all_copies.append(modified_data)

        # Concatenate all copies into a single DataFrame
        combined_data = pd.concat(all_copies, ignore_index=True)

        # Saving the combined data to a single file 'roll.csv'
        combined_data.to_csv('roll.csv', index=False)

# Assuming that the 'filtered_roll.csv' file is available in the same directory
# Create an instance of the class and call exec()
gen_roll_data = GenRollData('filtered_roll.csv')
gen_roll_data.exec()

# This code will generate a single file 'roll.csv' containing all modified copies of the data.
