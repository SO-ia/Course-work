import paddle
import paddle.nn as nn
import paddle.nn.functional as F
from paddle.nn.initializer import Normal


# 定义残差块 (Residual Block)，ResNet 的核心组件
class ResidualBlock(nn.Layer):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        # 第一个卷积层，保持输入和输出特征图的一致性
        self.conv1 = nn.Conv2D(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2D(out_channels)
        # 第二个卷积层，用于进一步提取特征
        self.conv2 = nn.Conv2D(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2D(out_channels)
        # Shortcut，用于将输入直接加到输出
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            # 如果通道数或尺寸变化，需要对输入进行调整
            self.shortcut = nn.Sequential(
                nn.Conv2D(in_channels, out_channels, kernel_size=1, stride=stride),
                nn.BatchNorm2D(out_channels)
            )

    def forward(self, x):
        # 主路径
        out = self.conv1(x)
        out = F.relu(self.bn1(out))  # ReLU 激活
        out = self.conv2(out)
        out = self.bn2(out)
        # 将输入直接加到输出
        out += self.shortcut(x)
        out = F.relu(out)  # 再次激活
        return out


# 定义 ResNet 主体网络
class ResNetFace(nn.Layer):
    def __init__(self, num_classes=7):
        super(ResNetFace, self).__init__()
        # 初始卷积层，用于提取低级特征
        self.initial = nn.Sequential(
            nn.Conv2D(1, 64, kernel_size=3, stride=1, padding=1),  # 输入为灰度图（1通道）
            nn.BatchNorm2D(64),
            nn.ReLU()
        )
        # 4个残差模块，每个模块由多个残差块组成
        self.layer1 = self._make_layer(64, 64, num_blocks=2, stride=1)  # 保持尺寸
        self.layer2 = self._make_layer(64, 128, num_blocks=2, stride=2)  # 下采样尺寸
        self.layer3 = self._make_layer(128, 256, num_blocks=2, stride=2)
        self.layer4 = self._make_layer(256, 512, num_blocks=2, stride=2)

        # 全局平均池化层，压缩特征图到 1x1 的大小
        self.global_pool = nn.AdaptiveAvgPool2D((1, 1))
        # 全连接层，用于分类
        self.fc = nn.Linear(512, num_classes)

    # 构建残差模块
    def _make_layer(self, in_channels, out_channels, num_blocks, stride):
        layers = []
        # 第一个残差块，可能涉及通道数或尺寸变化
        layers.append(ResidualBlock(in_channels, out_channels, stride))
        # 后续残差块
        for _ in range(1, num_blocks):
            layers.append(ResidualBlock(out_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        # 前向传播过程
        x = self.initial(x)  # 初始卷积层
        x = self.layer1(x)  # 第一个残差模块
        x = self.layer2(x)  # 第二个残差模块
        x = self.layer3(x)  # 第三个残差模块
        x = self.layer4(x)  # 第四个残差模块
        x = self.global_pool(x)  # 全局平均池化
        x = paddle.flatten(x, start_axis=1)  # 展平为全连接层输入
        x = self.fc(x)  # 全连接层
        return x
