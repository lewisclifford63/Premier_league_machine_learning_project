import os
import pandas as pd

# List to store all dataframes
all_data = []

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# List to store csv file paths
csv_files = []

# Loop over all files in the directory and add CSV files to the list
for file in os.listdir(current_directory):
    if file.endswith(".csv") and file.startswith("Prem"):
        csv_files.append(file)

# Sort the CSV files based on their file names to maintain the correct order
csv_files.sort()

# Initialize a variable to hold the header columns
expected_columns = None

# Loop over the sorted CSV files to read and concatenate
for file in csv_files:
    file_path = os.path.join(current_directory, file)
    print(f"Reading file {file}")
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # If this is the first file, set the expected columns
    if expected_columns is None:
        expected_columns = list(df.columns)
    
    # Find any missing columns and extra columns in the current dataframe
    missing_columns = [col for col in expected_columns if col not in df.columns]
    extra_columns = [col for col in df.columns if col not in expected_columns]
    
    # Add missing columns with NaN values
    for col in missing_columns:
        df[col] = pd.NA
    
    # Drop extra columns that are not in the expected columns
    df = df.drop(columns=extra_columns)
    
    # Ensure the order of columns matches the expected columns
    df = df[expected_columns]
    
    # Append the dataframe to the list
    all_data.append(df)

# Concatenate all dataframes in the list
combined_df = pd.concat(all_data, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_df.to_csv("combined_prem_stats.csv", index=False)

print("All files have been combined and saved to 'combined_prem_stats.csv'")
