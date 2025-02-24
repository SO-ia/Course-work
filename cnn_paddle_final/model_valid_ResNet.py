import paddle
import numpy as np
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from PIL import Image
import random
from models import CNN_face_ResNet
from dataloader import rewrite_dataset
from visualization import plot_accuracy, plot_matrix
from datetime import datetime


# 定义类别名称
classes_name = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def load_model(model_path):
    """
    加载训练好的模型
    """
    model = CNN_face_ResNet.ResNetFace()  # 初始化模型
    model.set_state_dict(paddle.load(model_path))  # 加载模型参数
    model.eval()  # 设置为评估模式
    return model

def test(model, test_loader):
    """
    在测试集上测试模型，并返回预测结果和真实标签
    """
    model.eval()
    all_preds = []
    all_labels = []

    for images, labels in test_loader:
        preds = model(images)
        preds = np.argmax(preds.numpy(), axis=1)  # 获取预测的类别索引
        labels = labels.numpy()  # 获取真实标签

        all_preds.extend(preds)
        all_labels.extend(labels)

    return np.array(all_preds), np.array(all_labels)

def test_saved_model(test_dataset, model_path='best_model_net.pdparams', batch_size=128):
    """
    加载保存的模型，并使用测试集进行测试
    """
    # 加载保存的模型参数
    model = load_model(model_path)

    # 创建DataLoader用于加载测试数据集
    test_loader = paddle.io.DataLoader(test_dataset, batch_size=batch_size)

    # 测试模型并获取预测结果和真实标签
    predictions, true_labels = test(model, test_loader)

    # 计算精确度、召回率、F1分数
    report = classification_report(true_labels, predictions, target_names=classes_name)
    print(report)

    # 可视化混淆矩阵
    plot_matrix.plot_confusion_matrix(true_labels, predictions, classes_name, filename='confusion_matrix.png')

def load_and_preprocess_image(image_path):
    """
    加载并预处理图像，以便进行模型推断
    """
    image = Image.open(image_path).convert('L')  # 打开图像并转换为灰度图
    image = image.resize((48, 48))  # 调整图像大小为48x48（假设模型输入为48x48）
    image = np.array(image) / 255.0  # 归一化图像至[0, 1]区间
    image = image.reshape((1, 48, 48))  # 将图像形状调整为(C, H, W)
    image = paddle.to_tensor(image, dtype=paddle.float32)  # 转换为Paddle的Tensor
    return image

def get_random_image_from_dataset(test_dataset):
    """
    从测试数据集中随机获取一张图片
    """
    random_idx = random.randint(0, len(test_dataset) - 1)  # 随机选择一个索引
    image, label = test_dataset[random_idx]  # 获取图像和标签
    return image, label, random_idx

def predict(model, image):
    """
    对给定的图像进行分类预测
    """
    pred = model(image.unsqueeze(0))  # 添加batch维度
    pred_class = np.argmax(pred.numpy())  # 获取预测的类别索引
    return pred_class

def main():
    start = datetime.now()
    print(f"开始时间: {start}")

    # 加载测试数据集
    test_dataset = rewrite_dataset.FaceDataset(
        root=r'datasets\cnn_test\test_dataset.csv')  # 修改为测试集路径

    # 使用测试集验证保存的模型
    test_saved_model(test_dataset)

    # 加载训练好的模型
    model = load_model('best_model_net.pdparams')

    # 从测试数据集中随机选取一张图片
    image, true_label, idx = get_random_image_from_dataset(test_dataset)

    # 预测选中图片的类别
    pred_class = predict(model, image)

    # 输出结果
    print(f"真实类别是 {classes_name[true_label]}，预测类别是 {classes_name[pred_class]}")

    # 展示图片
    image = image.squeeze(0)  # 去除batch维度
    plt.imshow(image, cmap='gray')  # 以灰度图显示图片
    plt.axis('off')  # 关闭坐标轴
    plt.show()

    end = datetime.now()
    print(f"结束时间: {end}")
    print(f"总运行时间: {end - start}")

if __name__ == '__main__':
    main()
