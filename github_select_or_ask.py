import pandas as pd

# File paths
final_results_path = "final_results.csv"
output_path = "query_type_bleu_summary.csv"

# Load the input data
final_results_df = pd.read_csv(final_results_path)

# Add a column for the query type (the first word of the Ground Truth Query)
final_results_df["Query Type"] = final_results_df["Ground Truth Query"].str.split().str[0]

# Filter the data for specific query types (SELECT or ASK)
filtered_data = final_results_df[
    final_results_df["Query Type"].str.upper().isin(["SELECT", "ASK"])
]

# Group the filtered data by "Query Type"
grouped_results = filtered_data.groupby("Query Type")

# Calculate BLEU score statistics and question count for each query type
summary = grouped_results["BLEU Score"].agg(
    Average_BLEU="mean",
    Median_BLEU="median",
    Question_Count="size"
).reset_index()

# Save the updated summary to a new CSV file
summary.to_csv(output_path, index=False)
