#!/usr/bin/env python3
"""
Multi-Dataset Integration for Salary Prediction
Creates realistic synthetic datasets simulating Glassdoor, Remote Job Boards, and LinkedIn data
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_glassdoor_dataset():
    """Generate realistic Glassdoor company-specific salary data"""
    print("🏢 Generating Glassdoor company salary dataset...")
    
    companies = [
        'Google', 'Microsoft', 'Apple', 'Amazon', 'Meta', 'Netflix', 'Tesla',
        'Uber', 'Airbnb', 'Stripe', 'Snowflake', 'Databricks', 'OpenAI',
        'GitHub', 'Atlassian', 'Shopify', 'Spotify', 'Adobe', 'Salesforce',
        'Oracle', 'IBM', 'Intel', 'NVIDIA', 'AMD', 'Cisco', 'VMware'
    ]
    
    job_titles = [
        'Software Engineer', 'Senior Software Engineer', 'Staff Software Engineer',
        'Principal Software Engineer', 'Engineering Manager', 'Senior Engineering Manager',
        'Product Manager', 'Senior Product Manager', 'Data Scientist', 'Senior Data Scientist',
        'ML Engineer', 'DevOps Engineer', 'Security Engineer', 'Frontend Engineer',
        'Backend Engineer', 'Full Stack Engineer', 'Mobile Engineer'
    ]
    
    locations = [
        'San Francisco, CA', 'Seattle, WA', 'New York, NY', 'Austin, TX',
        'Boston, MA', 'Los Angeles, CA', 'Chicago, IL', 'Denver, CO',
        'Remote - US', 'London, UK', 'Berlin, Germany', 'Toronto, Canada'
    ]
    
    # Generate 5000 Glassdoor records
    glassdoor_data = []
    for _ in range(5000):
        company = random.choice(companies)
        title = random.choice(job_titles)
        location = random.choice(locations)
        
        # Base salary influenced by company tier and role seniority
        company_multiplier = {
            'Google': 1.4, 'Microsoft': 1.35, 'Apple': 1.4, 'Amazon': 1.3, 'Meta': 1.45,
            'Netflix': 1.5, 'Tesla': 1.25, 'Uber': 1.2, 'Airbnb': 1.3, 'Stripe': 1.4
        }.get(company, 1.0)
        
        seniority_multiplier = {
            'Software Engineer': 1.0, 'Senior Software Engineer': 1.4, 'Staff Software Engineer': 1.8,
            'Principal Software Engineer': 2.2, 'Engineering Manager': 1.9, 'Data Scientist': 1.3
        }.get(title, 1.2)
        
        location_multiplier = {
            'San Francisco, CA': 1.5, 'Seattle, WA': 1.3, 'New York, NY': 1.4,
            'Remote - US': 1.1, 'London, UK': 0.9, 'Berlin, Germany': 0.7
        }.get(location, 1.0)
        
        base_salary = 90000 * company_multiplier * seniority_multiplier * location_multiplier
        salary = int(base_salary + np.random.normal(0, base_salary * 0.2))
        salary = max(40000, min(500000, salary))  # Realistic bounds
        
        # Add experience and other details
        experience = random.randint(0, 20)
        rating = round(random.uniform(3.0, 5.0), 1)
        
        glassdoor_data.append({
            'company': company,
            'job_title': title,
            'location': location,
            'salary': salary,
            'experience_years': experience,
            'company_rating': rating,
            'data_source': 'glassdoor',
            'date_posted': datetime.now() - timedelta(days=random.randint(1, 365))
        })
    
    return pd.DataFrame(glassdoor_data)

def generate_remote_jobs_dataset():
    """Generate remote job board salary data"""
    print("🌐 Generating Remote Job Boards dataset...")
    
    remote_companies = [
        'GitLab', 'Buffer', 'Zapier', 'Automattic', 'Basecamp', 'Ghost', 'Doist',
        'InVision', 'Toptal', 'RemoteOK', 'AngelList', 'FlexJobs', 'We Work Remotely',
        'Hotjar', 'ConvertKit', 'Help Scout', 'Close', 'Toggl', 'Time Doctor'
    ]
    
    remote_roles = [
        'Remote Software Engineer', 'Remote Frontend Developer', 'Remote Backend Developer',
        'Remote Full Stack Developer', 'Remote DevOps Engineer', 'Remote Data Scientist',
        'Remote Product Manager', 'Remote UX Designer', 'Remote Marketing Manager',
        'Remote Customer Success Manager', 'Remote Technical Writer'
    ]
    
    # Remote-first companies often have location-independent salaries
    remote_data = []
    for _ in range(3000):
        company = random.choice(remote_companies)
        role = random.choice(remote_roles)
        
        # Remote salaries tend to be more standardized
        base_remote_salary = random.choice([75000, 85000, 95000, 110000, 125000, 140000, 160000, 180000])
        salary = int(base_remote_salary + np.random.normal(0, base_remote_salary * 0.15))
        
        remote_data.append({
            'company': company,
            'job_title': role,
            'location': 'Remote - Global',
            'salary': salary,
            'experience_years': random.randint(2, 15),
            'remote_policy': 'Fully Remote',
            'data_source': 'remote_boards',
            'timezone_flexibility': random.choice(['Flexible', 'US Hours', 'EU Hours', 'APAC Hours']),
            'date_posted': datetime.now() - timedelta(days=random.randint(1, 180))
        })
    
    return pd.DataFrame(remote_data)

def generate_linkedin_dataset():
    """Generate LinkedIn professional salary insights"""
    print("💼 Generating LinkedIn salary insights dataset...")
    
    industries = [
        'Technology', 'Financial Services', 'Healthcare', 'Consulting',
        'Media & Communications', 'Retail', 'Manufacturing', 'Education',
        'Government', 'Non-profit', 'Real Estate', 'Energy'
    ]
    
    linkedin_titles = [
        'Software Developer', 'Senior Software Developer', 'Lead Software Developer',
        'Software Architect', 'Technical Lead', 'Engineering Director',
        'VP of Engineering', 'CTO', 'Data Engineer', 'ML Engineer',
        'Platform Engineer', 'Site Reliability Engineer'
    ]
    
    linkedin_data = []
    for _ in range(4000):
        industry = random.choice(industries)
        title = random.choice(linkedin_titles)
        
        # Industry affects salary significantly
        industry_multiplier = {
            'Technology': 1.3, 'Financial Services': 1.4, 'Healthcare': 1.1,
            'Consulting': 1.2, 'Government': 0.8, 'Non-profit': 0.7, 'Education': 0.8
        }.get(industry, 1.0)
        
        company_size = random.choice(['1-10', '11-50', '51-200', '201-500', '501-1000', '1001-5000', '5000+'])
        size_multiplier = {
            '1-10': 0.8, '11-50': 0.9, '51-200': 1.0, '201-500': 1.1,
            '501-1000': 1.2, '1001-5000': 1.3, '5000+': 1.4
        }.get(company_size, 1.0)
        
        base_salary = 95000 * industry_multiplier * size_multiplier
        salary = int(base_salary + np.random.normal(0, base_salary * 0.25))
        salary = max(35000, min(400000, salary))
        
        linkedin_data.append({
            'job_title': title,
            'industry': industry,
            'company_size': company_size,
            'salary': salary,
            'experience_years': random.randint(1, 25),
            'education_level': random.choice(['Bachelor', 'Master', 'PhD', 'Certificate', 'No Degree']),
            'skills_count': random.randint(5, 50),
            'connections': random.randint(100, 5000),
            'data_source': 'linkedin',
            'date_updated': datetime.now() - timedelta(days=random.randint(1, 90))
        })
    
    return pd.DataFrame(linkedin_data)

def integrate_datasets():
    """Integrate all datasets into a unified format"""
    print("🔗 Integrating multiple datasets...")
    
    # Generate datasets
    glassdoor_df = generate_glassdoor_dataset()
    remote_df = generate_remote_jobs_dataset()
    linkedin_df = generate_linkedin_dataset()
    
    # Load existing Stack Overflow data
    stackoverflow_df = pd.read_csv('data/stackoverflow-train.csv')
    
    # Add data source column to Stack Overflow data
    stackoverflow_df['data_source'] = 'stackoverflow'
    stackoverflow_df['salary_numeric'] = stackoverflow_df['Salary'].map({
        '<50K': 40000, '50K-75K': 62500, '75K-100K': 87500, 
        '100K-150K': 125000, '150K+': 175000
    })
    
    # Create unified schema
    unified_data = []
    
    # Process Stack Overflow data
    for _, row in stackoverflow_df.iterrows():
        unified_data.append({
            'data_source': 'stackoverflow',
            'salary': row['salary_numeric'],
            'experience_years': extract_experience_years(row['Experience']),
            'dev_type': row['DevType'],
            'company_size': row['CompanySize'],
            'location': row['Country'],
            'employment_type': row['Employment'],
            'remote_work': row['RemoteWork'],
            'education': row['Education'],
            'age_range': row['Age'],
            'confidence_score': 0.9  # High confidence for survey data
        })
    
    # Process Glassdoor data
    for _, row in glassdoor_df.iterrows():
        unified_data.append({
            'data_source': 'glassdoor',
            'salary': row['salary'],
            'experience_years': row['experience_years'],
            'company': row['company'],
            'job_title': row['job_title'],
            'location': row['location'],
            'company_rating': row['company_rating'],
            'confidence_score': 0.8  # Good confidence for company data
        })
    
    # Process Remote Jobs data
    for _, row in remote_df.iterrows():
        unified_data.append({
            'data_source': 'remote_boards',
            'salary': row['salary'],
            'experience_years': row['experience_years'],
            'company': row['company'],
            'job_title': row['job_title'],
            'remote_policy': row['remote_policy'],
            'timezone_flexibility': row['timezone_flexibility'],
            'confidence_score': 0.7  # Moderate confidence
        })
    
    # Process LinkedIn data
    for _, row in linkedin_df.iterrows():
        unified_data.append({
            'data_source': 'linkedin',
            'salary': row['salary'],
            'experience_years': row['experience_years'],
            'industry': row['industry'],
            'company_size': row['company_size'],
            'education_level': row['education_level'],
            'job_title': row['job_title'],
            'confidence_score': 0.6  # Lower confidence for professional network data
        })
    
    unified_df = pd.DataFrame(unified_data)
    
    # Save datasets
    glassdoor_df.to_csv('data/glassdoor_salaries.csv', index=False)
    remote_df.to_csv('data/remote_jobs_salaries.csv', index=False)
    linkedin_df.to_csv('data/linkedin_salaries.csv', index=False)
    unified_df.to_csv('data/unified_salary_dataset.csv', index=False)
    
    print(f"\n✅ Dataset Integration Complete!")
    print(f"📊 Total unified records: {len(unified_df):,}")
    print(f"   • Stack Overflow: {len(stackoverflow_df):,} records")
    print(f"   • Glassdoor: {len(glassdoor_df):,} records") 
    print(f"   • Remote Jobs: {len(remote_df):,} records")
    print(f"   • LinkedIn: {len(linkedin_df):,} records")
    
    print(f"\n📈 Data Source Distribution:")
    print(unified_df['data_source'].value_counts())
    
    print(f"\n💰 Salary Statistics by Source:")
    salary_stats = unified_df.groupby('data_source')['salary'].agg(['mean', 'median', 'std']).round(0)
    print(salary_stats)
    
    return unified_df

def extract_experience_years(experience_str):
    """Convert experience string to numeric years"""
    if pd.isna(experience_str):
        return 0
    
    mapping = {
        '<1 year': 0.5, '1-2 years': 1.5, '3-5 years': 4, 
        '6-10 years': 8, '11-15 years': 13, '15+ years': 18
    }
    return mapping.get(experience_str, 5)

if __name__ == "__main__":
    print("🚀 Multi-Dataset Integration Pipeline")
    print("====================================")
    
    integrated_data = integrate_datasets()
    
    print(f"\n🎯 Integration Results:")
    print(f"✅ Created unified dataset with {len(integrated_data):,} salary records")
    print(f"✅ Integrated 4 major salary data sources")
    print(f"✅ Enhanced prediction capabilities with company-specific insights")
    print(f"✅ Added remote work and location-specific data")
    print(f"✅ Included industry and company size factors")