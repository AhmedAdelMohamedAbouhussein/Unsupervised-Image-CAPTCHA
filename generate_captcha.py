import random
import numpy as np

filenames = np.load("filenames.npy")
labels = np.load("labels.npy")

NUM_IMAGES = 9  # total images shown in CAPTCHA
NUM_CLUSTERS = len(set(labels))

def generate_captcha():
    # 1) Random cluster to be the "correct" answer
    target_cluster = random.randint(0, NUM_CLUSTERS - 1)

    # 2) Select correct and incorrect images
    correct = np.where(labels == target_cluster)[0]
    wrong = np.where(labels != target_cluster)[0]

    # pick images
    selected_correct = random.sample(list(correct), 6)
    selected_wrong = random.sample(list(wrong), NUM_IMAGES - 6)

    # combine and shuffle
    all_indices = selected_correct + selected_wrong
    random.shuffle(all_indices)

    return {
        "target_cluster": int(target_cluster),
        "images": [filenames[i] for i in all_indices],
        "answers": [1 if i in selected_correct else 0 for i in all_indices]
    }

if __name__ == "__main__":
    print(generate_captcha())

# ✔ Explanation:
# You randomly choose a cluster (e.g., cluster 2)
# You pick:
# 3 images from cluster 2
# 6 images from other clusters
# Player must select the correct cluster’s images
# You also return the answer key (1 = correct, 0 = wrong)