# wine_quality_white
import numpy as np
from sklearn.metrics import classification_report

from data_loader import load_filtered_dataset
from SVM_class.svm_multi_model import SVM
from SVM_class.utils import calculate_accuracy
from visualization_white import plot_class_distribution, plot_confusion_matrix


# Load and preprocess data
file_path = r"dataset\filtered_winequality-white.csv"
train_features, train_labels, test_features, test_labels = load_filtered_dataset(file_path, ratio=0.2)

# Print the number of training and testing samples
print(f"Training data size: {len(train_features)}")
print(f"Testing data size: {len(test_features)}")

kernels_name = ["linear", "poly", "rbf"]

for kernel_name in kernels_name:
    print(f"\nTraining SVM with {kernel_name} kernel...")
    if kernel_name == 'rbf':
        svm_model = SVM(kernel_name, C=0.25, max_iter=100, gamma=0.41)
    elif kernel_name == 'poly':
        svm_model = SVM(kernel_name, C=1.0, max_iter=100, degree=3)
    else:
        svm_model = SVM(kernel_name, C=10.0, max_iter=100)
    svm_model.train(train_features, train_labels)
    print(f"Model trained using {kernel_name} kernel.")

    predictions = svm_model.predict(train_features, train_labels, test_features)
    accuracy = calculate_accuracy(predictions, test_labels)

    # Output the accuracy for the kernel used
    print(f"Testing accuracy using {kernel_name} kernel: {accuracy:.8f}")
    print(f'classification report:\n{classification_report(test_labels, predictions)}')

    # Output the confusion matrix and class distribution
    plot_confusion_matrix(test_labels, predictions, labels=[0, 1, 2], title=f"{kernel_name}")
    plot_class_distribution(test_labels, predictions, labels=["Low", "Medium", "High"], title=f"{kernel_name}")
