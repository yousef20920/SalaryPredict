#!/usr/bin/env python3
"""
Example: Simple Rule-Based Salary Prediction (No ML)
This shows what a non-ML approach would look like
"""

def predict_salary_simple_rules(profile):
    """
    Simple rule-based salary prediction - no machine learning
    Just hardcoded if-else statements
    """
    
    # Start with base salary
    salary = 50000
    
    # Simple rules based on obvious patterns
    if profile['Country'] == 'United States':
        salary += 20000
    elif profile['Country'] in ['Germany', 'United Kingdom']:
        salary += 10000
    
    # Experience multiplier
    if profile['Experience'] == '15+ years':
        salary *= 1.5
    elif profile['Experience'] in ['11-15 years', '6-10 years']:
        salary *= 1.2
    elif profile['Experience'] in ['3-5 years']:
        salary *= 1.0
    else:
        salary *= 0.8
    
    # Company size bonus
    if 'Enterprise' in profile['CompanySize']:
        salary += 15000
    elif 'Large' in profile['CompanySize']:
        salary += 10000
    
    # Dev type adjustments
    if profile['DevType'] == 'Data Science':
        salary += 20000
    elif profile['DevType'] == 'DevOps/SRE':
        salary += 15000
    elif profile['DevType'] == 'Full-stack':
        salary += 5000
    
    # Convert to salary bracket
    if salary < 50000:
        return '<50K'
    elif salary < 75000:
        return '50K-75K'
    elif salary < 100000:
        return '75K-100K'
    elif salary < 150000:
        return '100K-150K'
    else:
        return '150K+'

# Test the simple approach
test_profile = {
    'Age': '25-34',
    'Education': 'Other',
    'Employment': 'Full-time',
    'RemoteWork': 'Hybrid',
    'Experience': '6-10 years',
    'DevType': 'Full-stack',
    'CompanySize': 'Large (100-499)',
    'Country': 'United States'
}

simple_prediction = predict_salary_simple_rules(test_profile)
print(f"Simple Script Prediction: {simple_prediction}")
print("\nPROBLEMS with this approach:")
print("❌ No confidence scores")
print("❌ No probability distributions") 
print("❌ Rules are just my guesses")
print("❌ Doesn't learn from real data")
print("❌ Can't handle complex interactions")
print("❌ No way to validate accuracy")