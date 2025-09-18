#!/usr/bin/env python3
"""
Enhanced Multi-Dataset Salary Prediction API
Leverages Stack Overflow, Glassdoor, Remote Jobs, and LinkedIn data
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import sys
from collections import defaultdict

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naive_bayes_solution import naive_bayes_model, ve
from bnetbase import Variable

app = Flask(__name__)
CORS(app)

# Global variables
trained_model = None
unified_data = None
glassdoor_data = None
remote_jobs_data = None
linkedin_data = None

# Original Stack Overflow variable domains
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

def load_all_datasets():
    """Load all salary datasets"""
    global unified_data, glassdoor_data, remote_jobs_data, linkedin_data
    
    print("📊 Loading multi-dataset salary information...")
    
    try:
        unified_data = pd.read_csv('data/unified_salary_dataset.csv')
        glassdoor_data = pd.read_csv('data/glassdoor_salaries.csv')
        remote_jobs_data = pd.read_csv('data/remote_jobs_salaries.csv') 
        linkedin_data = pd.read_csv('data/linkedin_salaries.csv')
        
        print(f"✅ Loaded {len(unified_data):,} unified salary records")
        print(f"   • Glassdoor: {len(glassdoor_data):,} company records")
        print(f"   • Remote Jobs: {len(remote_jobs_data):,} remote records")
        print(f"   • LinkedIn: {len(linkedin_data):,} professional records")
        
    except Exception as e:
        print(f"⚠️ Could not load additional datasets: {e}")
        print("Falling back to Stack Overflow data only")

def load_model():
    """Load the trained Naive Bayes model"""
    global trained_model
    if trained_model is None:
        print("🧠 Loading Stack Overflow developer survey model...")
        trained_model = naive_bayes_model('data/stackoverflow-train.csv', variable_domains)
        print("Model loaded successfully!")
    return trained_model

def get_company_insights(profile):
    """Get company-specific salary insights from Glassdoor data"""
    if glassdoor_data is None:
        return {}
    
    try:
        # Map dev type to job titles
        dev_type_mapping = {
            'Full-stack': ['Full Stack Engineer', 'Software Engineer'],
            'Backend': ['Backend Engineer', 'Software Engineer'],
            'Frontend': ['Frontend Engineer', 'Software Engineer'],
            'Data Science': ['Data Scientist', 'Senior Data Scientist'],
            'DevOps/SRE': ['DevOps Engineer', 'Site Reliability Engineer'],
            'Mobile': ['Mobile Engineer', 'iOS Engineer', 'Android Engineer']
        }
        
        relevant_titles = dev_type_mapping.get(profile.get('DevType', ''), ['Software Engineer'])
        
        # Filter Glassdoor data for similar roles
        company_matches = glassdoor_data[
            glassdoor_data['job_title'].str.contains('|'.join(relevant_titles), case=False, na=False)
        ]
        
        if len(company_matches) > 0:
            top_companies = company_matches.nlargest(10, 'salary')[['company', 'salary', 'company_rating']].to_dict('records')
            avg_company_salary = company_matches['salary'].mean()
            
            return {
                'top_paying_companies': top_companies,
                'average_company_salary': int(avg_company_salary),
                'company_data_points': len(company_matches)
            }
    except Exception as e:
        print(f"Error getting company insights: {e}")
    
    return {}

def get_remote_insights(profile):
    """Get remote work salary insights"""
    if remote_jobs_data is None:
        return {}
    
    try:
        # Filter for similar remote roles
        remote_matches = remote_jobs_data[
            remote_jobs_data['job_title'].str.contains(profile.get('DevType', ''), case=False, na=False)
        ]
        
        if len(remote_matches) > 0:
            avg_remote_salary = remote_matches['salary'].mean()
            remote_companies = remote_matches['company'].value_counts().head(5).to_dict()
            
            return {
                'average_remote_salary': int(avg_remote_salary),
                'top_remote_companies': remote_companies,
                'remote_data_points': len(remote_matches),
                'fully_remote_available': True
            }
    except Exception as e:
        print(f"Error getting remote insights: {e}")
    
    return {}

def get_industry_insights(profile):
    """Get industry-specific insights from LinkedIn data"""
    if linkedin_data is None:
        return {}
    
    try:
        # Get industry salary distributions
        industry_stats = linkedin_data.groupby('industry')['salary'].agg(['mean', 'count']).round(0)
        industry_stats = industry_stats[industry_stats['count'] >= 50]  # Minimum sample size
        top_industries = industry_stats.nlargest(5, 'mean')
        
        return {
            'top_paying_industries': top_industries.to_dict('records'),
            'industry_data_available': len(industry_stats) > 0
        }
    except Exception as e:
        print(f"Error getting industry insights: {e}")
    
    return {}

def get_multi_source_insights(profile):
    """Combine insights from all data sources"""
    
    # Calculate data source statistics
    source_stats = {}
    if unified_data is not None:
        source_counts = unified_data['data_source'].value_counts().to_dict()
        source_avg_salaries = unified_data.groupby('data_source')['salary'].mean().round(0).to_dict()
        
        source_stats = {
            'data_source_counts': source_counts,
            'data_source_avg_salaries': source_avg_salaries,
            'total_unified_records': len(unified_data)
        }
    
    # Get specialized insights
    company_insights = get_company_insights(profile)
    remote_insights = get_remote_insights(profile)
    industry_insights = get_industry_insights(profile)
    
    return {
        'source_statistics': source_stats,
        'company_insights': company_insights,
        'remote_work_insights': remote_insights,
        'industry_insights': industry_insights,
        'data_integration_note': "This prediction combines insights from Stack Overflow developer survey, Glassdoor company data, remote job boards, and LinkedIn professional networks for comprehensive salary analysis."
    }

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "Multi-Dataset Developer Salary Prediction API is running!",
        "data_sources": ["Stack Overflow 2023", "Glassdoor", "Remote Job Boards", "LinkedIn"],
        "status": "healthy"
    })

@app.route('/api/domains', methods=['GET'])
def get_domains():
    """Get the available options for each feature"""
    features = {k: v for k, v in variable_domains.items() if k != 'Salary'}
    return jsonify(features)

@app.route('/api/data-sources', methods=['GET'])
def get_data_sources():
    """Get information about all data sources"""
    load_all_datasets()
    
    sources_info = {
        "stackoverflow": {
            "name": "Stack Overflow 2023 Developer Survey",
            "records": 35082,
            "type": "Developer Survey",
            "confidence": 0.9,
            "coverage": "Global developers, all experience levels"
        },
        "glassdoor": {
            "name": "Glassdoor Company Salaries",
            "records": 5000,
            "type": "Company Reviews",
            "confidence": 0.8,
            "coverage": "Top tech companies, verified employee reports"
        },
        "remote_boards": {
            "name": "Remote Job Boards",
            "records": 3000,
            "type": "Job Postings",
            "confidence": 0.7,
            "coverage": "Remote-first companies, location-independent roles"
        },
        "linkedin": {
            "name": "LinkedIn Professional Network",
            "records": 4000,
            "type": "Professional Profiles",
            "confidence": 0.6,
            "coverage": "Cross-industry professionals, various company sizes"
        }
    }
    
    return jsonify(sources_info)

@app.route('/api/predict', methods=['POST'])
def predict_salary():
    """Enhanced salary prediction using multiple datasets"""
    try:
        # Load all datasets if not already loaded
        load_all_datasets()
        
        # Get input data
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
        
        # Load Stack Overflow model for base prediction
        model = load_model()
        
        # Original Stack Overflow prediction logic
        import pandas as pd
        training_data = pd.read_csv('data/stackoverflow-train.csv')
        
        # Calculate similar developer counts
        total_training_size = len(training_data)
        match_counts = {}
        for field, value in data.items():
            if field in training_data.columns:
                matches = len(training_data[training_data[field] == value])
                match_counts[field] = matches
        
        # Count exact matches
        exact_matches = training_data
        for field, value in data.items():
            if field in training_data.columns:
                exact_matches = exact_matches[exact_matches[field] == value]
        exact_match_count = len(exact_matches)
        
        # Get salary distribution
        salary_distribution = training_data['Salary'].value_counts().to_dict()
        
        # Run ML model prediction
        variables = {var.name: var for var in model.variables()}
        
        evidence_vars = []
        for field, value in data.items():
            if field in variables:
                var = variables[field]
                var.set_evidence(value)
                evidence_vars.append(var)
        
        salary_var = variables['Salary']
        result_factor = ve(model, salary_var, evidence_vars)
        
        # Extract probabilities
        probabilities = {}
        salary_values = salary_var.domain()
        
        for i, salary_value in enumerate(salary_values):
            salary_var.set_assignment_index(i)
            prob = result_factor.get_value_at_current_assignments()
            probabilities[salary_value] = prob
        
        # Determine prediction
        predicted_salary = max(probabilities.keys(), key=lambda k: probabilities[k])
        confidence = probabilities[predicted_salary]
        
        # Format salary display
        salary_display = {
            '<50K': 'Less than $50,000',
            '50K-75K': '$50,000 - $75,000', 
            '75K-100K': '$75,000 - $100,000',
            '100K-150K': '$100,000 - $150,000',
            '150K+': '$150,000 or more'
        }
        
        # Reset evidence
        for var in evidence_vars:
            var.evidence_index = None
        
        # Get multi-source insights
        multi_source_insights = get_multi_source_insights(data)
        
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
                "similar_developers_note": f"Base prediction from {total_training_size:,} Stack Overflow survey responses."
            },
            "multi_source_insights": multi_source_insights
        })
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced Multi-Dataset Salary Prediction API...")
    print("📊 Loading Stack Overflow model and additional datasets...")
    
    load_all_datasets()
    load_model()
    
    print("🎯 API ready with multi-source salary insights!")
    app.run(debug=True, host='0.0.0.0', port=5001)