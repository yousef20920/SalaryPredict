import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [formData, setFormData] = useState({
    Work: '',
    Education: '',
    Occupation: '',
    MaritalStatus: '',
    Relationship: '',
    Race: '',
    Gender: '',
    Country: ''
  });
  
  const [domains, setDomains] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load domains on component mount
  useEffect(() => {
    const fetchDomains = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/domains`);
        setDomains(response.data);
      } catch (err) {
        setError('Failed to load form options. Please ensure the backend is running.');
      }
    };

    fetchDomains();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/predict`, formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = Object.values(formData).every(value => value !== '');

  return (
    <div className="App">
      <header className="App-header">
        <h1>💰 Salary Predictor</h1>
        <p>Predict your salary category using AI-powered machine learning</p>
      </header>

      <main className="App-main">
        <div className="form-container">
          <form onSubmit={handleSubmit} className="prediction-form">
            <h2>Enter Your Information</h2>
            
            {Object.entries(domains).map(([field, options]) => (
              <div key={field} className="form-group">
                <label htmlFor={field}>
                  {field === 'MaritalStatus' ? 'Marital Status' : field}:
                </label>
                <select
                  id={field}
                  name={field}
                  value={formData[field]}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select {field === 'MaritalStatus' ? 'Marital Status' : field}</option>
                  {options.map(option => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>
            ))}

            <button 
              type="submit" 
              disabled={!isFormValid || loading}
              className="predict-button"
            >
              {loading ? 'Predicting...' : 'Predict Salary'}
            </button>
          </form>

          {error && (
            <div className="error-message">
              <h3>Error</h3>
              <p>{error}</p>
            </div>
          )}

          {prediction && (
            <div className="prediction-result">
              <h2>Prediction Result</h2>
              <div className="prediction-card">
                <div className="main-prediction">
                  <h3>Predicted Salary Category</h3>
                  <div className={`salary-badge ${prediction.prediction === '>=50K' ? 'high-salary' : 'low-salary'}`}>
                    {prediction.prediction === '>=50K' ? '$50,000 or Higher' : 'Less than $50,000'}
                  </div>
                  <p className="confidence">
                    Confidence: {(prediction.confidence * 100).toFixed(1)}%
                  </p>
                </div>
                
                <div className="probability-breakdown">
                  <h4>Probability Breakdown</h4>
                  <div className="probability-bars">
                    <div className="probability-item">
                      <span className="probability-label">≥ $50K:</span>
                      <div className="probability-bar">
                        <div 
                          className="probability-fill high"
                          style={{ width: `${prediction.probabilities['>=50K'] * 100}%` }}
                        ></div>
                      </div>
                      <span className="probability-value">
                        {(prediction.probabilities['>=50K'] * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="probability-item">
                      <span className="probability-label">&lt; $50K:</span>
                      <div className="probability-bar">
                        <div 
                          className="probability-fill low"
                          style={{ width: `${prediction.probabilities['<50K'] * 100}%` }}
                        ></div>
                      </div>
                      <span className="probability-value">
                        {(prediction.probabilities['<50K'] * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>Powered by Naive Bayes Machine Learning • Built with React & Flask</p>
      </footer>
    </div>
  );
}

export default App;
