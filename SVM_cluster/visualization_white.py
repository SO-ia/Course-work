import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


# Function to plot Confusion Matrix
def plot_confusion_matrix(y_true, y_pred, labels=None, title=None, cmap='Blues'):
    """
    Plots a confusion matrix as a heatmap.

    Parameters:
    - y_true: True labels
    - y_pred: Predicted labels
    - labels: List of class labels (optional)
    - title: Title of the plot
    - cmap: Color map for the heatmap (default is 'Blues')
    """
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    # Plot confusion matrix using seaborn heatmap
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, xticklabels=labels, yticklabels=labels, cbar=False)

    # Titles and labels
    plt.title(title + "\nConfusion Matrix")
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the figure to the images folder with the given naming format
    file_name = f"images/003_{title}_matrix.png"
    plt.savefig(file_name)

    plt.show()


# Function to plot Bar Chart for class distribution comparison
def plot_class_distribution(y_true, y_pred, labels=None, title=None):
    """
    Plots a bar chart comparing the true class distribution with the predicted class distribution.

    Parameters:
    - y_true: True labels
    - y_pred: Predicted labels
    - labels: List of class labels (optional)
    - title: Title of the plot
    """
    # Ensure y_pred is integer type (needed for bincount)
    y_pred = np.round(np.clip(y_pred, 0, 2)).astype(int)  # Round to nearest int, clip to valid class range, and cast to integer

    # Count occurrences of each class in true and predicted labels
    true_counts = np.bincount(y_true, minlength=3)  # Ensure all classes are represented (minlength=3 for 3 classes)
    pred_counts = np.bincount(y_pred, minlength=3)  # Same for predicted labels

    # Ensure labels are available
    if labels is None:
        labels = [str(i) for i in range(len(true_counts))]

    # Set up bar positions for comparison
    x = np.arange(len(labels))
    width = 0.35  # Bar width

    # Create bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(x - width / 2, true_counts, width, label='True Labels')
    plt.bar(x + width / 2, pred_counts, width, label='Predicted Labels')

    # Titles and labels
    plt.title(title + "\nClass Distribution Comparison")
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.xticks(x, labels)
    plt.legend()

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the figure to the images folder with the given naming format
    file_name = f"images/003_{title}_bar.png"
    plt.savefig(file_name)

    plt.show()
