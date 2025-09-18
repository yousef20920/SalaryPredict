#!/usr/bin/env python3
"""
Stack Overflow 2023 Developer Survey Data Preprocessing Script
Converts raw survey data into clean format for ML model training
"""

import pandas as pd
import numpy as np
import sys
from typing import Dict, List, Tuple

def clean_salary_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and categorize salary data"""
    print("Cleaning salary data...")
    
    # Filter for responses with salary data
    df_salary = df[df['ConvertedCompYearly'].notna()].copy()
    print(f"Records with salary data: {len(df_salary)}")
    
    # Convert to numeric and filter realistic salaries (10k-500k USD)
    df_salary['ConvertedCompYearly'] = pd.to_numeric(df_salary['ConvertedCompYearly'], errors='coerce')
    df_salary = df_salary[
        (df_salary['ConvertedCompYearly'] >= 10000) & 
        (df_salary['ConvertedCompYearly'] <= 500000)
    ].copy()
    print(f"Records with realistic salaries: {len(df_salary)}")
    
    # Create salary brackets
    def categorize_salary(salary):
        if salary < 50000:
            return "<50K"
        elif salary < 75000:
            return "50K-75K"
        elif salary < 100000:
            return "75K-100K"
        elif salary < 150000:
            return "100K-150K"
        else:
            return "150K+"
    
    df_salary['SalaryBracket'] = df_salary['ConvertedCompYearly'].apply(categorize_salary)
    return df_salary

def clean_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize categorical features"""
    print("Cleaning categorical features...")
    
    # Age mapping
    age_mapping = {
        'Under 18 years old': 'Under 18',
        '18-24 years old': '18-24',
        '25-34 years old': '25-34', 
        '35-44 years old': '35-44',
        '45-54 years old': '45-54',
        '55-64 years old': '55-64',
        '65 years or older': '65+',
        'Prefer not to say': 'Unknown'
    }
    df['Age_Clean'] = df['Age'].map(age_mapping).fillna('Unknown')
    
    # Education level mapping
    edu_mapping = {
        'Primary/elementary school': 'High School or Less',
        'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 'High School or Less',
        'Some college/university study without earning a degree': 'Some College',
        'Associate degree (A.A., A.S., etc.)': 'Associate',
        "Bachelor's degree (B.A., B.S., B.Eng., etc.)": 'Bachelor',
        "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": 'Master',
        'Professional degree (JD, MD, Ph.D, Ed.D, etc.)': 'Professional/PhD',
        'Something else': 'Other'
    }
    df['Education_Clean'] = df['EdLevel'].map(edu_mapping).fillna('Other')
    
    # Employment type
    def clean_employment(emp_str):
        if pd.isna(emp_str):
            return 'Unknown'
        if 'full-time' in str(emp_str).lower():
            return 'Full-time'
        elif 'part-time' in str(emp_str).lower():
            return 'Part-time'
        elif 'contractor' in str(emp_str).lower() or 'freelance' in str(emp_str).lower():
            return 'Contractor/Freelance'
        elif 'student' in str(emp_str).lower():
            return 'Student'
        else:
            return 'Other'
    
    df['Employment_Clean'] = df['Employment'].apply(clean_employment)
    
    # Remote work
    def clean_remote(remote_str):
        if pd.isna(remote_str):
            return 'Unknown'
        remote_lower = str(remote_str).lower()
        if 'fully remote' in remote_lower:
            return 'Fully Remote'
        elif 'hybrid' in remote_lower:
            return 'Hybrid'
        else:
            return 'In-person'
    
    df['RemoteWork_Clean'] = df['RemoteWork'].apply(clean_remote)
    
    # Years of experience
    def clean_years_code(years_str):
        if pd.isna(years_str):
            return 'Unknown'
        years_str = str(years_str).lower()
        if 'less than 1 year' in years_str or years_str == '0':
            return '<1 year'
        elif years_str in ['1', '2']:
            return '1-2 years'
        elif years_str in ['3', '4', '5']:
            return '3-5 years'
        elif years_str in ['6', '7', '8', '9', '10']:
            return '6-10 years'
        elif years_str in ['11', '12', '13', '14', '15']:
            return '11-15 years'
        else:
            return '15+ years'
    
    df['YearsCode_Clean'] = df['YearsCode'].apply(clean_years_code)
    
    # Developer type (simplified)
    def clean_dev_type(dev_type_str):
        if pd.isna(dev_type_str):
            return 'Unknown'
        
        dev_type_lower = str(dev_type_str).lower()
        if 'full-stack' in dev_type_lower:
            return 'Full-stack'
        elif 'back-end' in dev_type_lower:
            return 'Backend'
        elif 'front-end' in dev_type_lower:
            return 'Frontend'
        elif 'mobile' in dev_type_lower:
            return 'Mobile'
        elif 'data scientist' in dev_type_lower or 'data' in dev_type_lower:
            return 'Data Science'
        elif 'devops' in dev_type_lower or 'sre' in dev_type_lower:
            return 'DevOps/SRE'
        else:
            return 'Other'
    
    df['DevType_Clean'] = df['DevType'].apply(clean_dev_type)
    
    # Organization size
    def clean_org_size(org_str):
        if pd.isna(org_str):
            return 'Unknown'
        org_lower = str(org_str).lower()
        if 'just me' in org_lower or '2 to 9' in org_lower:
            return 'Small (1-9)'
        elif '10 to 19' in org_lower:
            return 'Medium (10-19)'
        elif '20 to 99' in org_lower:
            return 'Medium (20-99)'
        elif '100 to 499' in org_lower:
            return 'Large (100-499)'
        elif '500 to 999' in org_lower:
            return 'Large (500-999)'
        elif '1,000 to 4,999' in org_lower:
            return 'Enterprise (1K-5K)'
        elif '5,000 to 9,999' in org_lower or '10,000 or more' in org_lower:
            return 'Enterprise (5K+)'
        else:
            return 'Unknown'
    
    df['OrgSize_Clean'] = df['OrgSize'].apply(clean_org_size)
    
    # Country (top countries + others)
    top_countries = ['United States of America', 'Germany', 'United Kingdom of Great Britain and Northern Ireland', 
                    'India', 'Canada', 'France', 'Netherlands', 'Australia', 'Brazil', 'Poland']
    
    def clean_country(country_str):
        if pd.isna(country_str):
            return 'Other'
        if country_str in top_countries:
            return country_str.replace('United States of America', 'United States') \
                             .replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom')
        else:
            return 'Other'
    
    df['Country_Clean'] = df['Country'].apply(clean_country)
    
    return df

def create_training_data(df: pd.DataFrame) -> pd.DataFrame:
    """Create final training dataset with selected features"""
    print("Creating training dataset...")
    
    # Select features for ML model
    features = [
        'Age_Clean', 'Education_Clean', 'Employment_Clean', 'RemoteWork_Clean',
        'YearsCode_Clean', 'DevType_Clean', 'OrgSize_Clean', 'Country_Clean', 'SalaryBracket'
    ]
    
    # Create clean dataset
    ml_data = df[features].copy()
    
    # Remove rows with 'Unknown' values (except for target variable)
    for col in features[:-1]:  # Exclude target variable
        ml_data = ml_data[ml_data[col] != 'Unknown']
    
    # Rename columns to match our existing format
    ml_data.columns = [
        'Age', 'Education', 'Employment', 'RemoteWork', 
        'Experience', 'DevType', 'CompanySize', 'Country', 'Salary'
    ]
    
    print(f"Final dataset size: {len(ml_data)} records")
    print(f"Salary distribution:")
    print(ml_data['Salary'].value_counts())
    
    return ml_data

def main():
    """Main preprocessing pipeline"""
    print("=== Stack Overflow 2023 Survey Data Preprocessing ===")
    
    # Load raw data
    print("Loading raw survey data...")
    df = pd.read_csv('data/survey_results_public.csv')
    print(f"Total survey responses: {len(df)}")
    
    # Clean salary data
    df_clean = clean_salary_data(df)
    
    # Clean categorical features
    df_clean = clean_categorical_features(df_clean)
    
    # Create training data
    training_data = create_training_data(df_clean)
    
    # Split into train/test (80/20)
    train_size = int(0.8 * len(training_data))
    training_data_shuffled = training_data.sample(frac=1, random_state=42).reset_index(drop=True)
    
    train_data = training_data_shuffled[:train_size]
    test_data = training_data_shuffled[train_size:]
    
    # Save processed data
    train_data.to_csv('data/stackoverflow-train.csv', index=False)
    test_data.to_csv('data/stackoverflow-test.csv', index=False)
    
    print(f"\n=== Processing Complete ===")
    print(f"Training data: {len(train_data)} records -> data/stackoverflow-train.csv")
    print(f"Test data: {len(test_data)} records -> data/stackoverflow-test.csv")
    
    # Show sample data
    print(f"\nSample training data:")
    print(train_data.head())
    
    print(f"\nFeature distributions:")
    for col in train_data.columns[:-1]:
        print(f"\n{col}:")
        print(train_data[col].value_counts().head())

if __name__ == "__main__":
    main()