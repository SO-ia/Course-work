# utils.py
import numpy as np


def calculate_accuracy(predictions, labels):
    correct = np.mean(predictions == labels)
    return correct
