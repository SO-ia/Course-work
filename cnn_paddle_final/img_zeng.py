import os
import random
from PIL import Image
import imgaug.augmenters as iaa
from tqdm import tqdm

# 数据增强函数
def augment_image(image):
    seq = iaa.Sequential([
        iaa.Affine(rotate=(-20, 20)),  # 随机旋转
        iaa.Fliplr(0.5),              # 随机水平翻转
        iaa.Crop(percent=(0, 0.2)),   # 随机裁剪
        iaa.GaussianBlur(sigma=(0, 1.0))  # 随机高斯模糊
    ])
    return seq(image=image)

# 数据增强处理函数
def augment_dataset(category_folder, target_count):
    images = os.listdir(category_folder)
    current_count = len(images)
    if current_count >= target_count:
        print(f"{category_folder} 已经达到目标数量，无需扩展")
        return

    print(f"开始扩展 {category_folder}，当前数量: {current_count}，目标数量: {target_count}")
    images_to_generate = target_count - current_count

    for _ in tqdm(range(images_to_generate), desc=f"扩展 {category_folder}"):
        # 随机选择一张图片进行增强
        img_name = random.choice(images)
        img_path = os.path.join(category_folder, img_name)
        image = Image.open(img_path).convert("L")  # 转为灰度图像
        image = np.array(image)  # 转为数组

        # 数据增强
        augmented_image = augment_image(image)
        augmented_image = Image.fromarray(augmented_image)

        # 保存增强后的图片
        new_image_name = f"aug_{random.randint(100000, 999999)}.jpg"
        augmented_image.save(os.path.join(category_folder, new_image_name))

# 主函数
def main():
    dataset_path = "e:/pycharm/cnn/data/facial expression"  # 替换为你的数据集路径
    categories = {
        "Angry": 8000,
        "Disgust": 8000,
        "Fear": 8000,
        "Happy": 8989,  # Happy 类别无需扩展
        "Neutral": 8000,
        "Sad": 8000,
        "Surprise": 8000,
    }

    for category, target_count in categories.items():
        category_folder = os.path.join(dataset_path, category)
        augment_dataset(category_folder, target_count)

if __name__ == "__main__":
    import numpy as np  # 避免在开头导入影响阅读
    main()
