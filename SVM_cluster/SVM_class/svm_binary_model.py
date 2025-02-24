import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels  # For computing kernel functions between samples

class SVM:
    def __init__(self, kernel_func='linear', C=1.0, max_iter=100, tolerance=1e-4, degree=3, gamma=0.1):
        """
        Initialize the SVM model with the specified parameters.

        Parameters:
        - kernel_func: Type of kernel ('linear', 'poly', 'rbf')
        - C: Regularization parameter
        - max_iter: Maximum number of iterations for training
        - tolerance: Tolerance for stopping criterion
        - degree: Degree of the polynomial kernel (only used for 'poly')
        - gamma: Kernel coefficient (only used for 'rbf')
        """
        self.kernel_func = kernel_func
        self.C = C  # Regularization parameter
        self.max_iter = max_iter  # Maximum number of iterations for training
        self.tolerance = tolerance  # Tolerance for convergence
        self.alpha = None  # Lagrange multipliers (support vectors)
        self.b = None  # Bias term
        self.kernel_matrix = None  # Precomputed kernel matrix (to speed up calculations)
        self.gamma = gamma  # Kernel coefficient for RBF kernel
        self.degree = degree  # Degree for polynomial kernel

    def sk_precompute_kernel_matrix(self, X):
        """
            Precompute the kernel matrix to improve computational efficiency
        """
        if self.kernel_func == 'linear':
            # Compute the linear kernel matrix: K(x, y) = x.dot(y)
            kernel_matrix = pairwise_kernels(X, metric='linear')
        elif self.kernel_func == 'poly':
            # Compute the polynomial kernel matrix: K(x, y) = (x.dot(y) + 1)^degree
            kernel_matrix = pairwise_kernels(X, metric='polynomial', degree=self.degree)
        elif self.kernel_func == 'rbf':
            # Compute the radial basis function (RBF) kernel matrix: K(x, y) = exp(-gamma * ||x - y||^2)
            kernel_matrix = pairwise_kernels(X, metric='rbf', gamma=self.gamma)
        else:
            # Raise an error if the kernel type is unsupported
            raise ValueError("Unsupported kernel type")
        return kernel_matrix

    def train(self, X, y):
        """
        Train the SVM model using the given training data.

        Parameters:
        - X: Training feature matrix (n_samples x n_features)
        - y: Training labels (1D array of -1 or 1)
        """
        n_samples, n_features = X.shape  # Get number of samples and features
        y = np.where(y == 0, -1, y)  # Convert target labels to -1 or 1 (for binary classification)

        # Initialize alpha (Lagrange multipliers) and bias b
        self.alpha = np.zeros(n_samples)
        self.b = 0

        # Precompute the kernel matrix to avoid redundant computations in each iteration
        print("Computing kernel matrix...")
        self.kernel_matrix = self.sk_precompute_kernel_matrix(X)

        # Train using the standard SVM optimization loop
        for iteration in range(self.max_iter):
            alpha_prev = np.copy(self.alpha)  # Keep track of previous alpha values

            # Iterate over all samples and update the Lagrange multipliers (alpha) and bias (b)
            for i in range(n_samples):
                # Calculate the margin (decision function) for the current sample
                margin = np.sum(self.alpha * y * self.kernel_matrix[i]) + self.b

                # If the sample is misclassified (margin < 1), update alpha and bias
                if y[i] * margin < 1:
                    # Update alpha based on the gradient descent rule
                    self.alpha[i] += self.C * (1 - y[i] * margin)
                    self.b += self.C * y[i]  # Update the bias term

                # Clip alpha to ensure it stays within the range [0, C] to avoid overfitting
                self.alpha[i] = np.clip(self.alpha[i], 0, self.C)

            # Check for convergence: if the change in alpha is small enough, stop the training
            alpha_change = np.linalg.norm(self.alpha - alpha_prev)
            if alpha_change < self.tolerance:
                print(f"Converged after {iteration + 1} iterations.")
                break

    def predict(self, X_train, y_train, X_test):
        """
        Predict the labels for the test data based on the trained SVM model.

        Parameters:
        - X_train: Training feature matrix
        - y_train: Training labels
        - X_test: Test feature matrix

        Returns:
        - predictions: Predicted class labels for the test set
        """
        # Calculate the kernel matrix between the test samples and the training samples
        if self.kernel_func == 'linear':
            kernel_matrix = pairwise_kernels(X_test, X_train, metric='linear')
        elif self.kernel_func == 'poly':
            kernel_matrix = pairwise_kernels(X_test, X_train, metric='polynomial', degree=self.degree)
        elif self.kernel_func == 'rbf':
            kernel_matrix = pairwise_kernels(X_test, X_train, metric='rbf', gamma=self.gamma)
        else:
            raise ValueError("Unsupported kernel type")

        predictions = []  # List to store predictions for each test sample
        for i in range(X_test.shape[0]):
            # Calculate the margin (decision function) for the current test sample
            margin = np.sum(self.alpha * y_train * kernel_matrix[i]) + self.b

            # Predict the class: if margin >= 0, predict 1, else predict -1
            predicted_class = 1 if margin >= 0 else 0
            predictions.append(predicted_class)

        return np.array(predictions)
