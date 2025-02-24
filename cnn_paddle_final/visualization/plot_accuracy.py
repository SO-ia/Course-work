import matplotlib.pyplot as plt

def plot_accuracy(train_acc, val_acc, filename='accuracy_plot.png'):
    """
    Plot the accuracy curves during training.
    :param train_acc: A list of training accuracy values.
    :param val_acc: A list of validation accuracy values.
    :param filename: Name of the file to save the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(train_acc, label='Training Accuracy', color='green')
    plt.plot(val_acc, label='Validation Accuracy', color='red')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
