# adult
import numpy as np
from sklearn.metrics import classification_report
from SVM_class.svm_binary_model import SVM
from SVM_class.utils import calculate_accuracy
from data_loader import load_income_data
from visualization_adult import plot_confusion_matrix, plot_class_distribution

# Load and preprocess the dataset
file_path = r"dataset\adult.csv"
ratio = 0.2
# Split dataset into training and testing sets
train_features, train_labels, test_features, test_labels = load_income_data(file_path, ratio, is_pack=False)

# Print the number of training and testing samples
print(f"Training data size: {len(train_features)}")
print(f"Testing data size: {len(test_features)}")

kernels_name = ["linear", "poly", "rbf"]

for kernel_name in kernels_name:
    print(f"\nTesting SVM with {kernel_name} kernel...")

    if kernel_name == 'rbf':
        svm_model = SVM(kernel_name, C=0.03, max_iter=100, gamma=0.6)
    elif kernel_name == 'poly':
        svm_model = SVM(kernel_name, C=0.01, max_iter=100, degree=4)
    else:
        svm_model = SVM(kernel_name, C=0.01, max_iter=100)

    svm_model.train(train_features, train_labels)

    # Make predictions on the test set
    predictions = svm_model.predict(train_features, train_labels, test_features)
    accuracy = calculate_accuracy(predictions, test_labels)

    # Output the accuracy for the kernel used
    print(f"Testing accuracy using {kernel_name} kernel: {accuracy:.8f}")
    print(f'classification report:\n{classification_report(test_labels, predictions)}')

    # Output the confusion matrix and class distribution
    plot_confusion_matrix(test_labels, predictions, labels=[0, 1], title=f"{kernel_name} Kernel")
    plot_class_distribution(test_labels, predictions, title=f"{kernel_name} Kernel")
