import os
import cv2
import pandas as pd

# 设置文件夹路径
dataset_dir = r'E:\pycharm\cnn\data\facial expression'  # 'face'文件夹所在路径
categories = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# 初始化数据列表
data = []

# 遍历每个子文件夹和图片
for label, category in enumerate(categories):
    category_folder = os.path.join(dataset_dir, category)

    # 确保文件夹存在
    if not os.path.exists(category_folder):
        continue

    for filename in os.listdir(category_folder):
        if filename.endswith('.jpg'):
            # 读取图像，转换为灰度图像
            img_path = os.path.join(category_folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            # 确保图像大小为48x48
            img = cv2.resize(img, (48, 48))

            # 将图像数据展平为一维数组并转换为每个像素值以空格分隔的字符串
            img_data = ' '.join(map(str, img.flatten()))

            # 创建每个图片的标签和特征数据
            data.append([label, img_data])
    print(category,"ok")
# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=['label', 'feature'])

# 保存为CSV文件
df.to_csv('facial_expression_features.csv', index=False)

print("数据已成功保存为CSV格式！")
