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
            time_offset = 40 * i
            modified_data['Time (s)'] += time_offset

            # Applying multiplier to the 'Roll (deg)' column
            roll_multiplier = np.random.uniform(0.95, 1.05) if i > 0 else 1.0
            modified_data['Roll (deg)'] *= roll_multiplier

            # Adding a multiplier column
            modified_data['Multiplier'] = roll_multiplier

            all_copies.append(modified_data)

        # Concatenate all copies into a single DataFrame
        combined_data = pd.concat(all_copies, ignore_index=True)

        # Saving the combined data to 'roll.csv'
        combined_data.to_csv('roll.csv', index=False)

# Example usage
gen_roll_data = GenRollData('filtered_roll.csv')
gen_roll_data.exec()
