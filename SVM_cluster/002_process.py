# wine_quality_red
import numpy as np
from sklearn.metrics import classification_report
from data_loader import load_red_data
from SVM_class.svm_multi_model import SVM
from SVM_class.utils import calculate_accuracy
from visualization_red import plot_class_distribution, plot_confusion_matrix


# Load and preprocess data
file_path = r"dataset\winequality-red.csv"
train_features, train_labels, test_features, test_labels = load_red_data(file_path, ratio=0.2)

# Print the number of training and testing samples
print(f"Training data size: {len(train_features)}")
print(f"Testing data size: {len(test_features)}")

# List of kernel names for testing
kernels_name = ['linear', 'poly', 'rbf']

# Grid search to find the best hyperparameters
for kernel_name in kernels_name:
    print(f"\nTesting SVM with {kernel_name} kernel...")

    # Initialize the SVM model with the current combination of parameters
    if kernel_name == 'rbf':
        svm_model = SVM(kernel_name, C=0.03, max_iter=100, gamma=0.22)
    elif kernel_name == 'poly':
        svm_model = SVM(kernel_name, C=0.1, max_iter=100, degree=3)
    else:   # 'linear
        svm_model = SVM(kernel_name, C=0.01, max_iter=100)

    # Train the model
    svm_model.train(train_features, train_labels)

    # Predict using the trained model
    predictions = svm_model.predict(train_features, train_labels, test_features)
    accuracy = calculate_accuracy(predictions, test_labels)

    print(f"Testing accuracy: {accuracy:.8f}")
    print(f'classification report:\n{classification_report(test_labels, predictions)}')

    # Output the confusion matrix and class distribution
    plot_confusion_matrix(test_labels, predictions, labels=[3, 4, 5, 6, 7, 8], title=f"{kernel_name}")
    plot_class_distribution(test_labels, predictions, labels=[3, 4, 5, 6, 7, 8], title=f"{kernel_name}")
