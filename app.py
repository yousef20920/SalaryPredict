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
    "Work": ['Not Working', 'Government', 'Private', 'Self-emp'],
    "Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional', 'Bachelors', 'Masters', 'Doctorate'],
    "Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour', 'Service', 'Professional'],
    "MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'],
    "Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
    "Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'],
    "Gender": ['Male', 'Female'],
    "Country": ['North-America', 'South-America', 'Europe', 'Asia', 'Middle-East', 'Carribean'],
    "Salary": ['<50K', '>=50K']
}

def load_model():
    """Load the trained Naive Bayes model"""
    global trained_model
    if trained_model is None:
        print("Loading model...")
        trained_model = naive_bayes_model('data/adult-train.csv', variable_domains)
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
        required_fields = ['Work', 'Education', 'Occupation', 'MaritalStatus', 
                          'Relationship', 'Race', 'Gender', 'Country']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Validate field values
        for field, value in data.items():
            if field in variable_domains and value not in variable_domains[field]:
                return jsonify({"error": f"Invalid value '{value}' for field '{field}'. Valid values: {variable_domains[field]}"}), 400
        
        # Load model if not loaded
        model = load_model()
        
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
        
        # Reset evidence for all variables
        for var in evidence_vars:
            var.evidence_index = None
        
        return jsonify({
            "prediction": predicted_salary,
            "confidence": confidence,
            "probabilities": probabilities,
            "input_data": data
        })
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Salary Prediction API...")
    print("Loading model on startup...")
    load_model()
    print("API ready!")
    app.run(debug=True, host='0.0.0.0', port=5000)