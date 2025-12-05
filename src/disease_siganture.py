"""
FarmOG Station - Disease Signature Database
===========================================
Maps disease conditions to sensor patterns based on agronomic research
"""

# Disease signature patterns from your master table
DISEASE_SIGNATURES = {
    "Tomato___Bacterial_spot": {
        "name": "Bacterial Spot",
        "sensor_conditions": {
            "air_humidity_min": 85,
            "air_temp_range": (20, 30),
            "soil_moisture": "high",
            "irrigation_risk": "overhead"  # overhead irrigation increases risk
        },
        "visual_markers": ["brown_irregular_lesions", "tiny_specks_with_halo"],
        "risk_weights": {
            "humidity": 0.4,
            "temperature": 0.3,
            "moisture": 0.2,
            "irrigation": 0.1
        },
        "corrective_actions": [
            "Stop overhead irrigation immediately",
            "Switch to drip irrigation",
            "Space plants wider to improve airflow",
            "Prune lower leaves to reduce splash infection",
            "Apply copper-based bactericide if severe"
        ],
        "root_cause": "High humidity + overhead irrigation creates splash transmission",
        "prevention": "Use drip irrigation from the start, increase plant spacing"
    },
    
    "Tomato___Early_blight": {
        "name": "Early Blight",
        "sensor_conditions": {
            "air_humidity_min": 80,
            "air_temp_range": (24, 30),
            "soil_moisture": "high",
            "canopy_light": "low"
        },
        "visual_markers": ["concentric_leaf_spots", "yellow_halo", "lower_leaves_affected"],
        "risk_weights": {
            "humidity": 0.4,
            "temperature": 0.35,
            "moisture": 0.15,
            "canopy": 0.1
        },
        "corrective_actions": [
            "Prune lower leaves to improve airflow",
            "Avoid overhead irrigation - use drip only",
            "Increase spacing between plants",
            "Apply mulch to reduce soil splash",
            "Remove severely infected leaves"
        ],
        "root_cause": "Warm humid conditions + poor airflow favor Alternaria fungus",
        "prevention": "Good spacing, drip irrigation, regular pruning"
    },
    
    "Tomato___Late_blight": {
        "name": "Late Blight",
        "sensor_conditions": {
            "air_humidity_min": 90,
            "air_temp_range": (10, 21),
            "rainfall": "frequent",
            "leaf_wetness": "continuous"
        },
        "visual_markers": ["water_soaked_lesions", "white_mold_underside", "rapid_collapse"],
        "risk_weights": {
            "humidity": 0.5,
            "temperature": 0.3,
            "rainfall": 0.2
        },
        "corrective_actions": [
            "⚠️ URGENT: Remove and destroy infected plants immediately",
            "Reduce watering during high-risk periods",
            "Increase airflow around all plants",
            "Apply preventive fungicide to healthy plants",
            "Use protective covers if persistent wet weather"
        ],
        "root_cause": "Cool saturated air (90%+ humidity) + continuous leaf wetness",
        "prevention": "Monitor weather forecasts, apply preventive fungicide before rain"
    },
    
    "Tomato___Septoria_leaf_spot": {
        "name": "Septoria Leaf Spot",
        "sensor_conditions": {
            "air_humidity_min": 80,
            "air_temp_range": (20, 28),
            "soil_moisture": "high",
            "canopy_density": "high"
        },
        "visual_markers": ["small_circular_spots", "dark_borders", "lower_leaves_infected"],
        "risk_weights": {
            "humidity": 0.45,
            "temperature": 0.25,
            "moisture": 0.2,
            "canopy": 0.1
        },
        "corrective_actions": [
            "Remove infected lower leaves",
            "Improve airflow (prune and increase spacing)",
            "Use drip irrigation only - avoid wetting foliage",
            "Apply fungicide if spreading rapidly"
        ],
        "root_cause": "High humidity + dense canopy + wet soil surface",
        "prevention": "Good spacing, bottom watering, regular pruning"
    },
    
    "Tomato___Leaf_Mold": {
        "name": "Leaf Mold",
        "sensor_conditions": {
            "air_humidity_min": 85,
            "air_temp_range": (22, 26),
            "poor_ventilation": True
        },
        "visual_markers": ["yellow_spots_upper", "gray_mold_underside"],
        "risk_weights": {
            "humidity": 0.6,
            "temperature": 0.25,
            "ventilation": 0.15
        },
        "corrective_actions": [
            "Increase ventilation immediately",
            "Reduce humidity if in greenhouse",
            "Space plants wider",
            "Remove infected leaves",
            "Use drip irrigation only"
        ],
        "root_cause": "Very high humidity (85%+) + poor air circulation",
        "prevention": "Ensure good ventilation, control humidity"
    },
    
    "Tomato___Target_Spot": {
        "name": "Target Spot",
        "sensor_conditions": {
            "air_humidity_min": 80,
            "air_temp_range": (18, 28),
            "prolonged_leaf_wetness": True
        },
        "visual_markers": ["concentric_rings", "target_pattern"],
        "risk_weights": {
            "humidity": 0.4,
            "temperature": 0.3,
            "leaf_wetness": 0.3
        },
        "corrective_actions": [
            "Remove infected leaves",
            "Improve air circulation",
            "Avoid overhead irrigation",
            "Apply fungicide if necessary"
        ],
        "root_cause": "High humidity + prolonged leaf wetness",
        "prevention": "Drip irrigation, good spacing, remove debris"
    },
    
    "Tomato___Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus",
        "sensor_conditions": {
            # Viral - not directly sensor-related but spread by contact
            "mechanical_transmission": True
        },
        "visual_markers": ["mosaic_pattern", "leaf_distortion", "stunted_growth"],
        "risk_weights": {
            "contact": 1.0  # Spread by tools, hands, etc.
        },
        "corrective_actions": [
            "Remove infected plants immediately",
            "Disinfect tools between plants (10% bleach)",
            "Wash hands before handling plants",
            "Do not smoke near plants (tobacco can carry virus)",
            "Plant resistant varieties in future"
        ],
        "root_cause": "Viral infection spread by mechanical contact",
        "prevention": "Use resistant varieties, practice strict hygiene"
    },
    
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "name": "Yellow Leaf Curl Virus",
        "sensor_conditions": {
            "vector_present": "whitefly",
            "air_temp_range": (25, 30)  # Whiteflies thrive in warm conditions
        },
        "visual_markers": ["yellow_curling", "stunted_growth", "upward_curl"],
        "risk_weights": {
            "vector": 0.7,
            "temperature": 0.3
        },
        "corrective_actions": [
            "Control whitefly population (yellow sticky traps)",
            "Remove infected plants to prevent spread",
            "Use insecticidal soap or neem oil",
            "Plant resistant varieties",
            "Use reflective mulch to deter whiteflies"
        ],
        "root_cause": "Whitefly-transmitted virus",
        "prevention": "Control whitefly population, use resistant varieties"
    },
    
    "Tomato___Spider_mites_Two_spotted_spider_mite": {
        "name": "Two-Spotted Spider Mite",
        "sensor_conditions": {
            "air_humidity_max": 60,  # Thrive in DRY conditions
            "air_temp_range": (27, 35),
            "drought_stress": True
        },
        "visual_markers": ["stippling", "webbing", "yellow_leaves"],
        "risk_weights": {
            "humidity": 0.4,  # LOW humidity favors mites
            "temperature": 0.4,
            "water_stress": 0.2
        },
        "corrective_actions": [
            "Increase humidity (mist plants)",
            "Ensure adequate watering",
            "Spray with water to dislodge mites",
            "Apply neem oil or insecticidal soap",
            "Introduce predatory mites if severe"
        ],
        "root_cause": "Hot, dry conditions + water stress favor spider mites",
        "prevention": "Maintain adequate moisture, avoid drought stress"
    },
    
    "Tomato___healthy": {
        "name": "Healthy",
        "sensor_conditions": {
            "air_humidity_range": (50, 70),
            "air_temp_range": (18, 27),
            "soil_moisture": "optimal",
            "good_airflow": True
        },
        "visual_markers": ["green_leaves", "no_spots", "vigorous_growth"],
        "risk_weights": {},
        "corrective_actions": [
            "Maintain current practices",
            "Continue monitoring",
            "Keep soil consistently moist",
            "Ensure good air circulation"
        ],
        "root_cause": "Optimal growing conditions maintained",
        "prevention": "Continue current care routine"
    }
}

# Simplified access functions
def get_disease_signature(disease_name):
    """Get signature for a specific disease"""
    return DISEASE_SIGNATURES.get(disease_name, None)

def get_all_diseases():
    """Get list of all disease names"""
    return list(DISEASE_SIGNATURES.keys())

def get_disease_display_name(class_name):
    """Convert class name to display name"""
    sig = DISEASE_SIGNATURES.get(class_name)
    return sig['name'] if sig else class_name.replace('Tomato___', '').replace('_', ' ')