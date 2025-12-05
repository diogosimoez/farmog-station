# GitHub Setup Guide

## Files Excluded from Repository

Due to GitHub's 100MB file size limit and repository size constraints, the following are **excluded** via `.gitignore`:

### 1. Large Model Files (`.h5`, `.pkl`)
- `farmog_resnet50v2_classifier.h5` (220 MB)
- `farmog_efficientnet_classifier.h5` (45 MB)
- Other checkpoint files

**Why:** Too large for GitHub
**Solution:** See `notebooks/models/README.md` for download instructions

### 2. Dataset (`data/raw/`)
- 87,000 images (~2-3 GB total)

**Why:** Too large for GitHub
**Solution:**
- Download from: https://www.kaggle.com/datasets/arjuntejaswi/plant-village
- Place in `data/raw/`

### 3. Backup Files
- All `*_BACKUP.*` files

**Why:** Not needed in version control

---

## What IS Included in GitHub:

✅ **Source Code:**
- `app/app.py` - Streamlit application
- `src/` - All Python modules (fusion engine, sensor matcher, etc.)

✅ **Notebooks:**
- All `.ipynb` training and analysis notebooks
- Model comparison and evaluation notebooks

✅ **Documentation:**
- `README.md` - Main project documentation
- `HOW_TO_DEMO.md` - Demo instructions
- `PRESENTATION.md` - Presentation guide
- `RESULTS_SUMMARY.md` - Full results
- `QUICK_REFERENCE.md` - Quick reference card

✅ **Metadata Files:**
- `class_names.json` - Disease class mapping
- `*_metadata.json` - Training metadata
- `evaluation_report.json` - Performance metrics
- `requirements.txt` - Python dependencies

✅ **Visualizations:**
- All plots in `notebooks/docs/` (.png files)
- Training curves
- Confusion matrices
- Model comparisons

✅ **Presentation:**
- `FarmOG_Station_Presentation.pptx`

---

## Steps to Commit to GitHub:

### 1. Check what will be committed:
```bash
cd "C:\Users\diogo\IRONHACK\FINAL PROJECT - FarmOG station"
git status
```

### 2. Add all files (large files will be automatically excluded):
```bash
git add .
```

### 3. Verify large files are excluded:
```bash
# Check that .h5 files are NOT in the staged files
git status | grep -i ".h5"  # Should show nothing

# Check that data folder is excluded
git status | grep -i "data/raw"  # Should show nothing
```

### 4. Create commit:
```bash
git commit -m "FarmOG Station - Multi-Modal AI Disease Detection System

- 98.74% accuracy with ResNet50V2
- Three model architectures trained and compared
- Multi-modal fusion (vision + sensors)
- Complete documentation and presentation
- TensorFlow Lite ready for edge deployment

Note: Large model files (.h5) excluded - see notebooks/models/README.md"
```

### 5. Add remote and push:
```bash
# Add your GitHub repository
git remote add origin https://github.com/diogosimoez/farmog-station.git

# Push to GitHub
git push -u origin main
```

---

## If Git Complains About Large Files:

### Problem: "File is larger than 100MB"

**Solution 1: Remove from staging**
```bash
git rm --cached path/to/large/file.h5
git commit -m "Remove large file"
```

**Solution 2: Remove from history (if already committed)**
```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove large files from history
git filter-repo --path-glob '*.h5' --invert-paths
git filter-repo --path-glob 'data/raw/*' --invert-paths
```

### Problem: "Repository size exceeds GitHub limit"

**Solution: Use Git LFS (Large File Storage)**
```bash
# Install Git LFS
git lfs install

# Track large files (if you want to include them)
git lfs track "*.h5"
git lfs track "*.pkl"
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

**Note:** Git LFS has storage limits on free accounts (1GB storage, 1GB bandwidth/month)

---

## Recommended: Host Models Externally

### Option 1: Google Drive
1. Upload model files to Google Drive
2. Get shareable link
3. Add link to `notebooks/models/README.md`

### Option 2: Hugging Face Model Hub
```bash
# Install huggingface_hub
pip install huggingface_hub

# Upload model
huggingface-cli upload your-username/farmog-station notebooks/models/farmog_resnet50v2_classifier.h5
```

### Option 3: GitHub Releases
1. Create a release in your GitHub repo
2. Attach model files as release assets
3. Free up to 2GB per file

---

## Final Repository Structure on GitHub:

```
farmog-station/
├── .gitignore                    ✅ Updated
├── README.md                     ✅
├── requirements.txt              ✅
├── app/
│   └── app.py                    ✅
├── src/
│   ├── fusion_engine.py          ✅
│   ├── disease_siganture.py      ✅
│   ├── sensor_matcher.py         ✅
│   └── utils.py                  ✅
├── notebooks/
│   ├── *.ipynb                   ✅ All notebooks
│   ├── models/
│   │   ├── *.h5                  ❌ EXCLUDED
│   │   ├── *.json                ✅ Metadata only
│   │   └── README.md             ✅ Instructions
│   └── docs/
│       └── *.png                 ✅ Visualizations
├── data/
│   └── raw/                      ❌ EXCLUDED
├── PRESENTATION.md               ✅
├── HOW_TO_DEMO.md               ✅
├── RESULTS_SUMMARY.md           ✅
└── FarmOG_Station_Presentation.pptx  ✅
```

---

## Checklist Before Pushing:

- [ ] `.gitignore` is properly configured
- [ ] Large files (.h5, data/) are excluded
- [ ] `notebooks/models/README.md` explains where to get models
- [ ] All documentation is up to date
- [ ] `requirements.txt` includes all dependencies
- [ ] README.md has clear setup instructions
- [ ] Git status shows no unwanted large files

---

## After Pushing to GitHub:

1. ✅ Add model download link to `notebooks/models/README.md`
2. ✅ Update main `README.md` with GitHub repo link
3. ✅ Create a Release with model files attached (optional)
4. ✅ Add topics/tags to GitHub repo: `machine-learning`, `agriculture`, `computer-vision`, `tensorflow`
5. ✅ Add a nice cover image to README

---

## Need Help?

- GitHub Docs: https://docs.github.com/en/repositories/working-with-files/managing-large-files
- Git LFS: https://git-lfs.github.com/
- Contact: [Your email]
