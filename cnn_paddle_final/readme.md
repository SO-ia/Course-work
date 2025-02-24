### 项目概述

该项目旨在构建和训练一个基于PaddlePaddle深度学习框架的卷积神经网络（CNN）模型，用于人脸表情分类。项目中包含了两个主要的模型结构：一个是标准的CNN结构，另一个是残差网络（ResNet）结构。模型的目标是能够识别七种基本的人脸表情：愤怒、厌恶、恐惧、高兴、悲伤、惊讶和中性。



### 外部依赖包

requirements.txt内容如下：

```python
imgaug==0.4.0
matplotlib==2.0.2
numpy==1.13.1
opencv_python==4.10.0.84
paddlepaddle==2.6.2
pandas==2.2.3
Pillow==4.2.1
scikit_learn==1.3.2
seaborn==0.13.2
tqdm==4.66.4
```

PaddlePaddle：深度学习框架，用于构建和训练模型。

NumPy：用于数值计算。

Pandas：用于数据处理和CSV文件操作。

OpenCV（cv2）：用于图像处理。

imgaug：用于图像数据增强。

Matplotlib：用于数据可视化。

scikit-learn：用于计算分类报告和其他机器学习工具。

PIL（Python Imaging Library）：用于图像处理。



### 项目结构

```python
cnn_paddle_final
│  img_zeng.py
│  model_valid_cnn.py
│  model_valid_ResNet.py
│  train.py
│  train_ResNet.py
│
├─dataloader
│    cnn_picture_label.py
│    cnn_picture_to_csv.py
│    rewrite_dataset.py
│
├─datasets
│  ├─cnn_test                   # 以下文件通过数据预处理自动生成
│  │  │ test_dataset.csv
│  │  └─angry等七个人脸类别文件夹
│  │          
│  ├─cnn_train
│  │  │ train_dataset.csv
│  │  └─angry等七个人脸类别文件夹
│  │          
│  ├─cnn_val
│  │  │  val_dataset.csv
│  │  └─angry等七个人脸类别文件夹
│  │
│  └─facial expression          # 运行时需要将原始数据集放于datasets文件夹下
│     └─angry等七个人脸类别文件夹
│
├─models
│    CNN_face.py
│    CNN_face_ResNet.py
│
└─visualization
      plot_accuracy.py
      plot_loss.py
      plot_matrix.py
      plot_metrics.py
      __init__.py
```



### 主要文件说明

`model_valid_cnn.py`：用于加载训练好的CNN模型，并在测试集上进行验证和预测。

`model_valid_ResNet.py`: 加载训练好的ResNet模型，并在测试集上进行验证和预测。

`train.py`：用于训练CNN模型，并保存最佳模型参数。

`train_ResNet.py`：用于训练ResNet模型，并保存最佳模型参数。

`CNN_face.py`：定义了一个标准的CNN模型结构，用于人脸表情分类。

`CNN_ResNet.py`：定义了一个基于ResNet的模型结构，用于人脸表情分类。

`cnn_picture_label.py`：用于将数据集中的图片按类别划分，并生成训练集、验证集和测试集的标签。

`cnn_picture_to_csv.py`：用于将图像数据转换为CSV文件。

`img_zeng.py`：用于对数据集中的图像进行数据增强。

`rewrite_dataset.py`：定义了一个用于加载和处理数据集的FaceDataset类。



### 代码主要功能

模型构建：在CNN_face.py和CNN_ResNet.py中定义了两个神经网络模型结构，分别用于构建标准的CNN和ResNet模型。

数据预处理：cnn_picture_label.py用于数据集的划分和标签生成，img_zeng.py用于数据增强，rewrite_dataset.py中的FaceDataset类用于加载和预处理数据。

模型训练与验证：train.py负责模型的训练和验证，并保存最佳模型参数。model_valid.py用于加载训练好的模型，并在测试集上进行验证和预测。

数据可视化：使用matplotlib库在model_valid.py中可视化混淆矩阵。



### 运行步骤

由于路径使用绝对路径，因此在运行前需要先替换为本机存在的路径

1. 环境配置

   ```python
   pip install -r requirements.txt
   ```

2. 数据准备：
   
   使用cnn_picture_label.py脚本将数据集中的图片按类别划分，并生成训练集、验证集和测试集的标签。
   
   使用img_zeng.py脚本对数据集中的图像进行数据增强。
   
   使用cnn_picture_to_csv.py脚本将图像数据转换为CSV文件。

4. 模型训练：
   
   运行train.py脚本，训练CNN模型，并在每个epoch后评估模型性能，保存最佳模型参数。
   
   运行train_ResNet.py脚本，训练ResNet模型，并在每个epoch后评估模型性能，保存最佳模型参数。

6. 模型验证：
   
   使用model_valid.py脚本加载训练好的CNN模型，并在测试集上进行验证和预测，输出分类报告和可视化混淆矩阵。
   
   使用model_valid_ResNet.py脚本加载训练好的ResNet模型，并在测试集上进行验证和预测，输出分类报告和可视化混淆矩阵。

8. 结果分析：
   
   分析model_valid.py脚本输出CNN模型的分类报告和混淆矩阵，评估模型性能
   
   分析model_valid_ResNet.py脚本输出ResNet模型的分类报告和混淆矩阵，评估模型性能
