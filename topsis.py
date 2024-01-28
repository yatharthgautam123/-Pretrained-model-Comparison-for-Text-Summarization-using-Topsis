import pandas as pd
import numpy as np

def load_data(file_path):
    return pd.read_csv(file_path)

def normalize_matrix(matrix):
    normalized_matrix = matrix / np.max(matrix, axis=0)
    return normalized_matrix

def calculate_topsis_scores(normalized_matrix, weights):
    weighted_normalized_matrix = normalized_matrix * weights
    ideal_solution = np.max(weighted_normalized_matrix, axis=0)
    negative_ideal_solution = np.min(weighted_normalized_matrix, axis=0)
    distance_to_ideal = np.sqrt(np.sum((weighted_normalized_matrix - ideal_solution)**2, axis=1))
    distance_to_negative_ideal = np.sqrt(np.sum((weighted_normalized_matrix - negative_ideal_solution)**2, axis=1))
    topsis_scores = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)
    return topsis_scores

def rank_models(data, topsis_scores):
    data['TOPSIS_Score'] = topsis_scores
    data['Rank'] = data['TOPSIS_Score'].rank(ascending=False)
    return data[['Model', 'TOPSIS_Score', 'Rank']].sort_values(by='Rank')

def main():
    # Load data from the CSV file
    data = load_data('data.csv')

    # Extract relevant columns
    rouge_scores = data['Rouge_Scores'].values
    length_of_summary = data['Length_of_Summary'].values
    training_time = data['Training_Time'].values

    # Weights for each parameter
    weights = np.array([0.4, 0.3, 0.3])

    # Normalize the matrix
    normalized_matrix = normalize_matrix(np.column_stack([
        rouge_scores, 1 - (length_of_summary / np.max(length_of_summary)),
        1 - (training_time / np.max(training_time))
    ]))

    # Calculate the TOPSIS scores
    topsis_scores = calculate_topsis_scores(normalized_matrix, weights)

    # Rank the models based on TOPSIS scores
    result = rank_models(data, topsis_scores)

    # Print the results
    print("Model Ranking:")
    print(result)

    # Save results to CSV
    result.to_csv('result.csv', index=False)

if __name__ == "__main__":
    main()
