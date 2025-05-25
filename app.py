from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model artifacts
model_artifacts = None

def load_model():
    """Load the trained model and preprocessing objects"""
    global model_artifacts
    try:
        with open('crop_yield_model_sa.pkl', 'rb') as f:
            model_artifacts = pickle.load(f)
        logger.info("Model loaded successfully")
        return True
    except FileNotFoundError:
        logger.error("Model file not found. Please ensure 'crop_yield_model_sa.pkl' is in the project directory.")
        return False
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def preprocess_input(area, item, year, avg_temp, rainfall, pesticides):
    """Preprocess input data for prediction"""
    try:
        # Extract model artifacts
        scaler = model_artifacts['scaler']
        encoders = model_artifacts['encoders']
        le_area, le_item, le_climate, le_rainfall = encoders
        
        # Create feature engineering
        temp_rainfall_ratio = avg_temp / (rainfall + 1)
        pesticide_intensity = pesticides / (year - 1960 + 1)  # Fixed calculation
        
        # Climate zone categorization
        if avg_temp <= 15:
            climate_zone = 'Cold'
        elif avg_temp <= 25:
            climate_zone = 'Temperate'
        elif avg_temp <= 35:
            climate_zone = 'Warm'
        else:
            climate_zone = 'Hot'
        
        # Rainfall zone categorization
        if rainfall <= 500:
            rainfall_zone = 'Low'
        elif rainfall <= 1000:
            rainfall_zone = 'Medium'
        elif rainfall <= 1500:
            rainfall_zone = 'High'
        else:
            rainfall_zone = 'Very High'
        
        # Encode categorical variables
        try:
            area_encoded = le_area.transform([area])[0]
        except ValueError:
            logger.warning(f"Unknown area '{area}', using default encoding")
            area_encoded = 0
        
        try:
            item_encoded = le_item.transform([item])[0]
        except ValueError:
            logger.warning(f"Unknown crop '{item}', using default encoding")
            item_encoded = 0
        
        try:
            climate_encoded = le_climate.transform([climate_zone])[0]
        except ValueError:
            climate_encoded = 0
        
        try:
            rainfall_encoded = le_rainfall.transform([rainfall_zone])[0]
        except ValueError:
            rainfall_encoded = 0
        
        # Create feature vector
        features = np.array([[
            year, avg_temp, rainfall, pesticides,
            temp_rainfall_ratio, pesticide_intensity,
            area_encoded, item_encoded, climate_encoded, rainfall_encoded
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        return features_scaled, {
            'climate_zone': climate_zone,
            'rainfall_zone': rainfall_zone,
            'temp_rainfall_ratio': temp_rainfall_ratio,
            'pesticide_intensity': pesticide_intensity
        }
        
    except Exception as e:
        logger.error(f"Error in preprocessing: {str(e)}")
        raise

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Make crop yield prediction"""
    try:
        if model_artifacts is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get input data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['area', 'item', 'year', 'avg_temp', 'rainfall', 'pesticides']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract and validate input
        area = data['area']
        item = data['item']
        year = int(data['year'])
        avg_temp = float(data['avg_temp'])
        rainfall = float(data['rainfall'])
        pesticides = float(data['pesticides'])
        
        # Validate ranges
        if not (1990 <= year <= 2030):
            return jsonify({'error': 'Year must be between 1990 and 2030'}), 400
        if not (-10 <= avg_temp <= 50):
            return jsonify({'error': 'Average temperature must be between -10°C and 50°C'}), 400
        if not (0 <= rainfall <= 5000):
            return jsonify({'error': 'Rainfall must be between 0 and 5000 mm'}), 400
        if pesticides < 0:
            return jsonify({'error': 'Pesticides amount cannot be negative'}), 400
        
        # Preprocess input
        features_scaled, preprocessing_info = preprocess_input(
            area, item, year, avg_temp, rainfall, pesticides
        )
        
        # Make prediction and convert numpy types to Python native types
        model = model_artifacts['model']
        prediction = float(model.predict(features_scaled)[0])
        
        # Convert preprocessing info numpy values to Python native types
        processed_info = {}
        for key, value in preprocessing_info.items():
            if isinstance(value, (np.floating, np.integer)):
                processed_info[key] = float(value)
            else:
                processed_info[key] = value
        
        # Prepare response
        response = {
            'prediction': prediction,
            'prediction_kg': prediction / 10,  # Convert hg/ha to kg/ha
            'unit': 'kg/ha',
            'input_summary': {
                'area': area,
                'crop': item,
                'year': year,
                'avg_temperature': float(avg_temp),
                'rainfall': float(rainfall),
                'pesticides': float(pesticides)
            },
            'preprocessing_info': processed_info,
            'interpretation': get_yield_interpretation(prediction)
        }
        
        logger.info(f"Prediction made: {prediction/10:.2f} kg/ha for {item} in {area}")
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error during prediction'}), 500

def get_yield_interpretation(yield_value):
    """Provide interpretation of yield prediction"""
    if yield_value < 20000:
        return "Low yield - Consider improving farming practices"
    elif yield_value < 40000:
        return "Moderate yield - Room for optimization"
    elif yield_value < 60000:
        return "Good yield - Above average performance"
    else:
        return "Excellent yield - High productivity achieved"

@app.route('/api/info')
def api_info():
    """Provide API information"""
    if model_artifacts is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    info = {
        'model_type': 'XGBoost Regressor',
        'target_region': 'South Asian Countries',
        'supported_countries': model_artifacts['south_asian_countries'],
        'features': model_artifacts['feature_names'],
        'api_version': '1.0',
        'prediction_unit': 'hectograms per hectare (hg/ha)'
    }
    return jsonify(info)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy' if model_artifacts is not None else 'unhealthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model_artifacts is not None
    }
    return jsonify(status)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        print("🌾 Crop Yield Prediction API is ready!")
        print("📊 Model loaded successfully")
        print("🌐 Starting Flask application...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to load model. Please check if 'crop_yield_model_sa.pkl' exists.")
        print("📝 Run the Google Colab notebook first to generate the model file.")