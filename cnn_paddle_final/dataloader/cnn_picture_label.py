import os
import pandas as pd
import random
import shutil

# 表情类别
categories = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# 读取每个类别文件夹中的图片，按80%为训练集，10%为验证集，10%为测试集划分
def data_label_and_split(source_dir, target_train_dir, target_val_dir, target_test_dir):
    # 存放图片路径和标签的列表
    train_path_list = []
    train_label_list = []
    val_path_list = []
    val_label_list = []
    test_path_list = []
    test_label_list = []

    # 遍历每个表情类别文件夹
    for idx, category in enumerate(categories):
        category_path = os.path.join(source_dir, category)
        files = os.listdir(category_path)

        # 获取该类别下所有图片文件（只考虑.jpg文件）
        image_files = [f for f in files if f.endswith('.jpg')]

        # 打乱文件顺序
        random.shuffle(image_files)

        # 划分80%作为训练集，10%作为验证集，10%作为测试集
        split_idx_80 = int(0.8 * len(image_files))  # 80%为训练集
        split_idx_90 = int(0.9 * len(image_files))  # 90%为验证集和测试集

        train_files = image_files[:split_idx_80]
        val_files = image_files[split_idx_80:split_idx_90]
        test_files = image_files[split_idx_90:]

        # 创建该类别的目标文件夹（如果不存在）
        train_category_dir = os.path.join(target_train_dir, category)
        val_category_dir = os.path.join(target_val_dir, category)
        test_category_dir = os.path.join(target_test_dir, category)

        os.makedirs(train_category_dir, exist_ok=True)
        os.makedirs(val_category_dir, exist_ok=True)
        os.makedirs(test_category_dir, exist_ok=True)

        # 移动图片到相应的训练集、验证集和测试集文件夹，同时记录路径和标签
        for train_file in train_files:
            # 源文件路径
            src = os.path.join(category_path, train_file)
            # 目标文件路径
            dst = os.path.join(train_category_dir, train_file)
            shutil.copy(src, dst)

            # 记录路径和标签
            train_path_list.append(dst)
            train_label_list.append(idx)  # 标签是类别的索引

        for val_file in val_files:
            # 源文件路径
            src = os.path.join(category_path, val_file)
            # 目标文件路径
            dst = os.path.join(val_category_dir, val_file)
            shutil.copy(src, dst)

            # 记录路径和标签
            val_path_list.append(dst)
            val_label_list.append(idx)  # 标签是类别的索引

        for test_file in test_files:
            # 源文件路径
            src = os.path.join(category_path, test_file)
            # 目标文件路径
            dst = os.path.join(test_category_dir, test_file)
            shutil.copy(src, dst)

            # 记录路径和标签
            test_path_list.append(dst)
            test_label_list.append(idx)  # 标签是类别的索引

    # 创建DataFrame并分别保存到训练集、验证集和测试集的csv文件
    train_df = pd.DataFrame({'path': train_path_list, 'label': train_label_list})
    val_df = pd.DataFrame({'path': val_path_list, 'label': val_label_list})
    test_df = pd.DataFrame({'path': test_path_list, 'label': test_label_list})

    # 保存到csv文件
    train_csv_path = os.path.join(target_train_dir, 'train_dataset.csv')
    val_csv_path = os.path.join(target_val_dir, 'val_dataset.csv')
    test_csv_path = os.path.join(target_test_dir, 'test_dataset.csv')

    train_df.to_csv(train_csv_path, index=False, header=False)
    val_df.to_csv(val_csv_path, index=False, header=False)
    test_df.to_csv(test_csv_path, index=False, header=False)

    print(f"train_dataset.csv has been saved to {train_csv_path}")
    print(f"val_dataset.csv has been saved to {val_csv_path}")
    print(f"test_dataset.csv has been saved to {test_csv_path}")


def main():
    # 定义源数据集和目标训练集、验证集、测试集路径
    source_dir = r'E:\pycharm\cnn\data\facial expression'
    target_train_dir = r'E:\pycharm\cnn\face_cnn_paddle\datasets\cnn_train'
    target_val_dir = r'E:\pycharm\cnn\face_cnn_paddle\datasets\cnn_val'
    target_test_dir = r'E:\pycharm\cnn\face_cnn_paddle\datasets\cnn_test'

    # 确保目标训练集、验证集和测试集的文件夹存在
    os.makedirs(target_train_dir, exist_ok=True)
    os.makedirs(target_val_dir, exist_ok=True)
    os.makedirs(target_test_dir, exist_ok=True)

    # 调用函数生成数据集和划分图片
    data_label_and_split(source_dir, target_train_dir, target_val_dir, target_test_dir)


if __name__ == '__main__':
    main()
