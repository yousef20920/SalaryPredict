# Salary Predictor Web Application

This is a full-stack web application that uses machine learning to predict salary categories based on demographic and employment information.

## Features

- **React Frontend**: Beautiful, responsive user interface with modern design
- **Flask Backend**: RESTful API serving the trained ML model
- **Naive Bayes ML Model**: Pre-trained model with 85% accuracy for salary prediction
- **Real-time Predictions**: Instant salary category predictions with confidence scores
- **Probability Visualization**: Visual breakdown of prediction probabilities

## Architecture

```
├── app.py                    # Flask backend API
├── naive_bayes_solution.py   # ML model implementation
├── bnetbase.py              # Bayesian network base classes
├── data/                    # Dataset files
│   ├── adult-train.csv      # Training data
│   └── adult-test.csv       # Test data
└── frontend/                # React application
    ├── src/
    │   ├── App.js           # Main React component
    │   └── App.css          # Styling
    └── package.json         # Dependencies
```

## Prerequisites

- Python 3.7+ 
- Node.js 14+
- npm or yarn

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SalaryPredict
```

### 2. Backend Setup (Flask)
```bash
# Install Python dependencies
pip install flask flask-cors

# Test the ML model (optional)
python naive_bayes_solution.py
```

### 3. Frontend Setup (React)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Install additional dependencies
npm install axios
```

## Running the Application

### Start the Backend (Terminal 1)
```bash
# From the root directory
python app.py
```
The Flask API will start on `http://localhost:5000`

### Start the Frontend (Terminal 2)
```bash
# From the frontend directory
cd frontend
npm start
```
The React app will start on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Fill out all the form fields with your information:
   - **Work**: Employment type (Private, Government, Self-employed, Not Working)
   - **Education**: Education level (from <Gr12 to Doctorate)
   - **Occupation**: Job category (Admin, Professional, Service, etc.)
   - **Marital Status**: Relationship status
   - **Relationship**: Family relationship role
   - **Race**: Demographic information
   - **Gender**: Male or Female
   - **Country**: Geographic region
3. Click "Predict Salary" to get your prediction
4. View the results showing:
   - Predicted salary category (< $50K or ≥ $50K)
   - Confidence percentage
   - Probability breakdown with visual bars

## API Endpoints

### GET /
Health check endpoint

### GET /api/domains
Returns available options for all form fields

### POST /api/predict
Predicts salary based on input features

**Request Body:**
```json
{
  "Work": "Private",
  "Education": "Bachelors",
  "Occupation": "Professional",
  "MaritalStatus": "Married",
  "Relationship": "Husband",
  "Race": "White",
  "Gender": "Male",
  "Country": "North-America"
}
```

**Response:**
```json
{
  "prediction": ">=50K",
  "confidence": 0.937,
  "probabilities": {
    "<50K": 0.063,
    ">=50K": 0.937
  },
  "input_data": { ... }
}
```

## Model Information

The application uses a Naive Bayes classifier trained on the Adult Census Income dataset:
- **Training Data**: 32,561 records
- **Features**: 8 demographic and employment attributes
- **Target**: Binary salary classification (<$50K vs ≥$50K)
- **Accuracy**: ~85% on test data
- **Fairness**: Implements bias reduction techniques

## Troubleshooting

### Backend Issues
- Ensure Flask dependencies are installed: `pip install flask flask-cors`
- Check that port 5000 is not in use
- Verify all data files are present in the `data/` directory

### Frontend Issues
- Ensure Node.js dependencies are installed: `npm install`
- Check that port 3000 is not in use
- Verify the backend is running on port 5000

### CORS Issues
- The Flask backend includes CORS headers for localhost:3000
- If accessing from a different port, update the CORS configuration in `app.py`

## Technology Stack

- **Frontend**: React, Axios, CSS3
- **Backend**: Flask, Flask-CORS
- **Machine Learning**: Custom Naive Bayes implementation
- **Data**: UCI Adult Census Income Dataset

## Future Enhancements

- Add more sophisticated ML models (Random Forest, Neural Networks)
- Implement user authentication and prediction history
- Add data visualization for model insights
- Deploy to cloud platforms (AWS, Heroku, etc.)
- Add A/B testing for different model versions
- Implement real-time model retraining

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is for educational purposes. The underlying dataset is from the UCI Machine Learning Repository.