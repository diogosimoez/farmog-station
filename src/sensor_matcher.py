"""
FarmOG Station - Sensor Pattern Matching
========================================
Calculates disease risk scores based on environmental sensor data
"""

import numpy as np
from src.disease_siganture import DISEASE_SIGNATURES, get_all_diseases

def calculate_disease_risk(sensor_data, disease_name):
    """
    Calculate risk score (0-100) for a specific disease based on sensor readings
    
    Args:
        sensor_data: dict with keys like 'air_humidity', 'air_temp', 'soil_moisture', etc.
        disease_name: string, disease class name
    
    Returns:
        float: risk score 0-100
    """
    signature = DISEASE_SIGNATURES.get(disease_name)
    if not signature:
        return 0.0
    
    conditions = signature['sensor_conditions']
    weights = signature['risk_weights']
    
    risk_score = 0.0
    
    # Humidity check
    if 'humidity' in weights and 'air_humidity' in sensor_data:
        humidity = sensor_data['air_humidity']
        
        if 'air_humidity_min' in conditions:
            if humidity >= conditions['air_humidity_min']:
                risk_score += 100 * weights['humidity']
            else:
                # Partial score if close
                diff = conditions['air_humidity_min'] - humidity
                if diff < 10:
                    risk_score += (100 - diff * 10) * weights['humidity']
        
        elif 'air_humidity_max' in conditions:  # Spider mites (LOW humidity)
            if humidity <= conditions['air_humidity_max']:
                risk_score += 100 * weights['humidity']
        
        elif 'air_humidity_range' in conditions:  # Healthy range
            min_h, max_h = conditions['air_humidity_range']
            if min_h <= humidity <= max_h:
                risk_score += 100 * weights['humidity']
    
    # Temperature check
    if 'temperature' in weights and 'air_temp' in sensor_data:
        temp = sensor_data['air_temp']
        
        if 'air_temp_range' in conditions:
            min_t, max_t = conditions['air_temp_range']
            if min_t <= temp <= max_t:
                risk_score += 100 * weights['temperature']
            else:
                # Partial score if within 5°C
                if temp < min_t and (min_t - temp) < 5:
                    risk_score += (100 - (min_t - temp) * 20) * weights['temperature']
                elif temp > max_t and (temp - max_t) < 5:
                    risk_score += (100 - (temp - max_t) * 20) * weights['temperature']
    
    # Soil moisture check
    if 'moisture' in weights and 'soil_moisture' in sensor_data:
        moisture = sensor_data['soil_moisture']
        target = conditions.get('soil_moisture', 'optimal')
        
        if target == 'high' and moisture > 70:
            risk_score += 100 * weights['moisture']
        elif target == 'optimal' and 40 <= moisture <= 70:
            risk_score += 100 * weights['moisture']
        elif target == 'low' and moisture < 40:
            risk_score += 100 * weights['moisture']
    
    # Irrigation method check
    if 'irrigation' in weights and 'irrigation_method' in sensor_data:
        method = sensor_data['irrigation_method']
        risk_method = conditions.get('irrigation_risk')
        
        if risk_method == 'overhead' and method == 'overhead':
            risk_score += 100 * weights['irrigation']
        elif risk_method != 'overhead' or method == 'drip':
            risk_score += 0  # No additional risk
    
    # Rainfall check
    if 'rainfall' in weights and 'rainfall_24h' in sensor_data:
        rain = sensor_data['rainfall_24h']
        if conditions.get('rainfall') == 'frequent' and rain > 5:
            risk_score += 100 * weights['rainfall']
    
    return min(100.0, risk_score)

def get_all_disease_risks(sensor_data):
    """
    Calculate risk scores for all diseases
    
    Returns:
        dict: {disease_name: risk_score}
    """
    risks = {}
    for disease in get_all_diseases():
        risks[disease] = calculate_disease_risk(sensor_data, disease)
    
    return risks

def get_top_risks(sensor_data, top_n=3):
    """
    Get top N diseases by risk score
    
    Returns:
        list of tuples: [(disease_name, risk_score), ...]
    """
    risks = get_all_disease_risks(sensor_data)
    sorted_risks = sorted(risks.items(), key=lambda x: x[1], reverse=True)
    return sorted_risks[:top_n]