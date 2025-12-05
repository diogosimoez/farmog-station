# 🎬 FarmOG Station - Demo Guide

## Quick Start

### Launch the App
```bash
# Option 1: Command line
streamlit run app/app.py

# Option 2: Windows
Double-click RUN_APP.bat
```

The app will open in your browser at `http://localhost:8501`

---

## Demo Scenario 1: Vision Only Mode

**Use Case:** Farmer spots suspicious leaf symptoms and wants instant diagnosis

### Steps:
1. **Select Mode:** Click "Vision Only" in the sidebar
2. **Upload Image:** Click "Browse files" and select a diseased leaf image
   - Sample location: `data/raw/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid/Tomato___Late_blight/`
3. **View Results:**
   - Disease name displayed
   - Confidence percentage
   - Top 3 predictions shown
   - Typical environmental conditions for this disease
   - Recommended corrective actions

### Expected Output:
```
Detected Disease: Late Blight
Confidence: 99.2%

Typical Environmental Conditions:
- Humidity: >80%
- Temperature: 15-25°C
- Soil Moisture: High

Recommended Actions:
- Remove infected leaves immediately
- Apply copper-based fungicide
- Improve air circulation
- Reduce overhead irrigation

Root Cause: Fungal pathogen (Phytophthora infestans)
```

### Good Test Images:
- **Late Blight:** Shows dark, water-soaked lesions
- **Early Blight:** Shows concentric ring patterns
- **Bacterial Spot:** Shows small dark spots
- **Healthy:** Should correctly identify as healthy

---

## Demo Scenario 2: Sensor Only Mode

**Use Case:** Farmer monitors environmental conditions to assess disease risk before symptoms appear

### Steps:
1. **Select Mode:** Click "Sensor Only" in the sidebar
2. **Input Environmental Data:**
   - Air Temperature: 22°C (use slider)
   - Air Humidity: 85% (use slider)
   - Soil Moisture: 75% (use slider)
   - Rainfall (24h): 10mm (enter number)
   - Irrigation Method: Select "overhead"
3. **Click:** "Analyze Conditions" button
4. **View Results:**
   - Risk assessment displayed
   - Top disease risks with percentages
   - Sample image of the likely disease
   - Preventive actions

### Expected Output:
```
Highest Risk Disease: Late Blight
Risk Score: 87.5%

Risk Assessment:
- Late Blight: 87.5% risk
- Septoria Leaf Spot: 65.0% risk
- Leaf Mold: 60.0% risk

Recommended Actions:
- Reduce irrigation frequency
- Ensure good air circulation
- Monitor plants closely for early symptoms
- Consider preventive fungicide application

Root Cause: High humidity + moderate temperature create ideal conditions
```

### Test Scenarios:

**High Late Blight Risk:**
- Air Temp: 20°C
- Humidity: 85%
- Soil Moisture: 80%
- Rainfall: 15mm
- Irrigation: overhead

**High Early Blight Risk:**
- Air Temp: 28°C
- Humidity: 70%
- Soil Moisture: 60%
- Rainfall: 5mm
- Irrigation: drip

**Low Risk (Favorable Conditions):**
- Air Temp: 25°C
- Humidity: 50%
- Soil Moisture: 55%
- Rainfall: 0mm
- Irrigation: drip

---

## Demo Scenario 3: Vision + Sensor Fusion (The Main Feature!)

**Use Case:** Comprehensive diagnosis using both visual symptoms and environmental data

### Steps:
1. **Select Mode:** Click "Vision + Sensor Fusion" in the sidebar
2. **Upload Image:** Select a diseased leaf image
3. **Wait for Vision Analysis:** Top predictions appear
4. **Input Sensor Data:** Fill in all environmental parameters
5. **Click:** "Analyze Conditions" button
6. **View Fusion Results:** Comprehensive diagnosis appears

### Expected Output (CONFIRMED Case):
```
⚠️ CONFIRMED DISEASE DETECTED

Diagnosed Disease: Late Blight
Confidence: 95.3%
Status: CONFIRMED

Detailed Analysis:
Disease: Late Blight
Root Cause: Fungal pathogen (Phytophthora infestans)
Confidence: Vision 99.2% + Sensor 87.5%

Corrective Actions:
- Remove infected leaves immediately
- Apply copper-based fungicide
- Improve air circulation
- Reduce overhead irrigation
- Monitor neighboring plants

Prevention:
Maintain good air circulation, avoid overhead watering,
use resistant varieties, apply preventive fungicides
during high-risk periods
```

### Expected Output (EARLY WARNING Case):
```
⚠️ EARLY WARNING

Diagnosed Disease: Late Blight
Confidence: 68.5%
Status: EARLY_WARNING

ALERT: Conditions highly favorable for Late Blight development
Risk Score: 87.5%

Preventive Actions:
- Monitor plants closely for symptoms
- Reduce irrigation frequency
- Improve air circulation
- Consider preventive fungicide application
```

### Test Cases for Different Fusion Outcomes:

**CONFIRMED (Vision + Sensor Agree):**
- Image: Late Blight leaf
- Sensors: High humidity (85%), temp 20°C, high moisture
- Result: Both detect Late Blight → CONFIRMED

**EARLY_WARNING (Sensor alerts, Vision unclear):**
- Image: Healthy or early symptoms
- Sensors: High risk conditions (85% humidity, 20°C)
- Result: Environmental risk without clear visual confirmation

**CONFLICT (Disagreement):**
- Image: Shows one disease clearly
- Sensors: Indicate different disease conditions
- Result: System flags for review

**LOW_CONFIDENCE (Uncertain):**
- Image: Ambiguous symptoms
- Sensors: Moderate risk levels
- Result: Recommend additional monitoring

---

## Demo Flow for Presentations

### Recommended Order (5 minutes):

**1. Start Simple - Vision Only (1.5 min)**
- "Let's start by taking a photo of a diseased plant"
- Upload Late Blight image
- "The system instantly identifies Late Blight with 99% confidence"
- Point out recommended actions

**2. Add Context - Sensor Only (1.5 min)**
- "Now let's check environmental conditions"
- Input high humidity, moderate temp
- "Even without a photo, the system warns us about favorable conditions for disease"
- Show risk scores

**3. The Power - Fusion Mode (2 min)**
- "Now let's combine both for maximum confidence"
- Upload image + input matching sensor data
- "CONFIRMED diagnosis - both vision and sensors agree"
- Highlight comprehensive treatment plan
- "This cross-validation reduces false positives"

### Key Points to Emphasize:
- ✅ **Speed:** Instant results (<2 seconds)
- ✅ **Accuracy:** 98.74% vision model
- ✅ **Actionable:** Clear recommendations, not just diagnosis
- ✅ **Robust:** Multiple detection modes for different scenarios
- ✅ **Early Detection:** Sensor-only mode warns before symptoms

---

## Troubleshooting

### App Won't Start
```bash
# Check if Streamlit is installed
pip install streamlit

# Check if you're in the right directory
cd "path/to/FINAL PROJECT - FarmOG station"

# Try running directly
python -m streamlit run app/app.py
```

### Model Not Loading
- Verify path: `notebooks/models/farmog_resnet50v2_classifier.h5` exists
- Check TensorFlow installation: `pip install tensorflow`
- File size should be ~220MB

### Image Upload Issues
- Supported formats: JPG, JPEG, PNG
- Try with sample images from dataset first
- Check file isn't corrupted

### Sensor Results Don't Appear
- Make sure to click "Analyze Conditions" button
- Check that all sliders have been adjusted
- Verify mode is set to "Sensor Only" or "Fusion"

---

## Sample Data Locations

### For Vision Demo:
```
data/raw/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid/

Good examples:
- Tomato___Late_blight/
- Tomato___Early_blight/
- Tomato___Bacterial_spot/
- Tomato___healthy/
```

### For Sensor Demo:
Use the preset values from "Test Scenarios" above, or create your own based on disease signatures in `src/disease_siganture.py`

---

## Advanced Demo: Show the Code

### If Technical Audience:
1. Show `src/fusion_engine.py` - The brain of the system
2. Show `src/disease_siganture.py` - Disease knowledge database
3. Show confusion matrix: `notebooks/docs/confusion_matrix.png`
4. Show model comparison: `notebooks/docs/model_comparison_final.png`

### Key Code Highlights:
```python
# Fusion logic (fusion_engine.py)
if vision_confidence > 0.7 and sensor_risk > 50:
    if vision_disease == sensor_disease:
        status = "CONFIRMED"  # High confidence!
```

---

## Post-Demo Q&A Preparation

### Common Questions:

**Q: How fast is the inference?**
A: <2 seconds for complete diagnosis (vision + sensor fusion)

**Q: Can it work offline?**
A: Yes! Model runs locally, no internet required. Perfect for off-grid farms.

**Q: What if it's wrong?**
A: The system provides confidence scores. Low confidence results suggest consulting an expert.

**Q: Can it detect other crops?**
A: Currently trained on tomatoes. Architecture supports other crops with new training data.

**Q: How do you handle false positives?**
A: Fusion mode cross-validates vision and sensors. CONFLICT status flags uncertain cases.

**Q: Can farmers use this without technical knowledge?**
A: Absolutely! Just upload a photo or input sensor readings. System does the rest.

---

## Demo Success Checklist

Before your presentation:

- [ ] App launches successfully
- [ ] All 3 modes tested and working
- [ ] Sample images ready (bookmarked or copied to desktop)
- [ ] Sensor values written down for quick input
- [ ] Screenshots prepared as backup
- [ ] Confusion matrix image ready to show
- [ ] Model comparison chart ready to show
- [ ] Internet connection stable (if presenting remotely)
- [ ] Screen sharing tested
- [ ] Browser zoom level appropriate for audience

---

## Tips for Impactful Demo

### DO:
✅ Start with the problem ("Farmers lose 40% of crops to disease")
✅ Show real-world images (actual diseased plants)
✅ Emphasize speed and simplicity
✅ Point out confidence scores
✅ Highlight actionable recommendations
✅ Show the fusion advantage (cross-validation)

### DON'T:
❌ Get stuck in technical details upfront
❌ Apologize for loading times (they're fast!)
❌ Skip the "why it matters" context
❌ Forget to show the recommended actions
❌ Rush through the fusion mode (it's your differentiator!)

---

**Good luck with your demo! 🌱🚀**
