import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:5001';

function App() {
  const [formData, setFormData] = useState({
    Age: '',
    Education: '',
    Employment: '',
    RemoteWork: '',
    Experience: '',
    DevType: '',
    CompanySize: '',
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

  const getFieldLabel = (field) => {
    const labels = {
      'Age': 'Age Range',
      'Education': 'Education Level', 
      'Employment': 'Employment Type',
      'RemoteWork': 'Work Arrangement',
      'Experience': 'Years of Coding Experience',
      'DevType': 'Developer Type',
      'CompanySize': 'Company Size',
      'Country': 'Country/Region'
    };
    return labels[field] || field;
  };

  const getSalaryDisplayName = (range) => {
    const names = {
      '<50K': 'Less than $50K',
      '50K-75K': '$50K - $75K',
      '75K-100K': '$75K - $100K', 
      '100K-150K': '$100K - $150K',
      '150K+': '$150K or more'
    };
    return names[range] || range;
  };

  const getSalaryClass = (range) => {
    if (range === '<50K') return 'low-salary';
    if (range === '50K-75K') return 'mid-low-salary';
    if (range === '75K-100K') return 'mid-salary';
    if (range === '100K-150K') return 'mid-high-salary';
    if (range === '150K+') return 'high-salary';
    return 'mid-salary';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>� Developer Salary Predictor</h1>
        <p>Predict your salary using Stack Overflow's 2023 Developer Survey data</p>
      </header>

      <main className="App-main">
        <div className="main-container">
          <div className="form-section">
            <div className="form-container">
              <form onSubmit={handleSubmit} className="prediction-form">
                <h2>Enter Your Developer Profile</h2>
                
                {Object.entries(domains).map(([field, options]) => (
                  <div key={field} className="form-group">
                    <label htmlFor={field}>
                      {getFieldLabel(field)}:
                    </label>
                    <select
                      id={field}
                      name={field}
                      value={formData[field]}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select {getFieldLabel(field)}</option>
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
            </div>
          </div>

          <div className="results-section">
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
                    <h3>Predicted Salary Range</h3>
                    <div className={`salary-badge ${getSalaryClass(prediction.prediction)}`}>
                      {getSalaryDisplayName(prediction.prediction)}
                    </div>
                    <p className="confidence">
                      Confidence: {(prediction.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                  
                  <div className="probability-breakdown">
                    <h4>All Salary Range Probabilities</h4>
                    <div className="probability-bars">
                      {Object.entries(prediction.probabilities).map(([range, prob]) => (
                        <div key={range} className="probability-item">
                          <span className="probability-label">{getSalaryDisplayName(range)}:</span>
                          <div className="probability-bar">
                            <div 
                              className={`probability-fill ${getSalaryClass(range)}`}
                              style={{ width: `${prob * 100}%` }}
                            ></div>
                          </div>
                          <span className="probability-value">
                            {(prob * 100).toFixed(1)}%
                          </span>
                        </div>
                      ))}
                    </div>
                    <div className="ml-insight">
                      <p><strong>🧠 ML Insight:</strong> These probabilities are calculated by analyzing similar developer profiles from {prediction.data_insights?.total_training_samples?.toLocaleString() || '43,853'} real Stack Overflow survey responses.</p>
                      
                      {prediction.data_insights && (
                        <div className="data-breakdown">
                          <h5>📊 Data Analysis for Your Profile:</h5>
                          <div className="insight-stats">
                            <div className="stat-item">
                              <span className="stat-label">🎯 Exact profile matches:</span>
                              <span className="stat-value">{prediction.data_insights.exact_profile_matches} developers</span>
                            </div>
                            
                            <div className="feature-matches">
                              <span className="stat-label">👥 Similar developers by characteristic:</span>
                              <div className="feature-match-list">
                                {Object.entries(prediction.data_insights.feature_matches).map(([feature, count]) => (
                                  <div key={feature} className="feature-match">
                                    <span className="feature-name">{getFieldLabel(feature)}:</span>
                                    <span className="feature-count">{count.toLocaleString()} devs</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                          
                          <p className="data-note">
                            <strong>💡 How it works:</strong> The model identified {prediction.data_insights.exact_profile_matches} developers with your exact profile, plus thousands more with similar characteristics, to calculate these probabilities.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {!prediction && !error && !loading && (
              <div className="placeholder-message">
                <h2>👋 Welcome!</h2>
                <p>Fill out the form on the left to get your salary prediction based on real Stack Overflow developer survey data.</p>
                
                <div className="features-list">
                  <h3>What we'll predict:</h3>
                  <ul>
                    <li>💰 Your expected salary range</li>
                    <li>📊 Confidence levels for each bracket</li>
                    <li>🎯 Probability breakdown across all ranges</li>
                  </ul>
                </div>

                <div className="ml-explanation">
                  <h3>🧠 How Our ML Works:</h3>
                  <div className="ml-details">
                    <div className="ml-step">
                      <div className="step-icon">📊</div>
                      <div className="step-content">
                        <strong>Real Data:</strong> Trained on 43,853 developer profiles from Stack Overflow's 2023 survey
                      </div>
                    </div>
                    <div className="ml-step">
                      <div className="step-icon">🎯</div>
                      <div className="step-content">
                        <strong>Naive Bayes:</strong> Calculates probabilities based on how similar developers are compensated
                      </div>
                    </div>
                    <div className="ml-step">
                      <div className="step-icon">🔮</div>
                      <div className="step-content">
                        <strong>Smart Predictions:</strong> Considers complex interactions between experience, location, role, and company size
                      </div>
                    </div>
                    <div className="ml-step">
                      <div className="step-icon">📈</div>
                      <div className="step-content">
                        <strong>Confidence Scores:</strong> Shows uncertainty and alternative possibilities, not just one guess
                      </div>
                    </div>
                  </div>
                  
                  <div className="why-ml">
                    <h4>🤔 Why ML instead of simple rules?</h4>
                    <p>Simple scripts use hardcoded guesses. Our ML model discovers real patterns from 43K+ actual developer salaries, handles complex feature interactions, and provides probability distributions with confidence scores.</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>Powered by Stack Overflow 2023 Developer Survey • Built with React & Flask</p>
      </footer>
    </div>
  );
}

export default App;
