import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y_true, y_pred, labels=None, title="Confusion Matrix", cmap='Blues'):
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
    plt.title(title)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the figure to the images folder with the given naming format
    file_name = f"images/001_{title}_matrix.png"
    plt.savefig(file_name)

    plt.show()


def plot_class_distribution(y_true, y_pred, title):
    """
    Plots the distribution of true and predicted class labels.

    Parameters:
    - y_true (np.ndarray): The true class labels
    - y_pred (np.ndarray): The predicted class labels
    """
    # Ensure y_true and y_pred are NumPy arrays and contain only non-negative integers
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # Get the class distribution for the true labels
    true_counts = np.bincount(y_true.astype(int), minlength=2)  # Binary classification: 0 and 1

    # Get the class distribution for the predicted labels
    pred_counts = np.bincount(y_pred.astype(int), minlength=2)  # Binary classification: 0 and 1

    # Define x-axis positions
    x = np.arange(2)  # Only two classes: 0 and 1

    # Set width for the bars
    width = 0.35

    # Create the bar plot for true vs predicted counts
    plt.bar(x - width / 2, true_counts, width, label='True Labels')
    plt.bar(x + width / 2, pred_counts, width, label='Predicted Labels')

    # Add labels and title
    plt.xlabel('Class')
    plt.ylabel('Frequency')
    plt.title(title + '\nClass Distribution: True vs Predicted')
    plt.xticks(x, ['<=50K', '>50K'])  # Set class labels for the x-axis
    plt.legend()

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the figure to the images folder with the given naming format
    file_name = f"images/001_{title}_bar.png"
    plt.savefig(file_name)

    # Show the plot
    plt.show()
