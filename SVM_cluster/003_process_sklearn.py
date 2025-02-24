import numpy as np
from data_loader import load_filtered_dataset
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from visualization_white import plot_confusion_matrix, plot_class_distribution


# Load and preprocess the dataset
file_path = r"D:\A_assignment\work\Pythonwork\Nerual_Network\SVM_cluster\dataset\filtered_winequality-white.csv"
# Split dataset into training and testing sets
train_features, train_labels, test_features, test_labels = load_filtered_dataset(file_path, ratio=0.2)

# Print the number of training and testing samples
print(f"Training data size: {len(train_features)}")
print(f"Testing data size: {len(test_features)}")

kernels_name = ["linear", "poly", "rbf"]

for kernel_name in kernels_name:
    print(f"running with {kernel_name} kernel")
    if kernel_name == 'rbf':
        svm_model = SVC(kernel=kernel_name, C=0.1, gamma=0.1)
    elif kernel_name == 'poly':
        svm_model = SVC(kernel=kernel_name, C=0.1, degree=3)
    else:
        svm_model = SVC(kernel=kernel_name, C=0.1)

    svm_model.fit(train_features, train_labels)
    # Make predictions on the test set
    pred_labels = svm_model.predict(test_features)

    # Output the accuracy for the kernel used
    accuracy = np.mean(pred_labels == test_labels)
    print(f'Testing Accuracy: {accuracy:.8f}')
    print(f'classification report:\n{classification_report(test_labels, pred_labels)}')

    # Output the confusion matrix and class distribution
    plot_confusion_matrix(test_labels, pred_labels, labels=[0, 1, 2], title=f"{kernel_name}")
    plot_class_distribution(test_labels, pred_labels, labels=["Low", "Medium", "High"], title=f"{kernel_name}")
