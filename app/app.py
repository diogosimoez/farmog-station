"""
FarmOG Station - Streamlit Dashboard
Multi-modal disease detection system
"""

import streamlit as st
import numpy as np
from PIL import Image
import json
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import tensorflow as tf
from src.fusion_engine import FarmOGFusionEngine
from src.disease_siganture import get_disease_display_name

# Page config
st.set_page_config(
    page_title="FarmOG Station",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #2E7D32; font-weight: bold;}
    .sub-header {font-size: 1.5rem; color: #558B2F;}
    .metric-box {padding: 20px; border-radius: 10px; background: #E8F5E9;}
    .warning-box {padding: 20px; border-radius: 10px; background: #FFF3E0;}
    .danger-box {padding: 20px; border-radius: 10px; background: #FFEBEE;}
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('notebooks/models/farmog_resnet50v2_classifier.h5')
    with open('notebooks/models/class_names.json', 'r') as f:
        class_names = json.load(f)
    return model, class_names

# Initialize
try:
    model, class_names = load_model()
    fusion_engine = FarmOGFusionEngine(model, class_names)
    st.success("✅ Model loaded successfully")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

# Header
st.markdown('<p class="main-header">🌱 FarmOG Station</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Disease Detection System</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    mode = st.radio("Detection Mode", ["Vision + Sensor Fusion", "Vision Only", "Sensor Only"])
    st.markdown("---")
    st.info("Upload a plant image and enter sensor data for comprehensive diagnosis")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    if mode != "Sensor Only":
        st.subheader("📷 Vision Input")
        uploaded_file = st.file_uploader("Upload plant image", type=['jpg', 'jpeg', 'png'])
    else:
        uploaded_file = None

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Preprocess
        img_resized = image.resize((224, 224))
        img_array = np.array(img_resized)
        from tensorflow.keras.applications.resnet_v2 import preprocess_input
        img_array = preprocess_input(img_array)

        # Predict
        vision_results = fusion_engine.predict_from_image(img_array)

        st.success("✅ Image analyzed")

        if mode == "Vision Only":
            st.markdown("---")
            st.subheader("🔬 Vision Analysis Results")

            top_preds = fusion_engine.get_top_vision_predictions(vision_results, top_n=3)
            top_disease, top_conf = top_preds[0]

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Detected Disease", get_disease_display_name(top_disease))
            with col2:
                st.metric("Confidence", f"{top_conf*100:.1f}%")

            st.markdown("**All Predictions:**")
            for disease, conf in top_preds:
                st.write(f"- {get_disease_display_name(disease)}: {conf*100:.1f}%")

            # Get recommendations
            from src.disease_siganture import DISEASE_SIGNATURES
            if top_disease in DISEASE_SIGNATURES:
                disease_info = DISEASE_SIGNATURES[top_disease]

                st.markdown("### 📊 Typical Environmental Conditions")
                conditions = disease_info['sensor_conditions']
                if 'air_humidity_min' in conditions:
                    st.write(f"- Humidity: >{conditions['air_humidity_min']}%")
                if 'air_temp_range' in conditions:
                    st.write(f"- Temperature: {conditions['air_temp_range'][0]}-{conditions['air_temp_range'][1]}°C")
                if 'soil_moisture' in conditions:
                    st.write(f"- Soil Moisture: {conditions['soil_moisture']}")

                st.markdown("### 🛠️ Recommended Actions")
                for action in disease_info['corrective_actions']:
                    st.write(f"- {action}")
                st.info(f"**Root Cause:** {disease_info['root_cause']}")
        else:
            st.markdown("**Top Predictions:**")
            top_preds = fusion_engine.get_top_vision_predictions(vision_results, top_n=3)
            for disease, conf in top_preds:
                st.write(f"- {get_disease_display_name(disease)}: {conf*100:.1f}%")

with col2:
    if mode != "Vision Only":
        st.subheader("📊 Sensor Input")

        with st.form("sensor_form"):
            air_temp = st.slider("Air Temperature (°C)", 10, 40, 25)
            air_humidity = st.slider("Air Humidity (%)", 30, 100, 60)
            soil_moisture = st.slider("Soil Moisture (%)", 20, 90, 50)
            rainfall = st.number_input("Rainfall (24h, mm)", 0.0, 50.0, 0.0)
            irrigation = st.selectbox("Irrigation Method", ["drip", "overhead"])

            submit = st.form_submit_button("Analyze Conditions")
    else:
        submit = False

    if submit:
        sensor_data = {
            'air_temp': air_temp,
            'air_humidity': air_humidity,
            'soil_moisture': soil_moisture,
            'rainfall_24h': rainfall,
            'irrigation_method': irrigation
        }
        st.success("✅ Sensor data processed")

        if mode == "Sensor Only":
            st.markdown("---")
            st.subheader("🔬 Sensor Analysis Results")

            from src.sensor_matcher import get_all_disease_risks, get_top_risks
            risks = get_top_risks(sensor_data, top_n=3)

            if risks and risks[0][1] > 20:
                top_disease, top_risk = risks[0]

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Highest Risk Disease", get_disease_display_name(top_disease))
                with col_b:
                    st.metric("Risk Score", f"{top_risk:.1f}%")

                st.markdown("**Risk Assessment:**")
                for disease, risk in risks:
                    if risk > 20:
                        st.write(f"- {get_disease_display_name(disease)}: {risk:.1f}% risk")

                # Show sample image if disease detected
                from pathlib import Path
                import random
                disease_folder = Path("data/raw/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid") / top_disease
                if disease_folder.exists():
                    images = list(disease_folder.glob("*.jpg"))
                    if images:
                        sample_img = Image.open(random.choice(images))
                        st.image(sample_img, caption=f"Example of {get_disease_display_name(top_disease)}", use_container_width=True)

                from src.disease_siganture import DISEASE_SIGNATURES
                if top_disease in DISEASE_SIGNATURES:
                    disease_info = DISEASE_SIGNATURES[top_disease]
                    st.markdown("### 🛠️ Recommended Actions")
                    for action in disease_info['corrective_actions']:
                        st.write(f"- {action}")
                    st.info(f"**Root Cause:** {disease_info['root_cause']}")
            else:
                st.success("✅ Conditions appear favorable - low disease risk")

# Fusion Diagnosis
if uploaded_file and submit and mode == "Vision + Sensor Fusion":
    st.markdown("---")
    st.header("🔬 Diagnosis Results")

    diagnosis = fusion_engine.cross_validate(vision_results, sensor_data)

    # Status indicator
    status = diagnosis['status']
    if status == "CONFIRMED":
        st.markdown('<div class="danger-box"><h3>⚠️ CONFIRMED DISEASE DETECTED</h3></div>', unsafe_allow_html=True)
    elif status == "EARLY_WARNING":
        st.markdown('<div class="warning-box"><h3>⚠️ EARLY WARNING</h3></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-box"><h3>✅ Analysis Complete</h3></div>', unsafe_allow_html=True)

    # Main diagnosis
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Diagnosed Disease", get_disease_display_name(diagnosis['final_diagnosis']))
    with col2:
        st.metric("Confidence", f"{diagnosis['confidence']:.1f}%")
    with col3:
        st.metric("Status", status)

    # Detailed results
    st.subheader("📋 Detailed Analysis")

    if diagnosis['confirmed']:
        item = diagnosis['confirmed'][0]
        st.error(f"**Disease:** {item['display_name']}")
        st.write(f"**Root Cause:** {item['root_cause']}")
        st.write(f"**Confidence:** Vision {item['vision_confidence']:.1f}% + Sensor {item['sensor_risk']:.1f}%")

        st.markdown("### 🛠️ Corrective Actions")
        for action in item['corrective_actions']:
            st.write(f"- {action}")

        st.markdown("### 🛡️ Prevention")
        st.info(item['prevention'])

    elif diagnosis['early_warnings']:
        item = diagnosis['early_warnings'][0]
        st.warning(f"**{item['alert']}**")
        st.write(f"**Risk Score:** {item['risk_score']:.1f}%")

        st.markdown("### 🛡️ Preventive Actions")
        for action in item['corrective_actions']:
            st.write(f"- {action}")

    # Vision vs Sensor
    tab1, tab2 = st.tabs(["Vision Analysis", "Sensor Analysis"])

    with tab1:
        for pred in diagnosis['vision_predictions']:
            st.write(f"- {pred['display_name']}: {pred['confidence']:.1f}%")

    with tab2:
        for pred in diagnosis['sensor_predictions']:
            st.write(f"- {pred['display_name']}: {pred['risk_score']:.1f}% risk")

# Footer
st.markdown("---")
st.markdown("**FarmOG Station** | Off-Grid Agricultural Intelligence System")
