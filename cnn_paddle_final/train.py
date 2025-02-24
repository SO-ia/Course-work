from datetime import datetime
import paddle
import paddle.nn as nn
import paddle.optimizer as optim
import numpy as np
from models import CNN_face
from dataloader import rewrite_dataset
import matplotlib.pyplot as plt


# 绘制损失曲线
def plot_loss_curve(train_loss):
    epochs = range(1, len(train_loss) + 1)

    plt.figure(figsize=(8, 6))
    plt.plot(epochs, train_loss, 'b-', label='Training Loss')
    plt.title('Training Loss per Epoch')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig('training_loss_curve.png')
    plt.show()


# 绘制准确率曲线
def plot_accuracy_curve(train_acc, val_acc):
    epochs = range(1, len(train_acc) + 1)

    plt.figure(figsize=(8, 6))
    plt.plot(epochs, train_acc, 'g-', label='Training Accuracy')
    plt.plot(epochs, val_acc, 'r-', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy per Epoch')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('training_accuracy_curve.png')
    plt.show()


def train(train_dataset, val_dataset, batch_size, epochs, learning_rate, print_cost=True, isPlot=True):
    # 加载数据集并分割batch
    train_loader = paddle.io.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # 构建模型
    model = CNN_face.FaceCNN()

    # 损失函数和优化器
    compute_loss = nn.CrossEntropyLoss()
    optimizer = optim.Adam(learning_rate=learning_rate, parameters=model.parameters(), weight_decay=0.005)

    best_train_acc = 0.0
    best_val_acc = 0.0
    best_model = None  # 用来保存验证集准确率最好的模型

    # 用于存储每个epoch的损失和准确率
    train_losses = []
    train_accuracies = []
    val_accuracies = []

    for epoch in range(epochs):
        print(f"epoch {epoch + 1}")
        model.train()  # 设置模型为训练模式

        epoch_loss = 0.0
        correct_train = 0
        total_train = 0

        for batch_id, (images, labels) in enumerate(train_loader):
            # print("batch_id",batch_id)
            # 优化器清零
            optimizer.clear_grad()

            # 前向传播
            outputs = model(images)

            # 计算损失
            loss = compute_loss(outputs, labels)

            # 反向传播
            loss.backward()

            # 更新参数
            optimizer.step()

            epoch_loss += loss.numpy()  # 累加每个batch的损失

            # 计算训练集准确率
            pred = np.argmax(outputs.numpy(), axis=1)  # 获取最大值索引
            correct_train += np.sum((pred == labels.numpy()))
            total_train += len(images)

        # 记录每个epoch的训练损失
        train_loss = epoch_loss / (batch_id + 1)  # 计算当前epoch的平均损失
        train_losses.append(train_loss)

        # 计算训练集准确率
        acc_train = correct_train / total_train
        train_accuracies.append(acc_train)

        # 打印损失值
        if print_cost:
            print(f"Epoch {epoch + 1}: train_loss: {train_loss:.4f}, train_acc: {acc_train * 100:.2f}%")

        # 评估模型准确率
        acc_val = validate(model, val_dataset, batch_size)
        val_accuracies.append(acc_val)
        print(f"Validation Accuracy: {acc_val * 100:.2f}%")



        # 更新最佳准确率
        if acc_train > best_train_acc:
            best_train_acc = acc_train
        if acc_val > best_val_acc:
            best_val_acc = acc_val
            best_model = model.state_dict()  # 保存验证集准确率最好的模型

    print(f"Best Train Accuracy during Training: {best_train_acc * 100:.2f}%")
    print(f"Best Validation Accuracy during Training: {best_val_acc * 100:.2f}%")

    # 绘制损失和准确率曲线
    if isPlot:
        plot_loss_curve(train_losses)
        plot_accuracy_curve(train_accuracies, val_accuracies)

    return best_model, best_train_acc, best_val_acc


# 验证模型在验证集上的正确率
def validate(model, dataset, batch_size):
    val_loader = paddle.io.DataLoader(dataset, batch_size=batch_size)
    result, total = 0.0, 0
    model.eval()
    for images, labels in val_loader:
        # 前向传播
        pred = model(images)

        # 预测结果
        pred = np.argmax(pred.numpy(), axis=1)  # 获取最大值索引
        labels = labels.numpy()

        # 计算正确的预测数量
        result += np.sum((pred == labels))
        total += len(images)

    # 返回准确率
    acc = result / total
    return acc


def main():
    start = datetime.now()
    print(f"start: {start}")

    # 加载数据集
    train_dataset = rewrite_dataset.FaceDataset(
        root=r'E:\pycharm\cnn\face_cnn_paddle\datasets\cnn_train\train_dataset.csv')
    val_dataset = rewrite_dataset.FaceDataset(
        root=r'E:\pycharm\cnn\face_cnn_paddle\datasets\cnn_val\val_dataset.csv')

    # 训练模型
    best_model, best_train_acc, best_val_acc = train(train_dataset, val_dataset, batch_size=64, epochs=30,
                                                     learning_rate=0.001, print_cost=True, isPlot=True)

    # 保存验证集准确率最好的模型
    paddle.save(best_model, 'best_model_net.pdparams')  # 保存最佳验证集准确率的模型

    # 打印最终准确率
    print(f"Best Train Accuracy: {best_train_acc * 100:.2f}%")
    print(f"Best Validation Accuracy: {best_val_acc * 100:.2f}%")

    end = datetime.now()
    print(f"end: {end}")
    print(f"running time: {end - start}")


if __name__ == '__main__':
    main()
