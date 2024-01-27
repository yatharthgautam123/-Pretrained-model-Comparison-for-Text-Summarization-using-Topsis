import pandas as pd
import numpy as np

# Load data from the CSV file
data = pd.read_csv('data.csv')

# Extract relevant columns
rouge_scores = data['Rouge_Scores'].values
length_of_summary = data['Length_of_Summary'].values
training_time = data['Training_Time'].values

# Weights for each parameter
weights = np.array([0.4, 0.3, 0.3])

# Normalize the matrix
normalized_matrix = np.column_stack([
    rouge_scores / np.max(rouge_scores),
    1 - (length_of_summary / np.max(length_of_summary)),
    1 - (training_time / np.max(training_time))
])

# Calculate the weighted normalized decision matrix
weighted_normalized_matrix = normalized_matrix * weights

# Ideal and Negative Ideal solutions
ideal_solution = np.max(weighted_normalized_matrix, axis=0)
negative_ideal_solution = np.min(weighted_normalized_matrix, axis=0)

# Calculate the separation measures
distance_to_ideal = np.sqrt(np.sum((weighted_normalized_matrix - ideal_solution)**2, axis=1))
distance_to_negative_ideal = np.sqrt(np.sum((weighted_normalized_matrix - negative_ideal_solution)**2, axis=1))

# Calculate the TOPSIS scores
topsis_scores = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)

# Rank the models based on TOPSIS scores
data['TOPSIS_Score'] = topsis_scores
data['Rank'] = data['TOPSIS_Score'].rank(ascending=False)

# Print the results
print("Model Ranking:")
print(data[['Model', 'TOPSIS_Score', 'Rank']].sort_values(by='Rank'))

data.to_csv('result.csv', index=False)
