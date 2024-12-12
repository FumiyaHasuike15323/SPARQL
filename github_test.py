import csv
import json
from nltk.translate.bleu_score import sentence_bleu

# File paths
csv_file_path = "query_results.csv"  # CSV containing generated queries
json_file_path = "test_data.json"    # JSON containing ground truth queries
output_csv_path = "scraping_results.csv"  # CSV to save evaluation results

# Load generated questions and queries from a CSV file
def load_generated_queries(csv_path):
    generated_queries = {}
    with open(csv_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header
        for row in reader:
            if len(row) >= 2:  # Ensure the row has sufficient data
                question = row[0].strip()  # Extract the question text
                query = row[1].strip()     # Extract the generated SPARQL query
                generated_queries[question] = query
    return generated_queries

# Load ground truth queries and questions from a JSON file
def load_ground_truth_data(json_path):
    ground_truth_queries = {}
    with open(json_path, mode='r') as json_file:
        data = json.load(json_file)
        for item in data:
            question_text = item["corrected_question"].strip()
            sparql_query = item["sparql_query"].strip()
            ground_truth_queries[question_text] = sparql_query
    return ground_truth_queries

# Evaluation function
def evaluate_queries(generated_queries, ground_truth_queries):
    evaluation_results = []
    for question_text, generated_query in generated_queries.items():
        ground_truth_query = ground_truth_queries.get(question_text, "")
        # Calculate BLEU score
        bleu_score = sentence_bleu([ground_truth_query.split()], generated_query.split())
        # Check for exact match
        exact_match = int(generated_query == ground_truth_query)
        # Record results
        evaluation_results.append({
            "Question Text": question_text,
            "Generated Query": generated_query,
            "Ground Truth Query": ground_truth_query,
            "BLEU Score": bleu_score,
            "Exact Match": exact_match
        })
    return evaluation_results

# Save evaluation results to a CSV file
def save_evaluation_results_to_csv(results, output_path):
    with open(output_path, mode='w', newline='') as csv_file:
        fieldnames = [
            "Question Text", "Generated Query", 
            "Ground Truth Query", "BLEU Score", "Exact Match"
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

# Main process
if __name__ == "__main__":
    # Load queries
    generated_queries = load_generated_queries(csv_file_path)
    ground_truth_queries = load_ground_truth_data(json_file_path)

    # Evaluate
    evaluation_results = evaluate_queries(generated_queries, ground_truth_queries)

    # Save evaluation results to CSV
    save_evaluation_results_to_csv(evaluation_results, output_csv_path)

    # Display summary information
    avg_bleu = sum(res["BLEU Score"] for res in evaluation_results) / len(evaluation_results)
    exact_match_rate = sum(res["Exact Match"] for res in evaluation_results) / len(evaluation_results)
    print(f"Average BLEU Score: {avg_bleu:.4f}")
    print(f"Exact Match Rate: {exact_match_rate:.2%}")
    print(f"Results saved to {output_csv_path}")
