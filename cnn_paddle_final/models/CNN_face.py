import paddle
import paddle.nn as nn
import paddle.nn.functional as F
from paddle.nn.initializer import Normal


# 参数初始化
def gaussian_weights_init(m):
    if isinstance(m, nn.Conv2D):
        m.weight.set_value(paddle.randn(m.weight.shape) * 0.04)


class FaceCNN(nn.Layer):
    # 初始化网络结构
    def __init__(self):
        super(FaceCNN, self).__init__()

        # layer1(conv + relu + pool)
        # input:(batch_size, 1, 48, 48), output(batch_size, 64, 24, 24)
        self.conv1 = nn.Sequential(
            nn.Conv2D(1, 64, 3, padding=1),
            nn.BatchNorm2D(64),
            nn.ReLU(),  # 使用ReLU代替RReLU
            nn.MaxPool2D(2)
        )

        # layer2(conv + relu + pool)
        # input:(batch_size, 64, 24, 24), output(batch_size, 128, 12, 12)
        self.conv2 = nn.Sequential(
            nn.Conv2D(64, 128, 3, padding=1),
            nn.BatchNorm2D(128),
            nn.ReLU(),  # 使用ReLU代替RReLU
            nn.MaxPool2D(2)
        )

        # layer3(conv + relu + pool)
        # input: (batch_size, 128, 12, 12), output: (batch_size, 256, 6, 6)
        self.conv3 = nn.Sequential(
            nn.Conv2D(128, 256, 3, padding=1),
            nn.BatchNorm2D(256),
            nn.ReLU(),  # 使用ReLU代替RReLU
            nn.MaxPool2D(2)
        )

        # 参数初始化
        self.apply(gaussian_weights_init)

        # 全连接层
        self.fc = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(),  # 使用ReLU代替RReLU

            nn.Dropout(p=0.5),
            nn.Linear(4096, 1024),
            nn.ReLU(),  # 使用ReLU代替RReLU

            nn.Linear(1024, 256),
            nn.ReLU(),  # 使用ReLU代替RReLU
            nn.Linear(256, 7)
        )

    # 向前传播
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = paddle.flatten(x, start_axis=1)  # 数据扁平化
        y = self.fc(x)

        return y