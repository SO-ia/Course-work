import csv
from math import log2


def load_dataset(file_path):
    features = []
    labels = []
    header = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)  # Read header
        for row in reader:
            features.append([float(x) for x in row[:-1]])  # Features
            labels.append(int(row[-1]))  # Quality label
    return features, labels, header


def calculate_entropy(data):
    total = len(data)
    label_counts = {}
    for label in data:
        label_counts[label] = label_counts.get(label, 0) + 1
    entropy = 0
    for count in label_counts.values():
        p = count / total
        entropy -= p * log2(p)
    return entropy


def calculate_information_gain(dataset, feature_index, labels):
    total_entropy = calculate_entropy(labels)
    subsets = {}
    for row, label in zip(dataset, labels):
        key = row[feature_index]
        if key not in subsets:
            subsets[key] = []
        subsets[key].append(label)

    weighted_entropy = 0
    total = len(labels)
    for subset_labels in subsets.values():
        subset_entropy = calculate_entropy(subset_labels)
        weighted_entropy += (len(subset_labels) / total) * subset_entropy

    return total_entropy - weighted_entropy


def select_top_features(features, labels, num_top=8):
    info_gains = []
    num_features = len(features[0])
    for i in range(num_features):
        ig = calculate_information_gain(features, i, labels)
        info_gains.append((i, ig))
    info_gains.sort(key=lambda x: x[1], reverse=True)
    return [index for index, _ in info_gains[:num_top]]


def filter_and_save(features, labels, top_features, header, output_path):
    filtered_features = [[row[i] for i in top_features] for row in features]
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([header[i] for i in top_features] + ["quality"])
        for row, label in zip(filtered_features, labels):
            writer.writerow(row + [label])


# Main execution
file_path = r'dataset\winequality-white.csv'
output_file_path = r'dataset\filtered_winequality-white.csv'

features, labels, header = load_dataset(file_path)
top_features = select_top_features(features, labels)

# print(top_features)
filter_and_save(features, labels, top_features, header, output_file_path)

