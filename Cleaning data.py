import pandas as pd
import numpy as np
# Step 1: Load the CSV file into a DataFrame
file_path = 'combined_prem_stats.csv'  # Make sure the file path is correct
df = pd.read_csv(file_path)

# Step 3: Delete columns from 'B365H' onwards
cols_to_drop = df.columns[df.columns.get_loc("B365H"):]  # Getting all columns from 'B365H' to the end
df.drop(columns=cols_to_drop, inplace=True)

# Step 4: Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')  # Adjust format if necessary

# Removing the "index" and "Referee" columns
df = df.drop(columns=['index', 'Referee'], errors='ignore')

# Create two copies of the dataframe: one for home teams and one for away teams
home_df = df.copy()
away_df = df.copy()

# Set up home team rows
home_df['Team'] = home_df['HomeTeam']
home_df['Opposition'] = home_df['AwayTeam']
home_df['Venue'] = 'Home'

# Set up away team rows
away_df['Team'] = away_df['AwayTeam']
away_df['Opposition'] = away_df['HomeTeam']
away_df['Venue'] = 'Away'

# Concatenate both dataframes
final_df = pd.concat([home_df, away_df], ignore_index=True)

# Drop the original "HomeTeam" and "AwayTeam" columns
final_df = final_df.drop(columns=['HomeTeam', 'AwayTeam'])

final_df = final_df.sort_values(by='Date')

# Rearrange columns by specifying the new order
new_column_order = [
    'Div', 'Date', 'Time', 'Team', 'Opposition', 'Venue', 
    'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 
    'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 
    'HY', 'AY', 'HR', 'AR'
]

# Reorder the DataFrame columns
final_df = final_df[new_column_order]

# Define a function to convert FTR and HTR based on home/away teams
def convert_result(row):
    # Convert Full Time Result (FTR)
    if row['Venue'] == 'Home':
        if row['FTR'] == 'H':
            return 'W'
        elif row['FTR'] == 'A':
            return 'L'
        else:
            return 'D'
    else:
        if row['FTR'] == 'H':
            return 'L'
        elif row['FTR'] == 'A':
            return 'W'
        else:
            return 'D'

def convert_half_time_result(row):
    # Convert Half Time Result (HTR)
    if row['Venue'] == 'Home':
        if row['HTR'] == 'H':
            return 'W'
        elif row['HTR'] == 'A':
            return 'L'
        else:
            return 'D'
    else:
        if row['HTR'] == 'H':
            return 'L'
        elif row['HTR'] == 'A':
            return 'W'
        else:
            return 'D'

# Apply the conversion functions to the DataFrame
final_df['FTR'] = final_df.apply(convert_result, axis=1)
final_df['HTR'] = final_df.apply(convert_half_time_result, axis=1)

# Step 1: Rename the columns for generic names (not tied to home or away)
final_df.rename(columns={
    'FTHG': 'FTG', 'FTAG': 'FTGA',
    'HTHG': 'HTG', 'HTAG': 'HTGA',
    'HS': 'S', 'AS': 'SA',
    'HST': 'ST', 'AST': 'STA',
    'HF': 'F', 'AF': 'FA',
    'HC': 'C', 'AC': 'CA',
    'HY': 'Y', 'AY': 'YA',
    'HR': 'R', 'AR': 'RA'
}, inplace=True)

# Step 2: Function to swap columns for away team rows
def reorder_row(row):
    if row['Venue'] == 'Away':
        # Swap stats when the row corresponds to an away team
        row['FTG'], row['FTGA'] = row['FTGA'], row['FTG']
        row['HTG'], row['HTGA'] = row['HTGA'], row['HTG']
        row['S'], row['SA'] = row['SA'], row['S']
        row['ST'], row['STA'] = row['STA'], row['ST']
        row['F'], row['FA'] = row['FA'], row['F']
        row['C'], row['CA'] = row['CA'], row['C']
        row['Y'], row['YA'] = row['YA'], row['Y']
        row['R'], row['RA'] = row['RA'], row['R']
    return row

# Apply the function to reorder the rows for away teams
final_df = final_df.apply(reorder_row, axis=1)


# Save the rearranged DataFrame to a new CSV
final_df.to_csv('matches.csv', index=False)