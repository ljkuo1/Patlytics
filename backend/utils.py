from sentence_transformers import util
import json
import os
from datetime import datetime

# Calculate the cosine similarity between the description and claim text embeddings
# Returns True if similarity exceeds the threshold

def embedding(description, claim_text, model):
    description_embedding = model.encode(description, convert_to_tensor=True)
    claim_embedding = model.encode(claim_text, convert_to_tensor=True)
    cosine_similarity = util.pytorch_cos_sim(description_embedding, claim_embedding).item()
    similarity_threshold = 0.55
    return cosine_similarity > similarity_threshold

def format_claim_numbers(claim_numbers):
    return [str(int(claim_num)) for claim_num in claim_numbers]


# Prepare data for potential LLM integration (Now I don't have the api key)
def prepare_data_for_llm(product_name, product_description, relevant_claims, claims_data):
    claims_texts = [claim['text'] for claim in claims_data if claim['num'] in relevant_claims]
    llm_input = {
        "product_name": product_name,
        "product_description": product_description,
        "relevant_claims": claims_texts
    }
    return llm_input

# Determine the likelihood of infringement based on the number of relevant claims
def determine_infringement_likelihood(claim_count):
    if claim_count <= 2:
        return "Low"
    elif claim_count <= 5:
        return "Medium"
    else:
        return "High"

# Once the results are generated, users will have the option to save the results as a
# report and later return to the app to view all previously saved reports

def save_report(report):
    # Define the directory for storing reports
    reports_dir = 'reports'

    # Create the directory if it doesn't exist
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Generate a unique filename using a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"report_{timestamp}.json"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(report, f, indent=4)

def get_saved_reports():
    reports_dir = 'reports'
    reports = []

    if os.path.exists(reports_dir):
        for filename in os.listdir(reports_dir):
            filepath = os.path.join(reports_dir, filename)
            # Read each JSON file and append its content to the reports list
            with open(filepath, 'r') as f:
                report = json.load(f)
                reports.append(report)

    return reports
