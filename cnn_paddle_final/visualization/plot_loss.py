import matplotlib.pyplot as plt

def plot_loss(losses, filename='loss_plot.png'):
    """
    Plot the loss curve during training.
    :param losses: A list of loss values during training.
    :param filename: Name of the file to save the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(losses, label='Training Loss', color='blue')
    plt.title('Training Loss Curve')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
