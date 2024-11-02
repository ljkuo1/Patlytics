from flask import Flask, request, make_response, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
from utils import embedding, format_claim_numbers, determine_infringement_likelihood, prepare_data_for_llm, save_report, get_saved_reports
from data_access import get_patent_by_id, get_company_by_name
from models import model
import os

app = Flask(__name__)
CORS(app)

def check_infringement(patent_id, company_name):
    patent = get_patent_by_id(patent_id)
    if not patent:
        return {"error": "Patent not found"}

    claims_data = json.loads(patent['claims'])

    company = get_company_by_name(company_name)
    if not company:
        return {"error": "Company not found"}

    infringing_products = []
    for product in company['products']:
        relevant_claims = []
        for claim in claims_data:
            if 'text' in claim and embedding(product['description'], claim['text'], model):
                relevant_claims.append(claim['num'])

        # If relevant claims are found, prepare the product data
        if relevant_claims:
            formatted_claims = format_claim_numbers(relevant_claims)

            # Prepare data for potential LLM integration (Now I don't have the api key)
            llm_input = prepare_data_for_llm(product['name'], product['description'], formatted_claims, claims_data)

            # Placeholder for LLM integration
            response = {
                "explanation": "Generated explanation based on LLM analysis.",
                "specific_features": ["Feature A", "Feature B", "Feature C"]
            }

            # Determine infringement likelihood based on the number of relevant claims
            infringement_likelihood = determine_infringement_likelihood(len(relevant_claims))

            infringing_products.append({
                "product_name": product['name'],
                "infringement_likelihood": infringement_likelihood,
                "relevant_claims": formatted_claims,
                "explanation": response['explanation'],
                "specific_features": response['specific_features']
            })

    # Sort products by the number of relevant claims and select the top ones
    infringing_products.sort(key=lambda x: len(x['relevant_claims']), reverse=True)
    top_infringing_products = infringing_products[:2]
    analysis_date = datetime.now().strftime("%Y-%m-%d")

    response = {
        "analysis_id": str(patent['id']),
        "patent_id": patent_id,
        "company_name": company['name'],
        "analysis_date": analysis_date,
        "top_infringing_products": top_infringing_products
    }

    # Save the report
    save_report(response)

    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


# Infringement check
@app.route('/api/check', methods=['POST'])
def infringement_check():
    data = request.json
    patent_id = data.get('patent_id')
    company_name = data.get('company_name')

    # Validate input data
    if not patent_id or not company_name:
        response = make_response(json.dumps({"error": "Patent ID and Company Name are required"}), 400)
        response.headers['Content-Type'] = 'application/json'
    else:
        # Perform infringement check and return the result
        result = check_infringement(patent_id, company_name)
        response = make_response(json.dumps(result))
        response.headers['Content-Type'] = 'application/json'

    return response

# View saved reports
@app.route('/api/reports', methods=['GET'])
def view_reports():
    try:
        reports = get_saved_reports()
        return make_response(json.dumps(reports), 200, {'Content-Type': 'application/json'})
    except Exception as e:
        return make_response(json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
