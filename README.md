# Premier League Match Prediction

This project aims to predict the outcome of Premier League football matches using machine learning techniques, specifically the Random Forest algorithm. The process involves combining multiple seasons of match data, cleaning and preprocessing the data, and training a machine learning model to make predictions.

## Project Structure

The project consists of three main Python scripts executed in the following order:

1. **combine_data.py**: Combines multiple CSV files containing football match data into a single file.
2. **cleaning_data.py**: Cleans and processes the combined data, transforming it into a format suitable for machine learning.
3. **ML_predictions.py**: Trains a machine learning model to predict match outcomes and evaluates its performance.

## Prerequisites

Ensure you have Python 3 installed, along with the necessary libraries:
- `pandas`
- `numpy`
- `scikit-learn`

You can install these dependencies using the following command:
```bash
pip install pandas numpy scikit-learn
```

## Usage

### Step 1: Combine Data

The `combine_data.py` script combines multiple CSV files containing football match data into a single file.

- Place all CSV files in the same directory as `combine_data.py`.
- Make sure the CSV files start with "Prem" and are named in chronological order for correct processing (e.g., "Prem 19-20.csv", "Prem 20-21.csv", etc.).

To run the script, execute:
```bash
python combine_data.py
```
This will generate a `combined_prem_stats.csv` file containing the combined data from all seasons.

### Step 2: Clean and Preprocess Data

The `cleaning_data.py` script cleans and preprocesses the combined data:
- Removes unnecessary columns (e.g., betting odds and referee).
- Converts match results from 'H' (Home), 'D' (Draw), and 'A' (Away) to 'W' (Win), 'D' (Draw), and 'L' (Loss) for both home and away teams.
- Adds rolling averages to capture recent form for each team.

To run the script, execute:
```bash
python cleaning_data.py
```
This will produce a `matches.csv` file containing the cleaned data.

### Step 3: Train and Predict Using a Machine Learning Model

The `ML_predictions.py` script trains a Random Forest model to predict match outcomes:
- Splits the data into training and testing sets based on the date.
- Uses the cleaned data to train the model on the most relevant features.
- Evaluates the model's accuracy and precision, and calculates the prediction accuracy for cases where both teams' match predictions agree.

To run the script, execute:
```bash
python ML_predictions.py
```
This will display the overall accuracy and the accuracy of predictions when both teams' predictions align.

## File Descriptions

### 1. combine_data.py
- **Purpose**: Combines multiple CSV files containing match statistics into one file.
- **Output**: `combined_prem_stats.csv`
- **Key Steps**:
  - Reads all files starting with "Prem" in the current directory.
  - Ensures all columns are consistent across different CSV files.
  - Saves the combined data as `combined_prem_stats.csv`.

### 2. cleaning_data.py
- **Purpose**: Cleans and preprocesses the data to make it suitable for machine learning.
- **Output**: `matches.csv`
- **Key Steps**:
  - Removes unnecessary columns (e.g., betting odds).
  - Converts the match results to 'W', 'D', and 'L' for both home and away teams.
  - Rearranges and standardizes columns to ensure uniformity.
  - Swaps the columns appropriately for home and away teams.

### 3. ML_predictions.py
- **Purpose**: Uses a Random Forest model to predict match outcomes.
- **Key Steps**:
  - Converts categorical variables (e.g., team, venue) into numerical codes.
  - Trains a Random Forest classifier on historical match data.
  - Evaluates the model's accuracy and precision, using rolling averages of match statistics.

## Notes on Data Preparation
- Rolling averages are used to capture recent team performance, which is crucial for predicting future match outcomes.
- The data includes features such as `Venue_Code`, `Opp_Code`, `Hour`, and `Day_Code` to provide relevant context to the model.

## Observations and Improvements
- The current model's accuracy might be improved by including additional features, such as form over the last N matches, team strength, and player availability.
- Further feature engineering and hyperparameter tuning are recommended to optimize the model's predictive performance.

## How to Contribute
- Fork this repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes and commit them (`git commit -am 'Add new feature'`).
- Push to the branch (`git push origin feature-branch`).
- Create a new Pull Request.
