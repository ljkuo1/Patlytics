import json
from fuzzywuzzy import fuzz

# Load data from JSON files
try:
    with open('./json_files/patents.json', 'r') as f:
        patents_data = json.load(f)

    with open('./json_files/company_products.json', 'r') as f:
        company_products_data = json.load(f)
except Exception as e:
    print(f"Error loading data files: {e}")
    exit(1)

def get_patent_by_id(patent_id):
    return next((p for p in patents_data if p['publication_number'] == patent_id), None)


# Allow basic user input parsing so you can do some fuzzy match with the given dataset
def get_company_by_name(company_name):
    threshold = 60
    best_match = None
    highest_score = 0

    for company in company_products_data['companies']:
        score = fuzz.token_set_ratio(company['name'].lower(), company_name.lower())

        if score > highest_score and score >= threshold:
            highest_score = score
            best_match = company

    return best_match
