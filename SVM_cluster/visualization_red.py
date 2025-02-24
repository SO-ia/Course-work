import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def plot_confusion_matrix(true_labels, predicted_labels, labels, title=None):
    """
    Plots a confusion matrix as a heatmap.

    Parameters:
    - true_labels: True labels
    - predicted_labels: Predicted labels
    - labels: List of class labels（e.g. [3, 4, 5, 6, 7, 8]）
    - title: Title of the plot
    """
    # Compute confusion matrix
    cm = confusion_matrix(true_labels, predicted_labels, labels=labels)
    cm_display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    # Plot confusion matrix using seaborn heatmap
    plt.figure(figsize=(8, 6))
    cm_display.plot(cmap='Blues', ax=plt.gca())
    plt.title(title)
    plt.grid(False)

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the figure to the images folder with the given naming format
    file_name = f"images/002_{title}_matrix.png"
    plt.savefig(file_name)

    plt.show()


def plot_class_distribution(true_labels, predicted_labels, labels, title=None):
    """
    Plots the distribution of true and predicted class labels.

    Parameters:
    - true_labels: True labels
    - predicted_labels: Predicted labels
    - labels: List of class labels（e.g. [3, 4, 5, 6, 7, 8]）
    - title: Title of the plot
    """
    # Count occurrences of each class in true and predicted labels
    true_counts = [np.sum(np.array(true_labels) == label) for label in labels]
    pred_counts = [np.sum(np.array(predicted_labels) == label) for label in labels]

    # Set up bar positions for comparison
    bar_width = 0.4
    x = np.arange(len(labels))  # labels setting

    # Create bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(x - bar_width / 2, true_counts, width=bar_width, label='True Labels')
    plt.bar(x + bar_width / 2, pred_counts, width=bar_width, label='Predicted Labels')

    # Titles and labels
    plt.xticks(x, labels)
    plt.xlabel('Class Labels')
    plt.ylabel('Number of Samples')
    plt.title(title)
    plt.legend()
    plt.tight_layout()

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the figure to the images folder with the given naming format
    file_name = f"images/002_{title}_bar.png"
    plt.savefig(file_name)

    plt.show()
