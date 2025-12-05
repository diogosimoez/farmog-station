"""
FarmOG Station - Utility Functions
==================================
Helper functions for image processing, data validation, etc.
"""

import numpy as np
from PIL import Image

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess image for model input
    
    Args:
        image_path: path to image file
        target_size: tuple (height, width)
    
    Returns:
        numpy array: preprocessed image
    """
    img = Image.open(image_path)
    img = img.convert('RGB')
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0  # Normalize to 0-1
    return img_array

def validate_sensor_data(sensor_data):
    """
    Validate and clean sensor data
    
    Returns:
        dict: validated sensor data with defaults for missing values
    """
    defaults = {
        'air_humidity': 60.0,
        'air_temp': 22.0,
        'soil_moisture': 50.0,
        'rainfall_24h': 0.0,
        'irrigation_method': 'drip'
    }
    
    validated = defaults.copy()
    
    for key, value in sensor_data.items():
        if value is not None:
            validated[key] = value
    
    return validated

def calculate_health_score(diagnosis):
    """
    Calculate overall plant health score (0-100)
    
    Args:
        diagnosis: dict from fusion_engine
    
    Returns:
        float: health score
    """
    if diagnosis["status"] == "CONFIRMED":
        # Diseased - score based on severity
        return max(0, 100 - diagnosis["confidence"])
    elif diagnosis["status"] == "EARLY_WARNING":
        # At risk - moderate score
        return max(50, 100 - diagnosis["confidence"] * 0.5)
    elif diagnosis["final_diagnosis"] == "Tomato___healthy":
        # Healthy - high score
        return min(100, diagnosis["confidence"])
    else:
        # Uncertain - moderate score
        return 60.0