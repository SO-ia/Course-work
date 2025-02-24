import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels


class SVM:
    def __init__(self, kernel_func='linear', C=1.0, max_iter=100, tolerance=1e-4, degree=3, gamma=0.1):
        """
        Initialize the Support Vector Machine (SVM) classifier.

        Parameters:
        - kernel_func: The kernel function to use ('linear', 'poly', 'rbf').
        - C: Regularization parameter (higher values give less margin but fewer misclassifications).
        - max_iter: Maximum number of iterations for optimization.
        - tolerance: Tolerance for convergence (when changes in alpha are small enough, we stop iterating).
        - degree: Degree of the polynomial kernel (relevant for 'poly' kernel).
        - gamma: Gamma parameter for the 'rbf' kernel (controls the shape of the decision boundary).
        """
        self.kernel_func = kernel_func
        self.C = C
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.alpha = None
        self.b = None
        self.kernel_matrix = None  # Cache kernel matrix for faster computation
        self.classes = None
        self.gamma = gamma
        self.degree = degree

    def sk_precompute_kernel_matrix(self, X):
        """
        预计算核矩阵，以提高计算效率
        Precompute the kernel matrix for the training data X.
        This allows us to avoid recalculating the kernel in every iteration during training.

        Parameters:
        - X: Training data (a 2D array of shape [n_samples, n_features]).

        Returns:
        - kernel_matrix: The precomputed kernel matrix.
        """
        if self.kernel_func == 'linear':
            # Linear kernel
            kernel_matrix = pairwise_kernels(X, metric='linear')
        elif self.kernel_func == 'poly':
            # Polynomial kernel
            kernel_matrix = pairwise_kernels(X, metric='polynomial', degree=self.degree)
        elif self.kernel_func == 'rbf':
            # RBF kernel
            kernel_matrix = pairwise_kernels(X, metric='rbf', gamma=self.gamma)
        else:
            # Error if an unsupported kernel is specified
            raise ValueError("Unsupported kernel type")
        return kernel_matrix

    def train(self, X, y):
        """
        训练支持向量机模型，使用One-vs-All策略处理多分类任务
        Train the SVM model using a One-vs-All strategy for multiclass classification.

        Parameters:
        - X: Training data (a 2D array of shape [n_samples, n_features]).
        - y: Training labels (a 1D array of shape [n_samples]).

        This function trains the model for all classes using the One-vs-All approach, where for each class,
        we train a binary classifier to distinguish that class from all others.
        """
        n_samples, n_features = X.shape
        self.classes = np.unique(y)  # Get unique class labels

        # Initialize alpha (Lagrange multipliers) and b (bias) for each class        self.alpha = {}
        self.b = {}

        # Precompute the kernel matrix for the training set (avoids recomputation in each iteration)
        print("Computing kernel matrix...")
        self.kernel_matrix = self.sk_precompute_kernel_matrix(X)

        # Compute class weights to handle class imbalance
        class_counts = {class_label: np.sum(y == class_label) for class_label in self.classes}  # Class counts
        total_samples = len(y)
        class_weights = {class_label: total_samples / class_counts[class_label] for class_label in self.classes}  # Weight for each class

        # Train a binary SVM classifier for each class (One-vs-All)
        for class_label in self.classes:
            print(f"Training for class: {class_label}")
            y_binary = np.where(y == class_label, 1, -1)  # Create binary labels for the current class (1 for the class, -1 for others)
            self.alpha[class_label] = np.zeros(n_samples)  # Initialize the alpha vector for the current class
            self.b[class_label] = 0  # Initialize the bias term for the current class

            # Maximum number of iterations for training
            for iteration in range(self.max_iter):
                alpha_prev = np.copy(self.alpha[class_label])  # Save previous alpha values for convergence check

                # Iterate through all training samples
                for i in range(n_samples):
                    # Calculate the margin (decision function value) for the current sample
                    margin = np.sum(self.alpha[class_label] * y_binary * self.kernel_matrix[i]) + self.b[class_label]

                    # Weighted margin to give more importance to less frequent classes
                    weighted_margin = margin * class_weights[class_label]

                    # Debug: 打印 margin 和 alpha 更新的值
                    # if i % 3000 == 0:  # 每500个样本打印一次
                    #     print(f"i: {i}, margin: {margin}, alpha[{i}]: {self.alpha[class_label][i]}")

                    # If the sample is misclassified, update the alpha and b values
                    if y_binary[i] * weighted_margin < 1:
                        self.alpha[class_label][i] += self.C * (1 - y_binary[i] * weighted_margin)
                        self.b[class_label] += self.C * y_binary[i]

                    # Clip alpha to ensure it's within the range [0, C]
                    self.alpha[class_label][i] = np.clip(self.alpha[class_label][i], 0, self.C)

                # Debug: 打印 alpha 更新后的信息
                # print(f"After iteration {iteration + 1}, alpha[{class_label}]: {self.alpha[class_label]}")

                # Check for convergence by comparing the change in alpha values
                alpha_change = np.linalg.norm(self.alpha[class_label] - alpha_prev)
                if alpha_change < self.tolerance:
                    # print(f"Class {class_label} converged after {iteration + 1} iterations. Alpha change: {alpha_change}")
                    break  # If the change in alpha is small enough, stop the iteration
                # elif iteration == self.max_iter - 1:  # 如果达到最大迭代次数，打印警告
                #     print(f"Class {class_label} did not converge after {self.max_iter} iterations. Alpha change: {alpha_change}")

    def predict(self, X_train, y_train, X_test):
        """
        基于训练好的模型进行预测
        Make predictions using the trained SVM model.

        Parameters:
        - X_train: The training data (used to calculate the decision function).
        - y_train: The training labels (used to calculate the decision function).
        - X_test: The test data to predict labels for.

        Returns:
        - predictions: Predicted labels for the test data.
        """
        # Compute the kernel matrix between the training and test data
        if self.kernel_func == 'linear':
            kernel_matrix = pairwise_kernels(X_test, X_train, metric='linear')
        elif self.kernel_func == 'poly':
            kernel_matrix = pairwise_kernels(X_test, X_train, metric='polynomial', degree=self.degree)
        elif self.kernel_func == 'rbf':
            kernel_matrix = pairwise_kernels(X_test, X_train, metric='rbf', gamma=self.gamma)
        else:
            raise ValueError("Unsupported kernel type")

        predictions = []
        # For each test sample, compute the margin for each class and predict the class with the highest margin
        for i in range(X_test.shape[0]):
            margins = []
            for class_label in self.classes:
                margin = np.sum(self.alpha[class_label] * y_train * kernel_matrix[i]) + self.b[class_label]
                margins.append(margin)

            # Predict the class with the highest margin
            predicted_class = self.classes[np.argmax(margins)]  # Select the class with the highest margin
            predictions.append(predicted_class)

        return np.array(predictions)  # Return the predicted labels as a NumPy array
