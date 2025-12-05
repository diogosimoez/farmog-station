"""
FarmOG Station - Multi-Modal Fusion Engine
==========================================
Cross-validates vision model predictions with sensor pattern matching
"""

import numpy as np
from src.disease_siganture import DISEASE_SIGNATURES, get_disease_display_name
from src.sensor_matcher import calculate_disease_risk, get_all_disease_risks

class FarmOGFusionEngine:
    """
    Multi-modal disease detection system that fuses:
    1. Computer vision (CNN predictions from leaf images)
    2. Sensor pattern matching (environmental conditions)
    """
    
    def __init__(self, vision_model=None, class_names=None):
        """
        Initialize fusion engine
        
        Args:
            vision_model: Trained Keras model (optional, can load later)
            class_names: Dict mapping indices to class names
        """
        self.vision_model = vision_model
        self.class_names = class_names
        
    def predict_from_image(self, image):
        """
        Get vision model predictions from image
        
        Args:
            image: preprocessed image array (224x224x3, normalized)
        
        Returns:
            dict: {class_name: confidence, ...}
        """
        if self.vision_model is None:
            raise ValueError("Vision model not loaded!")
        
        # Get predictions
        predictions = self.vision_model.predict(np.expand_dims(image, axis=0), verbose=0)[0]
        
        # Map to class names
        results = {}
        for idx, prob in enumerate(predictions):
            class_name = self.class_names.get(str(idx), f"Class_{idx}")
            results[class_name] = float(prob)
        
        return results
    
    def get_top_vision_predictions(self, vision_results, top_n=3, threshold=0.1):
        """
        Filter and sort vision predictions
        
        Args:
            vision_results: dict from predict_from_image
            top_n: number of top predictions to return
            threshold: minimum confidence to consider
        
        Returns:
            list of tuples: [(class_name, confidence), ...]
        """
        filtered = [(k, v) for k, v in vision_results.items() if v >= threshold]
        sorted_preds = sorted(filtered, key=lambda x: x[1], reverse=True)
        return sorted_preds[:top_n]
    
    def cross_validate(self, vision_results, sensor_data):
        """
        CORE FUSION LOGIC - Cross-validate vision and sensor predictions
        
        Args:
            vision_results: dict from predict_from_image
            sensor_data: dict with sensor readings
        
        Returns:
            dict with comprehensive diagnosis
        """
        # Get top vision predictions
        top_vision = self.get_top_vision_predictions(vision_results, top_n=3)
        
        # Get sensor risk scores
        sensor_risks = get_all_disease_risks(sensor_data)
        top_sensors = sorted(sensor_risks.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Find matches and conflicts
        diagnosis = {
            "vision_predictions": [],
            "sensor_predictions": [],
            "confirmed": [],
            "early_warnings": [],
            "conflicts": [],
            "final_diagnosis": None,
            "confidence": 0.0,
            "status": "UNKNOWN"
        }
        
        # Format vision predictions
        for disease, confidence in top_vision:
            diagnosis["vision_predictions"].append({
                "disease": disease,
                "display_name": get_disease_display_name(disease),
                "confidence": confidence * 100,
                "source": "vision"
            })
        
        # Format sensor predictions
        for disease, risk in top_sensors:
            if risk > 20:  # Only include significant risks
                diagnosis["sensor_predictions"].append({
                    "disease": disease,
                    "display_name": get_disease_display_name(disease),
                    "risk_score": risk,
                    "source": "sensor"
                })
        
        # CROSS-VALIDATION LOGIC
        
        # Case 1: CONFIRMED - Both vision and sensor agree
        for v_disease, v_conf in top_vision:
            for s_disease, s_risk in top_sensors:
                if v_disease == s_disease and v_conf > 0.5 and s_risk > 50:
                    # Strong agreement!
                    combined_confidence = min(95, (v_conf * 100 + s_risk) / 2)
                    
                    diagnosis["confirmed"].append({
                        "disease": v_disease,
                        "display_name": get_disease_display_name(v_disease),
                        "confidence": combined_confidence,
                        "vision_confidence": v_conf * 100,
                        "sensor_risk": s_risk,
                        "status": "CONFIRMED",
                        "validation": "✅ Vision + Sensor Agreement",
                        "corrective_actions": DISEASE_SIGNATURES[v_disease]["corrective_actions"],
                        "root_cause": DISEASE_SIGNATURES[v_disease]["root_cause"],
                        "prevention": DISEASE_SIGNATURES[v_disease]["prevention"]
                    })
                    
                    # Set as final diagnosis
                    if diagnosis["final_diagnosis"] is None:
                        diagnosis["final_diagnosis"] = v_disease
                        diagnosis["confidence"] = combined_confidence
                        diagnosis["status"] = "CONFIRMED"
        
        # Case 2: EARLY WARNING - High sensor risk but no visual symptoms (or low confidence)
        if len(diagnosis["confirmed"]) == 0:
            top_vision_disease = top_vision[0][0] if top_vision else "Tomato___healthy"
            top_vision_conf = top_vision[0][1] if top_vision else 1.0
            
            for s_disease, s_risk in top_sensors:
                # High sensor risk but vision doesn't strongly agree
                if s_risk > 60 and (top_vision_disease == "Tomato___healthy" or 
                                   (s_disease != top_vision_disease and top_vision_conf < 0.7)):
                    
                    diagnosis["early_warnings"].append({
                        "disease": s_disease,
                        "display_name": get_disease_display_name(s_disease),
                        "risk_score": s_risk,
                        "status": "EARLY_WARNING",
                        "alert": f"⚠️ Conditions favor {get_disease_display_name(s_disease)} - symptoms may appear in 24-48h",
                        "corrective_actions": DISEASE_SIGNATURES[s_disease]["corrective_actions"],
                        "preventive_note": "Act now to prevent disease development"
                    })
                    
                    # Set as final diagnosis if no confirmed cases
                    if diagnosis["final_diagnosis"] is None and s_risk > 70:
                        diagnosis["final_diagnosis"] = s_disease
                        diagnosis["confidence"] = s_risk
                        diagnosis["status"] = "EARLY_WARNING"
        
        # Case 3: CONFLICT - Vision sees one thing, sensors say another
        if len(diagnosis["confirmed"]) == 0 and len(diagnosis["early_warnings"]) == 0:
            top_vision_disease, top_vision_conf = top_vision[0] if top_vision else ("Unknown", 0)
            top_sensor_disease, top_sensor_risk = top_sensors[0] if top_sensors else ("Unknown", 0)
            
            if (top_vision_disease != top_sensor_disease and 
                top_vision_conf > 0.5 and top_sensor_risk > 50):
                
                diagnosis["conflicts"].append({
                    "vision_says": top_vision_disease,
                    "vision_display": get_disease_display_name(top_vision_disease),
                    "vision_confidence": top_vision_conf * 100,
                    "sensor_says": top_sensor_disease,
                    "sensor_display": get_disease_display_name(top_sensor_disease),
                    "sensor_risk": top_sensor_risk,
                    "status": "CONFLICT",
                    "alert": "⚠️ Vision and sensor predictions disagree - manual review recommended",
                    "possible_causes": [
                        "Multiple diseases present simultaneously",
                        "Disease in early/transitional stage",
                        "Sensor calibration may need adjustment",
                        "Unusual environmental conditions"
                    ],
                    "next_steps": [
                        "Take additional photos from different angles",
                        "Verify sensor calibration",
                        "Monitor closely for 24-48 hours",
                        "Consider expert consultation"
                    ]
                })
                
                # Use vision if higher confidence, otherwise sensor
                if top_vision_conf > (top_sensor_risk / 100):
                    diagnosis["final_diagnosis"] = top_vision_disease
                    diagnosis["confidence"] = top_vision_conf * 100 * 0.7  # Reduce due to conflict
                    diagnosis["status"] = "NEEDS_REVIEW"
                else:
                    diagnosis["final_diagnosis"] = top_sensor_disease
                    diagnosis["confidence"] = top_sensor_risk * 0.7
                    diagnosis["status"] = "NEEDS_REVIEW"
        
        # Case 4: Low confidence all around
        if diagnosis["final_diagnosis"] is None:
            # Default to vision's top prediction or healthy
            if top_vision and top_vision[0][1] > 0.3:
                diagnosis["final_diagnosis"] = top_vision[0][0]
                diagnosis["confidence"] = top_vision[0][1] * 100
                diagnosis["status"] = "LOW_CONFIDENCE"
            else:
                diagnosis["final_diagnosis"] = "Tomato___healthy"
                diagnosis["confidence"] = 50.0
                diagnosis["status"] = "UNCERTAIN"
        
        return diagnosis
    
    def generate_report(self, diagnosis):
        """
        Generate human-readable report from diagnosis
        
        Returns:
            str: formatted report
        """
        report = []
        report.append("="*60)
        report.append("🌱 FARMOG STATION - DIAGNOSIS REPORT")
        report.append("="*60)
        report.append("")
        
        # Final diagnosis
        final_disease = diagnosis["final_diagnosis"]
        final_name = get_disease_display_name(final_disease)
        confidence = diagnosis["confidence"]
        status = diagnosis["status"]
        
        status_emoji = {
            "CONFIRMED": "✅",
            "EARLY_WARNING": "⚠️",
            "NEEDS_REVIEW": "🔍",
            "LOW_CONFIDENCE": "❓",
            "UNCERTAIN": "❓"
        }
        
        report.append(f"{status_emoji.get(status, '•')} DIAGNOSIS: {final_name}")
        report.append(f"   Confidence: {confidence:.1f}%")
        report.append(f"   Status: {status}")
        report.append("")
        
        # Vision predictions
        if diagnosis["vision_predictions"]:
            report.append("📷 VISION ANALYSIS:")
            for pred in diagnosis["vision_predictions"][:3]:
                report.append(f"   • {pred['display_name']}: {pred['confidence']:.1f}%")
            report.append("")
        
        # Sensor predictions
        if diagnosis["sensor_predictions"]:
            report.append("📊 SENSOR ANALYSIS:")
            for pred in diagnosis["sensor_predictions"][:3]:
                report.append(f"   • {pred['display_name']}: {pred['risk_score']:.1f}% risk")
            report.append("")
        
        # Confirmed cases
        if diagnosis["confirmed"]:
            report.append("✅ CONFIRMED DIAGNOSIS:")
            for item in diagnosis["confirmed"]:
                report.append(f"   Disease: {item['display_name']}")
                report.append(f"   {item['validation']}")
                report.append(f"   Root Cause: {item['root_cause']}")
                report.append("")
                report.append("   🛠️ CORRECTIVE ACTIONS:")
                for action in item['corrective_actions']:
                    report.append(f"      → {action}")
            report.append("")
        
        # Early warnings
        if diagnosis["early_warnings"]:
            report.append("⚠️ EARLY WARNINGS:")
            for item in diagnosis["early_warnings"]:
                report.append(f"   {item['alert']}")
                report.append(f"   Risk Score: {item['risk_score']:.1f}%")
                report.append("")
                report.append("   🛡️ PREVENTIVE ACTIONS:")
                for action in item['corrective_actions']:
                    report.append(f"      → {action}")
            report.append("")
        
        # Conflicts
        if diagnosis["conflicts"]:
            report.append("🔍 CONFLICTS DETECTED:")
            for item in diagnosis["conflicts"]:
                report.append(f"   Vision: {item['vision_display']} ({item['vision_confidence']:.1f}%)")
                report.append(f"   Sensor: {item['sensor_display']} ({item['sensor_risk']:.1f}%)")
                report.append(f"   {item['alert']}")
                report.append("")
                report.append("   Possible causes:")
                for cause in item['possible_causes']:
                    report.append(f"      • {cause}")
            report.append("")
        
        report.append("="*60)
        
        return "\n".join(report)