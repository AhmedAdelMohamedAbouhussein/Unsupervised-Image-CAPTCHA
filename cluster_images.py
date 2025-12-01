import numpy as np
from sklearn.cluster import KMeans

features = np.load("features.npy")
filenames = np.load("filenames.npy")

NUM_CLUSTERS = 7

# Run KMeans
kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42) #sets the random seed for reproducibility.
# K-Means starts with random initial centroids, so fixing the seed ensures the same result every time you run the code.

labels = kmeans.fit_predict(features)
#does two things at once:
    #Fit → K-Means computes the cluster centroids from the features.
    #Predict → assigns each image to its closest cluster.

# Save cluster assignments
np.save("labels.npy", labels) #NumPy array of shape (num_images,) Each entry is an integer 0–4 indicating which cluster the image belongs to.

print("Clustering complete!")
for c in range(NUM_CLUSTERS):
    print(f"Cluster {c}: {sum(labels == c)} images")

# ✔ What this does:
# Loads feature vectors
# Runs KMeans
# Assigns each image to a cluster
# Saves labels.npy