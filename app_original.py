from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add current directory to Python path to import our ML modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naive_bayes_solution import naive_bayes_model, ve
from bnetbase import Variable

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to store the trained model
trained_model = None
variable_domains = {
    "Age": ['Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
    "Education": ['High School or Less', 'Some College', 'Associate', 'Professional/PhD', 'Other'],
    "Employment": ['Full-time', 'Part-time', 'Contractor/Freelance'],
    "RemoteWork": ['In-person', 'Hybrid'],
    "Experience": ['<1 year', '1-2 years', '3-5 years', '6-10 years', '11-15 years', '15+ years'],
    "DevType": ['Full-stack', 'Backend', 'Frontend', 'Mobile', 'Data Science', 'DevOps/SRE', 'Other'],
    "CompanySize": ['Small (1-9)', 'Medium (10-19)', 'Medium (20-99)', 'Large (100-499)', 'Large (500-999)', 'Enterprise (1K-5K)', 'Enterprise (5K+)'],
    "Country": ['United States', 'Germany', 'United Kingdom', 'India', 'Canada', 'France', 'Netherlands', 'Australia', 'Brazil', 'Poland', 'Other'],
    "Salary": ['<50K', '50K-75K', '75K-100K', '100K-150K', '150K+']
}

def load_model():
    """Load the trained Naive Bayes model"""
    global trained_model
    if trained_model is None:
        print("Loading Stack Overflow developer survey model...")
        trained_model = naive_bayes_model('data/stackoverflow-train.csv', variable_domains)
        print("Model loaded successfully!")
    return trained_model

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "Salary Prediction API is running!",
        "status": "healthy"
    })

@app.route('/api/domains', methods=['GET'])
def get_domains():
    """Get the available options for each feature"""
    # Exclude 'Salary' from the domains since that's what we're predicting
    features = {k: v for k, v in variable_domains.items() if k != 'Salary'}
    return jsonify(features)

@app.route('/api/predict', methods=['POST'])
def predict_salary():
    """Predict salary based on input features"""
    try:
        # Get input data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['Age', 'Education', 'Employment', 'RemoteWork', 
                          'Experience', 'DevType', 'CompanySize', 'Country']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Validate field values
        for field, value in data.items():
            if field in variable_domains and value not in variable_domains[field]:
                return jsonify({"error": f"Invalid value '{value}' for field '{field}'. Valid values: {variable_domains[field]}"}), 400
        
        # Load model if not loaded
        model = load_model()
        
        # Calculate similar developer counts for transparency
        import pandas as pd
        training_data = pd.read_csv('data/stackoverflow-train.csv')
        
        # Count developers with similar characteristics
        similar_devs = training_data.copy()
        total_training_size = len(training_data)
        
        # Filter by each input characteristic and count matches
        match_counts = {}
        for field, value in data.items():
            if field in training_data.columns:
                matches = len(training_data[training_data[field] == value])
                match_counts[field] = matches
        
        # Count developers with exact same profile (all features match)
        exact_matches = training_data
        for field, value in data.items():
            if field in training_data.columns:
                exact_matches = exact_matches[exact_matches[field] == value]
        exact_match_count = len(exact_matches)
        
        # Count developers in each salary bracket for context
        salary_distribution = training_data['Salary'].value_counts().to_dict()
        
        # Create variable dictionary for the model
        variables = {var.name: var for var in model.variables()}
        
        # Set evidence for all input variables
        evidence_vars = []
        for field, value in data.items():
            if field in variables:
                var = variables[field]
                var.set_evidence(value)
                evidence_vars.append(var)
        
        # Query the salary variable
        salary_var = variables['Salary']
        
        # Perform variable elimination to get probability distribution
        result_factor = ve(model, salary_var, evidence_vars)
        
        # Extract probabilities
        probabilities = {}
        salary_values = salary_var.domain()
        
        for i, salary_value in enumerate(salary_values):
            # Get probability for this salary value
            salary_var.set_assignment_index(i)
            prob = result_factor.get_value_at_current_assignments()
            probabilities[salary_value] = prob
        
        # Determine prediction (highest probability)
        predicted_salary = max(probabilities.keys(), key=lambda k: probabilities[k])
        confidence = probabilities[predicted_salary]
        
        # Format salary range for display
        salary_display = {
            '<50K': 'Less than $50,000',
            '50K-75K': '$50,000 - $75,000', 
            '75K-100K': '$75,000 - $100,000',
            '100K-150K': '$100,000 - $150,000',
            '150K+': '$150,000 or more'
        }
        
        # Reset evidence for all variables
        for var in evidence_vars:
            var.evidence_index = None
        
        return jsonify({
            "prediction": predicted_salary,
            "prediction_display": salary_display.get(predicted_salary, predicted_salary),
            "confidence": confidence,
            "probabilities": probabilities,
            "input_data": data,
            "data_insights": {
                "total_training_samples": total_training_size,
                "exact_profile_matches": exact_match_count,
                "feature_matches": match_counts,
                "salary_distribution": salary_distribution,
                "similar_developers_note": f"This prediction is based on analyzing patterns from {total_training_size:,} real developer profiles from Stack Overflow's 2023 survey."
            }
        })
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Developer Salary Prediction API...")
    print("Loading Stack Overflow developer survey model on startup...")
    load_model()
    print("API ready!")
    app.run(debug=True, host='0.0.0.0', port=5001)