# data_loader.py
import csv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split  # Import train_test_split for data splitting
from sklearn.preprocessing import LabelEncoder, StandardScaler  # Import StandardScaler to normalize data


def load_income_data(file_path, ratio, is_pack):
    """
     Load and preprocess the income dataset. Handles missing values and encodes categorical features.

     Parameters:
     - file_path: The path to the CSV file containing the dataset.

     Returns:
     - features: Preprocessed feature matrix (numerical).
     - labels: The target labels (income <=50K, >50K).
     - label_encoders: A dictionary of LabelEncoders used to encode categorical features.
     """
    if is_pack:
        df = pd.read_csv(file_path)
    else:
        df = shuffle_data(file_path)

    # Handle missing values: Replace '?' with NaN
    df.replace('?', np.nan, inplace=True)

    # Drop rows with missing target labels (income)
    df.dropna(subset=['income'], inplace=True)

    # Impute missing values in features (for simplicity, using median or mode)
    for column in df.columns:
        if df[column].dtype == 'object':  # Categorical column
            # Use the mode to fill missing categorical data
            df[column] = df[column].fillna(df[column].mode()[0])
        else:  # Numerical column
            # Use the median to fill missing numerical data
            df[column] = df[column].fillna(df[column].median())

    # Encode categorical variables (except for the target label 'income')
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        if column != 'income':  # Don't encode the target column
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column])
            label_encoders[column] = le

    # Extract features (X) and target (y)
    X = df.drop(columns=['income'])
    y = df['income'].map({'<=50K': 0, '>50K': 1})  # Map income to binary (0, 1)

    # Normalize features
    X_scaled = normalize_data(X)

    features, labels, label_encoders = X_scaled, y, label_encoders

    # Split dataset into training and testing sets
    train_features, train_labels, test_features, test_labels = split_data(features, labels, ratio)

    return train_features, train_labels, test_features, test_labels


def load_filtered_dataset(file_path, ratio):
    """
    Load the filtered dataset from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - features (list): A list of feature values for each sample.
    - labels (list): A list of labels corresponding to each sample.
    - header (list): A list of the column headers from the dataset.
    """
    features = []
    labels = []
    header = []

    # Open the CSV file and read its contents
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)  # The first line is the header

        # Read each row in the CSV file and separate features and labels
        for row in reader:
            features.append([float(x) for x in row[:-1]])  # All columns except the last one are features
            labels.append(int(row[-1]))  # The last column is the label

    labels = reduce_classes(labels)  # Reduce classes to Low, Medium, High

    # Normalize the features
    normalized_features = normalize_data(features)

    # Split dataset into training and testing sets
    train_features, train_labels, test_features, test_labels = split_data(normalized_features, labels, test_ratio=ratio)

    # return features, labels, header
    return train_features, train_labels, test_features, test_labels


def load_red_data(file_path, ratio):

    data = pd.read_csv(file_path, delimiter=",")

    # Separate features (X) and labels (y)
    features = data.drop('quality', axis=1).values
    labels = data['quality'].values

    # 特征缩放：标准化（将数据转换为均值为 0，标准差为 1）
    # Normalize the features
    normalized_features = normalize_data(features)

    # 划分训练集和测试集（80% 用于训练，20% 用于测试）
    train_features, train_labels, test_features, test_labels = split_data(normalized_features, labels, test_ratio=ratio)

    return train_features, train_labels, test_features, test_labels


def shuffle_data(file_path, n=6000):
    """
    从CSV文件中随机选取 n 条数据，返回一个 DataFrame。

    :parameter:
    - file_path: path to dataset
    - n: select shuffling ，默认值为 6000

    :return:
    - 返回一个 pandas DataFrame，包含随机选取的样本数据。
    """
    # 读取 CSV 文件
    df = pd.read_csv(file_path)

    # 从 DataFrame 中随机选取 n 条数据
    sampled_data = df.sample(n=n, random_state=42)  # 设置 random_state 以确保结果可重复

    return sampled_data


def reduce_classes(labels):
    """
    Reduce the number of classes in the 'quality' column to 3 categories:
    Low (0), Medium (1), and High (2).

    Parameters:
    - labels (list): The list of original labels from the dataset.

    Returns:
    - reduced_labels (list): The reduced class labels (0, 1, or 2).
    """
    class_map = {}
    for label in set(labels):
        if label <= 5:  # Low quality
            class_map[label] = 0
        elif label <= 7:  # Medium quality
            class_map[label] = 1
        else:  # High quality
            class_map[label] = 2

    # Return the new label values based on the class_map
    return [class_map[label] for label in labels]


def split_data(features, labels, test_ratio=0.2, random_state=42):
    """
    Split the dataset into training and testing sets.

    This function uses sklearn's train_test_split for efficient data splitting.

    Parameters:
    - features (list or np.ndarray): The feature matrix.
    - labels (list or np.ndarray): The corresponding labels.
    - test_ratio (float): The proportion of the data to be used for testing (between 0 and 1).
    - random_state (int): Seed used by the random number generator to ensure reproducibility.

    Returns:
    - train_features (np.ndarray): The feature matrix for the training set.
    - train_labels (np.ndarray): The labels for the training set.
    - test_features (np.ndarray): The feature matrix for the testing set.
    - test_labels (np.ndarray): The labels for the testing set.
    """
    # Use sklearn's train_test_split for efficient data splitting
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=test_ratio, random_state=random_state
    )

    # Return the split data
    return np.array(train_features), np.array(train_labels), np.array(test_features), np.array(test_labels)


def normalize_data(features):
    """
    Normalize the feature data to have zero mean and unit variance.

    Parameters:
    - features (np.ndarray): The feature matrix to be normalized.

    Returns:
    - normalized_features (np.ndarray): The normalized feature matrix.
    """

    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(features)
    return normalized_features

# def split_data(features, labels, test_ratio):
#     data = list(zip(features, labels))
#     random.shuffle(data)
#     split_idx = int(len(data) * (1 - test_ratio))
#     train_data = data[:split_idx]
#     test_data = data[split_idx:]
#     train_features, train_labels = zip(*train_data)
#     test_features, test_labels = zip(*test_data)
#     return np.array(train_features), np.array(train_labels), np.array(test_features), np.array(test_labels)
