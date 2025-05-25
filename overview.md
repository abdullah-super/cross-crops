# Crop Yield Prediction System - Project Report

## Project Overview

CrossLit Crop Prediction is a machine learning-powered agricultural yield forecasting system specifically designed for South Asian agriculture. The system provides accurate crop yield predictions based on various environmental and agricultural factors, helping farmers and agricultural planners make informed decisions.

## Technical Stack

- **Backend Framework**: Flask
- **Machine Learning Framework**: XGBoost
- **Additional Libraries**:
  - NumPy (>= 1.26.0)
  - Pandas (>= 2.2.0)
  - Scikit-learn (>= 1.4.0)
  - XGBoost (>= 2.0.0)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn (>= 21.2.0)

## Model Architecture

### Machine Learning Model

- **Type**: XGBoost Regressor
- **Target Region**: South Asian Countries
- **Input Features**:
  - Year (1990-2030)
  - Average Temperature (-10°C to 50°C)
  - Annual Rainfall (0-5000mm)
  - Pesticides Usage (tonnes)
  - Derived Features:
    - Temperature-Rainfall Ratio
    - Pesticide Intensity
    - Climate Zone Classification
    - Rainfall Zone Classification

### Feature Engineering

1. **Climate Zone Categorization**:

   - Cold: ≤ 15°C
   - Temperate: 15-25°C
   - Warm: 25-35°C
   - Hot: > 35°C

2. **Rainfall Zone Categorization**:

   - Low: ≤ 500mm
   - Medium: 500-1000mm
   - High: 1000-1500mm
   - Very High: > 1500mm

3. **Derived Metrics**:
   - Temperature-Rainfall Ratio = avg_temp / (rainfall + 1)
   - Pesticide Intensity = pesticides / (year - 1960 + 1)

## API Endpoints

1. **Main Endpoints**:

   - `GET /`: Home page
   - `POST /predict`: Crop yield prediction
   - `GET /api/info`: Model information
   - `GET /health`: Health check

2. **Error Handling**:
   - 404: Endpoint not found
   - 500: Internal server error
   - Input validation errors with specific messages

## Prediction Output

The system provides comprehensive output including:

- Yield prediction in kg/ha
- Interpretation of yield levels:
  - < 20,000: Low yield
  - 20,000-40,000: Moderate yield
  - 40,000-60,000: Good yield
  - > 60,000: Excellent yield
- Input parameter summary
- Preprocessing information including climate and rainfall zones

## Data Sources

The system uses multiple data sources stored in the datasets folder:

- pesticides.csv
- rainfall.csv
- temp.csv
- yield.csv
- yield_df.csv

## User Interface Features

1. **Input Section**:

   - Country/Region selection (India, Pakistan, Bangladesh, Sri Lanka)
   - Year selection (1990-2030)
   - Average temperature input
   - Annual rainfall input
   - Pesticides usage input

2. **Results Section**:
   - Prediction display with interpretation
   - Input summary
   - Processing information
   - Real-time error handling and validation

## Model Performance and Validation

The model was trained on South Asian agricultural data with robust preprocessing and validation:

- Feature scaling for numerical inputs
- Label encoding for categorical variables
- Input range validation
- Error handling for unknown categories

## Deployment

The application is designed to run as a web service with the following features:

- RESTful API architecture
- Gunicorn server support
- Docker compatibility
- Health monitoring endpoint
- Comprehensive logging system

## Future Enhancements

Potential areas for improvement:

1. Extended geographical coverage
2. Additional crop types support
3. Integration with weather APIs
4. Mobile application development
5. Real-time data updates
6. Enhanced visualization features
