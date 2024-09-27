import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

# Read the file
matches = pd.read_csv("matches.csv")

# Remove non-numeric column that isn't used by classifier
del matches["Div"]

# Convert date to date-time value in pandas
matches["Date"] = pd.to_datetime(matches["Date"])

# Add column for target of classifier
matches["Target"] = (matches["FTR"] == "W").astype("int")

# Add Venue Code column to convert Home/Away to numeric values
matches["Venue_Code"] = matches["Venue"].astype("category").cat.codes

# Add Opponent Code column to convert Opposition to numeric values
matches["Opp_Code"] = matches["Opposition"].astype("category").cat.codes

# Add Hour column to convert hour of day to integer
matches["Hour"] = matches["Time"].str.replace(":.+", "", regex=True).astype("int")

# Add a code for the day of the week
matches["Day_Code"] = matches["Date"].dt.dayofweek

# Call the classifier
rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

# Divide the data into training and testing sets
train = matches[matches["Date"] < '2023-01-01']
test = matches[matches["Date"] > '2023-01-01']

# Choose initial predictors for results
predictors = ["Venue_Code", "Opp_Code", "Hour", "Day_Code"]

# Train a very simple random forest model with the predictors
rf.fit(train[predictors], train["Target"])

# Pass in test data to assess accuracy
preds = rf.predict(test[predictors])

# Calculate accuracy of model
error = accuracy_score(test["Target"], preds)

# Closer look at accuracy of model
combined = pd.DataFrame(dict(actual=test["Target"], predicted=preds))
crosstab = pd.crosstab(index=combined["actual"], columns=combined["predicted"])

# Precision of predictions
precision = precision_score(test["Target"], preds)

# Accuracy is poor, when predicting a win it is wrong most of the time
# Need additional predictors

# Create data frames for each team to be able to perform calculations for each team
grouped_matches = matches.groupby("Team")

# Retrieve the best team in the premier league's data frame
group = grouped_matches.get_group("Man United").sort_values("Date")

# Define a function to calculate the rolling averages of each of the teams
def rolling_averages(group, cols, new_cols):
    # Order results
    group = group.sort_values("Date")

    # Calculate rolling average
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    
    # Fill new columns
    group[new_cols] = rolling_stats

    # Drop empty cells
    group = group.dropna(subset=new_cols)

    return group

# Specify the columns where form may have an impact
cols = ["FTG", "FTGA", "HTG", "HTGA","S","SA","ST","STA","F","FA","C","CA","Y","YA","R","RA"]

# Specify that the new columns contain rolling values
new_cols = [f"{c}_Rolling" for c in cols]

# Loop through each team and return a df with function applied to each team
matches_rolling = matches.groupby("Team").apply(lambda x: rolling_averages(x, cols, new_cols))

# Drop the Team index
matches_rolling = matches_rolling.droplevel('Team')

# Reset the index of each fixture
matches_rolling.index = range(matches_rolling.shape[0])

# Function to aid in iterating on our algorithm
def make_predictions(data, predictors):

    # Split data
    train = data[data["Date"] < '2023-01-01']
    test = data[data["Date"] > '2023-01-01']

    # Create predictions
    rf.fit(train[predictors], train["Target"])
    preds = rf.predict(test[predictors])

    # Combine predicted and actual data
    combined = pd.DataFrame(dict(actual=test["Target"], predicted=preds), index=test.index)

    # Calculate precision
    precision = precision_score(test["Target"], preds)

    return combined, precision

# Run with new predictors
combined, precision = make_predictions(matches_rolling, predictors + new_cols)

# Matched each fixture using pandas so that can see both sides of the fixtures prediction
combined = combined.merge(matches_rolling[["Date", "Team", "Opposition", "FTR"]], left_index=True, right_index=True)
merged = combined.merge(combined, left_on=["Date", "Team"], right_on=["Date", "Opposition"])

# Times when both sides of prediction are in agreement
consistent = merged[(merged["predicted_x"] == 1) & (merged["predicted_y"] ==0)]["actual_x"].value_counts()

# Percentage of correct predictions when both sides of prediction in agreement
accuracy = consistent[1] / (consistent[0] + consistent[1])

print(accuracy)