import os
import cv2
import numpy as np
import paddle
import pandas as pd


class FaceDataset(paddle.io.Dataset):
    # 初始化
    def __init__(self, root):
        super(FaceDataset, self).__init__()
        self.root = root

        # 使用pandas读取路径和标签
        df_path = pd.read_csv(root, header=None, usecols=[0])
        df_label = pd.read_csv(root, header=None, usecols=[1])

        # 将路径和标签转换为NumPy数组
        self.path = np.array(df_path)[:, 0]
        self.label = np.array(df_label)[:, 0]

    # 读取某幅图片，item为索引号
    def __getitem__(self, idx):
        # 拼接图像路径
        image_path = os.path.join(self.root, self.path[idx])

        # 检查文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # 读取图像数据
        face = cv2.imread(image_path)
        if face is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # 读取单通道灰度图
        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        # 直方图均衡化
        face_hist = cv2.equalizeHist(face_gray)

        # 像素值标准化，48x48的图像转换为1x48x48格式
        face_normalized = face_hist.reshape(1, 48, 48) / 255.0

        # 将图像数据转换为Paddle Tensor并改变数据类型
        face_tensor = paddle.to_tensor(face_normalized, dtype='float32')  # 使用paddle.to_tensor而非torch.from_numpy

        # 获取标签
        label = self.label[idx]

        return face_tensor, label

    # 获取数据集样本个数
    def __len__(self):
        return len(self.path)
