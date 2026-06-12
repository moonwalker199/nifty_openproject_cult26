# InvestIQ

AI-Powered Investment Intelligence Platform built using historical NIFTY-50 market data.

Developed for the **Data-Driven Investment Intelligence Using NIFTY-50 Market Data Challenge**.

---

## Overview

InvestIQ transforms raw stock market data into actionable investment intelligence through:

- Stock Movement Prediction
- Portfolio Construction
- Risk Assessment
- Explainable AI Insights
- Personalized Investment Recommendations

The platform helps investors make informed decisions using historical NIFTY-50 market data from 2000–2021.

---

## Features

### 1. Stock Predictor Engine

Predicts future stock movement direction:

- UP
- DOWN

Uses machine learning-based classification with:

- Technical indicators
- Historical price trends
- Volume information

Model evaluation includes:

- Accuracy
- Precision
- Recall
- F1 Score

---

### 2. Portfolio Construction Module

Generates portfolios for different investor profiles:

#### Conservative Investor

Focus:

- Lower volatility
- Capital preservation

#### Balanced Investor

Focus:

- Return-risk balance

#### Aggressive Investor

Focus:

- Higher return potential

Portfolio allocations are generated automatically using historical returns and risk statistics.

---

### 3. Risk Assessment Module

Provides comprehensive risk analytics including:

- Annual Return
- Volatility
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Risk Adjusted Return
- Beta Analysis

---

### 4. Explainable AI Framework

Provides transparent reasoning behind:

- Stock predictions
- Portfolio recommendations
- Risk evaluations

Examples:

- Strong upward momentum detected
- High historical volatility observed
- Portfolio optimized for risk-adjusted returns

---

### 5. Investment Recommendation Engine

Generates actionable recommendations:

- BUY
- HOLD
- AVOID

Based on:

- Prediction output
- Risk metrics
- Historical performance

---

## Dataset

Source:

NIFTY-50 Stock Market Dataset

Contains:

- Open Price
- High Price
- Low Price
- Close Price
- Volume
- Turnover

Coverage:

- January 2000 to April 2021

Companies:

- NIFTY-50 constituent stocks across multiple sectors

---

## Project Structure

```text
InvestIQ/

│
├── app.py
│
├── data/
│   └── NIFTY50_all.csv
│
├── src/
│   ├── predictor.py
│   ├── portfolio.py
│   ├── risk.py
│   ├── explainability.py
│   └── utils.py
│
├── README.md
│
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd InvestIQ
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Required Libraries

```bash
pip install streamlit
pip install pandas
pip install numpy
pip install scikit-learn
pip install plotly
```

Or:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## Methodology

### Feature Engineering

The platform derives financial indicators from historical data:

- Daily Returns
- Moving Averages
- Volatility Measures
- Momentum Features

### Prediction Model

Machine learning classifier trained on:

- Historical prices
- Market behavior
- Trend features

Output:

- UP
- DOWN

### Portfolio Optimization

Portfolio construction uses:

- Historical returns
- Volatility estimates
- Risk-adjusted performance

### Risk Analytics

Risk metrics are calculated using:

- Annualized returns
- Volatility
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Beta

---

## Explainability

InvestIQ emphasizes transparency by providing explanations for:

- Forecasts
- Risk scores
- Portfolio allocations
- Investment recommendations

This allows investors to understand why a recommendation was generated.

---

## Key Capabilities

- Historical Stock Analysis
- Market Trend Understanding
- Investment Opportunity Evaluation
- Portfolio Recommendation
- Risk Assessment
- Explainable Decision Support

---

## Reproducibility

The project is fully reproducible using:

- Provided source code
- NIFTY-50 dataset
- Listed dependencies

No external APIs or live market data are used.

---

## Challenge Compliance

This solution follows all competition constraints:

### Allowed

- Historical market data
- Feature engineering
- Technical indicators
- Machine learning
- Portfolio optimization
- Risk analytics

### Not Used

- Live market data
- Financial APIs
- News datasets
- Social media sentiment
- Proprietary datasets

---

## Authors

Team Name: InvestIQ

Data-Driven Investment Intelligence Using NIFTY-50 Market Data Challenge