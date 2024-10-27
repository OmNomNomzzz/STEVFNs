import os
import pandas as pd
import numpy as np

# Define the root directory where the folders are located
root_dir = os.getcwd()

# Initialize a list to store DataFrames
dataframes = []

# Loop through all files and directories in the root directory
for folder in os.listdir(root_dir):
    # Check if the folder name starts and ends with 'Autarky'
    if folder.startswith('Autarky_') or folder.endswith('_Autarky'):
        # Construct the full path to the CSV file
        csv_file = os.path.join(root_dir, folder, 'total_data_unrounded.csv')
        
        # Check if the CSV file exists
        if os.path.exists(csv_file):
            # Read the CSV file and add to the list of DataFrames
            data = pd.read_csv(csv_file)
            # Round the values for emissions and cost to 1 decimal
            data['collaboration_emissions'] = np.round(data['collaboration_emissions'], decimals=1)
            data['technology_cost'] = np.round(data['technology_cost'], decimals=1)
            dataframes.append(data)

# Concatenate all DataFrames in the list
combined_data_autarky = pd.concat(dataframes, ignore_index=True)

# Save the combined, rounded data to a new CSV file in the root directory
combined_data_autarky.to_csv(os.path.join(root_dir, 'total_data_autarky.csv'), index=False)


# Initialize a list to store DataFrames
dataframes_collab = []

# Loop through all files and directories in the root directory
for folder in os.listdir(root_dir):
    
    if folder.startswith('Autarky_') or folder.endswith('_Collab'):
        # Construct the full path to the CSV file
        csv_file = os.path.join(root_dir, folder, 'total_data_unrounded.csv')
        
        # Check if the CSV file exists
        if os.path.exists(csv_file):
            # Read the CSV file and add to the list of DataFrames
            data = pd.read_csv(csv_file)
            # Round the values for emissions and cost to 1 decimal
            data['collaboration_emissions'] = np.round(data['collaboration_emissions'], decimals=1)
            data['technology_cost'] = np.round(data['technology_cost'], decimals=1)
            dataframes_collab.append(data)

# Concatenate all DataFrames in the list
combined_data_collab = pd.concat(dataframes_collab, ignore_index=True)

# Save the combined, rounded data to a new CSV file in the root directory
combined_data_collab.to_csv(os.path.join(root_dir, 'total_data_collaboration.csv'), index=False)









