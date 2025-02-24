from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns


def plot_confusion_matrix(true_labels, predictions, class_names=None, filename='confusion_matrix.png'):
    """
    Plot and save the confusion matrix as a heatmap.
    """
    # Compute the confusion matrix
    cm = confusion_matrix(true_labels, predictions)

    # Create a seaborn heatmap for visualization
    plt.figure(figsize=(10, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.savefig(filename)
    plt.close()
