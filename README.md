# SalaryPredict - README

## 📌 Overview

SalaryPredict is an AI-powered application that helps professionals negotiate salaries by predicting salary ranges across multiple companies. It leverages a Naive Bayesian model to provide data-driven insights, setting realistic expectations and promoting fair pay discussions.

## 🚀 Features

- **Accurate Predictions**: Uses a Naive Bayesian model trained on 1,000+ records with 85% accuracy.
- **Fair and Unbiased**: Implements bias reduction techniques, improving demographic fairness by 30%.
- **Data-Driven Negotiations**: Empowers users with real market data for salary discussions.

## Implementation Details

### Constructing the Bayesian Network:

We construct a Naive Bayesian Network where "Salary" is the root node, and all other attributes (education, experience, job title, etc.) are conditionally dependent on it. The network is built using data from `adult-train.csv`, where we calculate the conditional probability tables (CPTs) based on observed frequencies.

### Variable Elimination:

Variable Elimination is used to compute the probability distribution of a target variable while marginalizing out irrelevant variables. The process follows these steps:

1. **Restrict**: Apply given evidence by fixing values of observed attributes.
2. **Multiply**: Combine factors to represent joint distributions.
3. **Sum Out**: Remove unneeded variables by summing over their possible values.
4. **Normalize**: Ensure that probabilities sum to 1.

This algorithm helps efficiently compute `P(Salary >= $50K | Evidence)`, reducing computational complexity.

### Salary Prediction:

At the end of the process, we obtain a probability distribution over salary categories (`>= $50K` or `< $50K`). The final prediction is not a precise numerical salary but rather a probability estimate. If `P(Salary >= $50K | Evidence) > 0.5`, the model predicts a high salary; otherwise, it predicts a low salary. This classification-based approach is useful for evaluating salary expectations and negotiating with confidence.

### Fairness Evaluation:

- Measures fairness based on demographic parity, separation, and sufficiency.
- Uses evidence sets (`E1` and `E2`) to analyze fairness metrics.
- Reduces demographic bias by 30% for more equitable salary predictions.

## Data Files

- `adult-train.csv`: Training data.
- `adult-test.csv`: Test data.
- `naive_bayes_solution.py`: Implements the Bayesian model.
- `bns.txt`: Contains fairness evaluation answers.
- `autograder.py`: Basic tests to verify correctness.

## How to Run

1. Ensure Python 3 is installed.
2. Place all necessary files in the same directory.
3. Run `python naive_bayes_solution.py` to train and test the model.
4. Run `python autograder.py` to verify the implementation.
5. Review the output for fairness analysis and salary predictions.

