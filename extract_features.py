import os
import torch
import numpy as np
from PIL import Image
from torchvision import models, transforms

IMAGE_DIR = "images"
SAVE_FILE = "features.npy"
SAVE_NAMES = "filenames.npy"

# 1) Load pretrained ResNet18
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model = torch.nn.Sequential(*list(model.children())[:-1])  # remove classifier
model.eval() # set to evaluation mode (to disable dropout, batchnorm, etc.)

# 2) Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(), #a tensor is an N-dimensional array, compatible with GPU acceleration.
])

features = []
filenames = []

# 3) Loop through images
for file in os.listdir(IMAGE_DIR):
    path = os.path.join(IMAGE_DIR, file)

    img = Image.open(path).convert("RGB") # resizes + converts to tensor → shape (3, 224, 224)
    x = transform(img).unsqueeze(0)   # add batch dimension (Batch size = 1, since we are processing images one by one.)

    with torch.no_grad(): #disables gradient computation (we are not training, only extracting features).
        vec = model(x).squeeze().numpy()  
        #model(x) → outputs the 512-dimensional feature vector for this image.
        #squeeze() → removes extra dimensions (from (1, 512, 1, 1) → (512,)).
        #numpy() → converts PyTorch tensor to a NumPy array for easier saving and processing.

    features.append(vec)
    filenames.append(file)

# Save outputs
np.save(SAVE_FILE, np.array(features))
np.save(SAVE_NAMES, np.array(filenames))

print("Done! Saved features for", len(features), "images.")


# ✔ What this does:
# Loads ResNet18
# Removes the last classification layer → output becomes a 512-dim vector
# Converts each image into a vector
# Saves:
# features.npy → array of all vectors
# filenames.npy → list of matching image files