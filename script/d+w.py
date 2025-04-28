import os
import random
import shutil
from pathlib import Path


def shuffle_and_split_data(input_dir, train_ratio, val_ratio, test_ratio):
    """对图片和标签文件进行洗牌，并根据比例划分为train、val、test"""

    # 检查比例是否合理
    total_ratio = train_ratio + val_ratio + test_ratio
    if total_ratio != 1.0:
        print("比例之和必须为1.0")
        return

    # 设置路径
    images_dir = os.path.join(input_dir, "images")
    labels_dir = os.path.join(input_dir, "labels")
    class_file = os.path.join(input_dir, "classes.txt")

    # 创建输出目录
    output_dir = os.path.join(input_dir, "split_data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取 classes.txt 文件，获取类别信息
    with open(class_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # 获取 images 和 labels 文件夹中的所有图片和标签文件
    image_files = sorted(os.listdir(images_dir))
    label_files = sorted(os.listdir(labels_dir))

    # 确保图片和标签文件数目相同
    if len(image_files) != len(label_files):
        print("图片和标签文件数量不一致！")
        return

    # 洗牌：将文件随机打乱
    combined_files = list(zip(image_files, label_files))
    random.shuffle(combined_files)
    image_files, label_files = zip(*combined_files)

    # 计算划分的数量
    total_files = len(image_files)
    train_count = int(total_files * train_ratio)
    val_count = int(total_files * val_ratio)
    test_count = total_files - train_count - val_count  # 剩余的归为测试集

    # 创建划分子目录
    for split in ['train', 'val', 'test']:
        for sub_dir in ['images', 'labels']:
            os.makedirs(os.path.join(output_dir, split, sub_dir), exist_ok=True)

    # 将文件按照比例分配
    for i, (image_file, label_file) in enumerate(zip(image_files, label_files)):
        if i < train_count:
            split = 'train'
        elif i < train_count + val_count:
            split = 'val'
        else:
            split = 'test'

        # 复制文件到对应目录
        shutil.copy(os.path.join(images_dir, image_file), os.path.join(output_dir, split, 'images', image_file))
        shutil.copy(os.path.join(labels_dir, label_file), os.path.join(output_dir, split, 'labels', label_file))

    print(f"数据集已成功划分为 train: {train_count}, val: {val_count}, test: {test_count}")
    print(f"划分后的数据集保存在 {output_dir} 目录下。")


if __name__ == "__main__":
    # 输入目录和比例
    input_dir = "D:\\Dataset\\d+w_finallll_dataset"  #请输入包含 images、labels 和 class.txt 的目录路径
    train_ratio = float(input("请输入训练集比例（例如 0.7）: "))
    val_ratio = float(input("请输入验证集比例（例如 0.2）: "))
    test_ratio = float(input("请输入测试集比例（例如 0.1）: "))

    # 调用函数进行操作
    shuffle_and_split_data(input_dir, train_ratio, val_ratio, test_ratio)
