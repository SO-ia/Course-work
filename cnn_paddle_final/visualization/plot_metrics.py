import matplotlib.pyplot as plt

def plot_metrics(losses, train_acc, val_acc, filename='training_metrics.png'):
    """
    Plot loss and accuracy in the same figure for better comparison.
    :param losses: A list of loss values during training.
    :param train_acc: A list of training accuracy values.
    :param val_acc: A list of validation accuracy values.
    :param filename: Name of the file to save the plot.
    """
    fig, ax1 = plt.subplots(figsize=(10, 8))

    # Plot Loss on primary y-axis
    ax1.plot(losses, color='blue', label='Training Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create secondary y-axis for Accuracy
    ax2 = ax1.twinx()
    ax2.plot(train_acc, color='green', label='Training Accuracy', linestyle='--')
    ax2.plot(val_acc, color='red', label='Validation Accuracy', linestyle='--')
    ax2.set_ylabel('Accuracy', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    fig.tight_layout()  # Ensure everything fits without overlap
    plt.title('Training Loss and Accuracy')
    fig.legend(loc='upper right')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
