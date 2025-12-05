# 🌱 FarmOG Station
**Off-Grid Agricultural Intelligence System**

> Multi-sensor disease detection & crop monitoring for small farmers.
> Powered by AI. Runs anywhere. No internet required.

---

## 🎯 Mission

Help small farmers make data-driven decisions using:
- 📷 **Computer Vision** - Detect plant diseases from leaf images
- 📊 **Sensor Fusion** - Monitor soil, weather, and environmental conditions  
- 🤖 **AI Agents** - Cross-validate diagnosis & provide actionable recommendations
- 🔋 **Off-Grid** - Solar-powered, LoRa connectivity, edge AI

---

## 🏆 Project Highlights

- **98.74% accuracy**: Best-in-class ResNet50V2 model for disease detection
- **Multi-modal fusion**: Vision + sensors cross-validate for robust diagnosis
- **Early warning system**: Detect disease-favorable conditions before symptoms appear
- **Three detection modes**: Vision Only, Sensor Only, Full Fusion
- **Edge deployment**: Runs on Raspberry Pi (TensorFlow Lite optimized)
- **Real-world ready**: Designed for harsh farming environments with limited connectivity

---

## 🧠 Models

### 1. Disease Vision Classifier
**Three architectures trained and compared:**

| Model | Accuracy | Parameters | Best Use Case |
|-------|----------|------------|---------------|
| **ResNet50V2** | **98.74%** | 25M | Production (highest accuracy) |
| EfficientNetB0 | 93.37% | 5.3M | Balanced performance |
| MobileNetV2 | 90.05% | 3.5M | Edge devices (Raspberry Pi) |

- **Dataset**: 87K images, 10 tomato disease classes
- **Training**: Transfer learning with custom preprocessing per architecture
- **Deployment**: ResNet50V2 for web app, MobileNetV2 for edge (TFLite)
- **Inference**: <100ms (MobileNetV2 on Raspberry Pi 4)

### 2. Sensor Pattern Matcher
- **Input**: Air temp/humidity, soil moisture, rainfall, irrigation method
- **Output**: Disease risk scores (0-100%) + environmental diagnosis
- **Method**: Rule-based disease signatures with weighted scoring
- **Coverage**: 9 disease signatures + healthy baseline

### 3. Fusion System
- **Cross-validation**: Vision ↔ Sensor agreement with confidence weighting
- **Confidence scoring**: 0-100% with uncertainty quantification
- **Modes**:
  - **CONFIRMED**: Vision + Sensor agree (high confidence diagnosis)
  - **EARLY_WARNING**: Sensor alerts before visual symptoms
  - **CONFLICT**: Disagreement between modalities (needs review)
  - **LOW_CONFIDENCE**: Uncertain diagnosis

---

## 🚀 Quick Start

### Installation
```bash
# Clone repo
git clone https://github.com/diogosimoez/farmog-station.git
cd farmog-station

# Setup environment
conda create -n farmog python=3.10
conda activate farmog
pip install -r requirements.txt
```

### Run the App
```bash
# Option 1: Streamlit command
streamlit run app/app.py

# Option 2: Windows batch file
RUN_APP.bat
```

### Demo the System
The app has 3 detection modes:

1. **Vision Only**: Upload a plant image → Get disease diagnosis
2. **Sensor Only**: Input environmental data → Get risk assessment
3. **Vision + Sensor Fusion**: Both inputs → Cross-validated diagnosis

See `HOW_TO_DEMO.md` for detailed walkthrough

---

## 📊 System Architecture
```
┌─────────────────────────────────────────────┐
│         FARMOG STATION ECOSYSTEM            │
├─────────────────────────────────────────────┤
│                                             │
│  📷 Vision Input          📊 Sensor Input   │
│  (Plant images)           (Soil/Weather)    │
│         │                       │           │
│         ▼                       ▼           │
│  ┌─────────────┐        ┌─────────────┐    │
│  │ ResNet50V2  │        │ Disease     │    │
│  │ 98.74% Acc  │        │ Signatures  │    │
│  └─────────────┘        └─────────────┘    │
│         │                       │           │
│         │ Predictions      Risk Scores │   │
│         │ (0-100%)         (0-100%)    │   │
│         └───────┬───────────────┘           │
│                 ▼                           │
│         ┌───────────────┐                   │
│         │ FUSION ENGINE │                   │
│         │ Cross-validate│                   │
│         │ & Score       │                   │
│         └───────────────┘                   │
│                 │                           │
│                 ▼                           │
│    ┌────────────────────────┐              │
│    │ Final Diagnosis        │              │
│    │ • Disease detected     │              │
│    │ • Confidence (0-100%)  │              │
│    │ • Status (CONFIRMED/   │              │
│    │   EARLY_WARNING/etc)   │              │
│    │ • Root cause           │              │
│    │ • Corrective actions   │              │
│    │ • Prevention tips      │              │
│    └────────────────────────┘              │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎓 Academic Project

**Course**: Data Science & Machine Learning  
**Focus**: Multi-modal learning, computer vision, IoT sensor fusion  
**Duration**: 2 weeks 
**Status**: MVP complete ✅

---

## 🛠️ Tech Stack

- **ML/AI**: TensorFlow, Keras, scikit-learn
- **Vision**: MobileNetV2, TensorFlow Lite
- **Data**: Pandas, NumPy
- **Viz**: Matplotlib, Seaborn, Plotly
- **App**: Streamlit
- **Deploy**: Raspberry Pi 4, Docker (planned)

---

## 📁 Project Structure
```
farmog-station/
├── app/
│   └── app.py                      # Streamlit dashboard (3 detection modes)
├── src/
│   ├── fusion_engine.py            # Multi-modal fusion logic
│   ├── disease_siganture.py        # Disease signatures database
│   ├── sensor_matcher.py           # Environmental risk scoring
│   └── utils.py                    # Helper functions
├── notebooks/
│   ├── 01_EDA_diseases_model.ipynb            # Dataset exploration
│   ├── 03_train_efficientnet_FIXED.ipynb     # EfficientNet training
│   ├── 04_train_resnet50v2_FIXED.ipynb       # ResNet50V2 training
│   ├── 05_model_comparison_final.ipynb       # Model comparison
│   ├── 06_fusion_system_demo.ipynb           # Fusion testing
│   ├── 07_model_evaluation.ipynb             # Metrics & confusion matrix
│   ├── 08_convert_to_tflite.ipynb            # Edge deployment prep
│   ├── models/
│   │   ├── farmog_resnet50v2_classifier.h5   # Main production model
│   │   ├── class_names.json                  # Disease class mapping
│   │   ├── resnet50v2_metadata.json          # Training metadata
│   │   └── evaluation_report.json            # Performance metrics
│   └── docs/                                 # Generated visualizations
├── data/
│   └── raw/                        # Dataset (87K images, 10 classes)
├── README.md
├── requirements.txt
└── RUN_APP.bat                     # Windows launcher
```

---

## 🌍 Real-World Deployment Plan

### Phase 1: Academic MVP (2 weeks) ✅
- Vision model trained
- Sensor fusion logic
- Demo dashboard

### Phase 2: Hardware Prototype (Month 1-3)
- Raspberry Pi integration
- LoRa communication
- Solar power system

### Phase 3: Field Testing (Month 4-6)
- Deploy 5-10 beta units
- Real farmer feedback
- Model refinement

### Phase 4: Product Launch (Month 6-12)
- Production hardware
- Open-source documentation
- Community building

---

## 🤝 Contributing

This is an open-source project. Contributions welcome!

---

## 📄 License

MIT License - Free to use, modify, distribute

---

## 👨‍💻 Author

Diogo Simoes 
Data Scientist | Agricultural Technology Enthusiast  
[GitHub](https://github.com/diogosimoez) | [LinkedIn](https://linkedin.com/in/diogosimoes86)

---

## 📊 Key Results

### Model Performance
- **ResNet50V2**: 98.74% accuracy (production model)
- **Top-3 Accuracy**: 99.96% (near perfect)
- **Confusion Matrix**: Available in `notebooks/docs/confusion_matrix.png`
- **Per-disease Metrics**: F1-scores 0.96-1.00 across all classes

### Detection Capabilities
- **10 Disease Classes**: 9 tomato diseases + healthy baseline
- **Vision Mode**: Single image → instant diagnosis
- **Sensor Mode**: Environmental risk assessment without images
- **Fusion Mode**: Cross-validated diagnosis with <5% false positive rate

### Visualizations
All training results and comparisons available in `notebooks/docs/`:
- Model comparison charts
- Training curves (ResNet50V2, EfficientNet)
- Confusion matrix
- Per-disease performance metrics

---

**FarmOG Station** - *Bringing precision agriculture to off-grid farmers worldwide* 🌍🌱
