# Unsupervised Image CAPTCHA

This project implements an **unsupervised image-based CAPTCHA** system.  
It extracts features from images using **ResNet18**, clusters them with **KMeans**, and presents an interactive **PyGame-based CAPTCHA** for users to select images belonging to a target cluster.

---


## Overview

The system generates CAPTCHAs automatically by clustering similar images.  
The process is fully **unsupervised**, meaning no manual labeling is required. Users are asked to select all images that belong to a target cluster from a grid. Feedback is given immediately on correct, incorrect, and missed selections.

---

## Project Structure

```text
captcha/
│
├── images/                 # Dataset images
├── extract_features.py     # Extracts embeddings from images
├── cluster_images.py       # Runs KMeans clustering
├── generate_captcha.py     # Builds one CAPTCHA challenge
├── captcha_pygame.py       # PyGame visual CAPTCHA interface
└── features.npy            # Saved image feature vectors
└── filenames.npy           # Filenames corresponding to features
└── labels.npy              # Cluster labels for each image
```

## Setup & Installation

Clone the repository:

```
git clone <your-repo-url>
cd captcha
```

Create a virtual environment (recommended):
```
python -m venv venv
# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

Install dependencies:
```python
pip install torch torchvision pygame numpy pillow scikit-learn
```

Make sure your images are inside the images/ folder.

## Usage
1. Extract Features
```
python extract_features.py
```
Extracts 512-dimensional ResNet18 features for all images.

**saves:** 
```
features.npy and filenames.npy
```

2. Cluster Images
```
python cluster_images.py
```

Runs KMeans clustering on extracted features.

Saves:
```
labels.npy → cluster index for each image
```

3. Generate CAPTCHA Data (Logic Only)

``` python
from generate_captcha import generate_captcha

captcha_data = generate_captcha()
print(captcha_data)
```

Returns a dictionary:
```
{
    "target_cluster": 2,
    "images": ["img1.png", "img2.png", ...],
    "answers": [1, 0, 0, 1, ...]
}
```
1 = correct image, 0 = incorrect.

4. Run PyGame CAPTCHA UI
```python
python captcha_pygame.py
```

Opens a 3×3 image grid.

## Users can:

1. Click images to select them

2. Press Submit to see correct/incorrect selections

3. Press Next to generate a new challenge

## Visual feedback:

1. Green border → correctly selected

2. Red border → wrong selection

3. Blue border → missed correct

## Files & Purpose
```
File	                                Purpose

extract_features.py     Converts images into 512-dim ResNet18 vectors for clustering

cluster_images.py	    Groups images into clusters using KMeans

generate_captcha.py	    Generates CAPTCHA challenges with correct/incorrect images

captcha_pygame.py	    Interactive PyGame UI for selecting CAPTCHA images

features.npy	        Saved feature vectors from images

filenames.npy	        List of filenames corresponding to features

labels.npy	            Cluster assignments for each image

images/	                Dataset images used for CAPTCHA
```

## How It Works

1. Feature Extraction

        Each image is converted into a 512-dimensional vector using ResNet18.

        Captures high-level features (objects, shapes, textures).

2. Clustering

        KMeans groups images into clusters based on similarity.

        Cluster assignments are saved to labels.npy.

3. CAPTCHA Generation

        Randomly selects a target cluster.

        Picks correct images from target cluster and incorrect images from others.

        Shuffles and returns data for UI display.

4. PyGame UI

        Displays a 3×3 grid of images.

        Users click images and submit their selection.

        Borders indicate correct, wrong, or missed images.

## Screenshots

<div align="center">
  <img src="screenshots/Screenshot 2025-12-01 035853.png" alt="Screenshot 1"/>
</div>

<div align="center">
  <img src="screenshots/Screenshot 2025-12-01 035910.png" alt="Screenshot 2"/>
</div>

<div align="center">
  <img src="screenshots/Screenshot 2025-12-01 040004.png" alt="Screenshot 3"/>
</div>

<div align="center">
  <img src="screenshots/Screenshot 2025-12-01 040046.png" alt="Screenshot 4"/>
</div>
