import pandas as pd

# File paths
final_results_path = "final_results.csv"
output_path = "question_word_bleu_summary.csv"

# Load the input data
final_results_df = pd.read_csv(final_results_path)

# Add a column for the question word (the first word of the Question Text)
final_results_df["Question Word"] = final_results_df["Question Text"].str.split().str[0]

# Filter the data for specific question words (case insensitive)
filtered_data = final_results_df[
    final_results_df["Question Word"].str.lower().isin(["what", "who", "where", "how", "does", "is", "did", "was"])
]

# Convert "Question Word" to uppercase for consistency
filtered_data["Question Word"] = filtered_data["Question Word"].str.upper()

# Group the filtered data by "Question Word" (now in uppercase)
grouped_results = filtered_data.groupby("Question Word")

# Calculate BLEU score statistics and question count for each question word
summary = grouped_results["BLEU Score"].agg(
    Average_BLEU="mean",
    Median_BLEU="median",
    Question_Count="size"
).reset_index()

# Save the updated summary to a new CSV file
summary.to_csv(output_path, index=False)
