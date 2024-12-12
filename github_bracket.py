import pandas as pd

# File paths
final_results_path = "final_results.csv"
output_path = "bleu_score_by_brackets_count.csv"

# Load the input data
final_results_df = pd.read_csv(final_results_path)

# Add a column for the count of '<>' occurrences in the Ground Truth Query
final_results_df["Brackets Count"] = final_results_df["Ground Truth Query"].str.count("<.*?>")

# Group the data by "Brackets Count"
grouped_results = final_results_df.groupby("Brackets Count")

# Calculate BLEU score statistics and question count for each group
summary = grouped_results["BLEU Score"].agg(
    Average_BLEU="mean",
    Median_BLEU="median",
    Question_Count="size"
).reset_index()

# Save the updated summary to a new CSV file
summary.to_csv(output_path, index=False)
