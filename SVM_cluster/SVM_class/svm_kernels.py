# svm_kernels.py
import numpy as np


def linear_kernel(x, y):
    return np.dot(x, y)  # Dot product of vectors


def polynomial_kernel(x, y, degree=3):
    return (np.dot(x, y) + 1) ** degree


def rbf_kernel(x, y, gamma=0.1):
    return np.exp(-gamma * np.sum((x - y) ** 2))
