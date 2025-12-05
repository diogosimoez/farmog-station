# Model Files

## ⚠️ Large Model Files Not Included in Git

Due to GitHub's file size limitations, the trained model files (`.h5` files) are **not included** in this repository.

### Required Model Files:

To run the FarmOG Station app, you need:

1. **`farmog_resnet50v2_classifier.h5`** (220 MB)
   - Main production model with 98.74% accuracy
   - Required for: Streamlit app, fusion system

2. **`class_names.json`** ✅ (included)
   - Disease class mapping

3. **`resnet50v2_metadata.json`** ✅ (included)
   - Training metadata

## How to Get the Models:

### Option 1: Download from Cloud Storage
**[Add your Google Drive/Dropbox link here]**

### Option 2: Train Yourself
Run the training notebooks in order:
```bash
# Navigate to notebooks folder
cd notebooks

# Train ResNet50V2 (best accuracy)
jupyter notebook 04_train_resnet50v2_FIXED.ipynb

# Or train EfficientNetB0
jupyter notebook 03_train_efficientnet_FIXED.ipynb

# Or train MobileNetV2
jupyter notebook 02_train_mobilenetv2.ipynb
```

Training takes approximately:
- ResNet50V2: ~2 hours (GPU recommended)
- EfficientNetB0: ~1.5 hours
- MobileNetV2: ~1 hour

### Option 3: Contact the Author
Email: [Your email]

## Model Files Summary:

| File | Size | Status | Purpose |
|------|------|--------|---------|
| `farmog_resnet50v2_classifier.h5` | 220 MB | ❌ Not in repo | Production model |
| `farmog_efficientnet_classifier.h5` | 45 MB | ❌ Not in repo | Alternative model |
| `class_names.json` | <1 KB | ✅ Included | Class mapping |
| `resnet50v2_metadata.json` | <1 KB | ✅ Included | Training info |
| `efficientnet_metadata.json` | <1 KB | ✅ Included | Training info |
| `evaluation_report.json` | <1 KB | ✅ Included | Performance metrics |

## Metadata Files Included:

These small JSON files ARE included and contain:
- Model architecture details
- Training parameters
- Validation accuracy
- Per-class performance metrics

You can review these without downloading the large model files.

## After Downloading Models:

1. Place the `.h5` files in this directory (`notebooks/models/`)
2. Verify files:
```bash
ls -lh notebooks/models/*.h5
```
3. Run the app:
```bash
streamlit run app/app.py
```

## Need Help?

- Check `HOW_TO_DEMO.md` for detailed setup instructions
- See `QUICK_REFERENCE.md` for troubleshooting
- Open an issue on GitHub
