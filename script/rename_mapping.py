import os
import shutil
import json


def load_mapping(mapping_path):
    """加载映射字典"""
    with open(mapping_path, 'r') as file:
        return json.load(file)


def update_labels_and_rename(images_dir, labels_dir, output_images_dir, output_labels_dir, old_mapping, new_mapping):
    """根据映射字典更新标签，重命名图片和标签文件，并将它们复制到新的目录"""
    if not os.path.exists(output_images_dir):
        os.makedirs(output_images_dir)
    if not os.path.exists(output_labels_dir):
        os.makedirs(output_labels_dir)

    image_files = sorted(os.listdir(images_dir))
    label_files = sorted(os.listdir(labels_dir))

    # 确保图片和标签数量一致
    if len(image_files) != len(label_files):
        print("图片和标签数量不一致，请检查输入目录。")
        return

    # 遍历每一对图片和标签文件
    for idx, (image_file, label_file) in enumerate(zip(image_files, label_files)):
        # 确保文件扩展名是正确的
        if not image_file.lower().endswith(('.jpg', '.png', '.jpeg')) or not label_file.lower().endswith('.txt'):
            continue

        # 构建标签文件路径
        label_path = os.path.join(labels_dir, label_file)
        with open(label_path, 'r') as label:
            lines = label.readlines()

        # 更新标签文件中的类别映射
        updated_lines = []
        for line in lines:
            parts = line.strip().split()
            old_class = int(parts[0])  # 类别索引
            # 从 old_mapping 中获取类名
            old_class_name = old_mapping.get(old_class)
            if old_class_name is not None:
                # 在 new_mapping 中查找 old_class_name 对应的新的类名
                for new_class, new_class_name in new_mapping.items():
                    if new_class_name == old_class_name:
                        # 找到对应的新类名，将新类别索引写入
                        updated_lines.append(f"{new_class} " + " ".join(parts[1:]) + "\n")
                        break
            else:
                # 如果没有找到对应的类名，保持原样
                updated_lines.append(line)

        # 创建新的标签文件路径
        new_label_filename = f"{str(idx + 1).zfill(7)}.txt"
        new_label_path = os.path.join(output_labels_dir, new_label_filename)

        # 将更新后的标签写入新文件
        with open(new_label_path, 'w') as new_label_file:
            new_label_file.writelines(updated_lines)

        # 复制图片文件，并重命名
        image_path = os.path.join(images_dir, image_file)
        new_image_filename = f"{str(idx + 1).zfill(7)}" + os.path.splitext(image_file)[1]
        new_image_path = os.path.join(output_images_dir, new_image_filename)

        shutil.copy(image_path, new_image_path)
        print(f"处理完成: {image_file} -> {new_image_filename}, {label_file} -> {new_label_filename}")




if __name__ == "__main__":
    # 输入路径（根据实际情况填写）
    # 输入的是 divide-category_datasets
    images_dir = "D:\\Dataset\\self-blind\\BDD100K\\divide-category_datasets\\images\\train"
    labels_dir = "D:\\Dataset\\self-blind\\BDD100K\\divide-category_datasets\\labels\\train"
    output_images_dir = "D:\\Dataset\\self-blind\\final_datasets\\bdd\\train\\images"
    output_labels_dir = "D:\\Dataset\\self-blind\\final_datasets\\bdd\\train\\labels"

    # 旧的和新的映射字典（示例字典）
    # 选用当前处理的数据集的mapping
    # old_mapping = {
    #     0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 5: "bus",
    #     7: "truck", 9: "traffic light", 10: "fire hydrant", 11: "stop sign",
    #     12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
    #     16: "dog", 24: "backpack", 25: "umbrella", 26: "handbag", 28: "suitcase",
    #     39: "bottle", 41: "cup", 56: "chair", 57: "couch", 58: "potted plant",
    #     60: "dining table"}# 👈COCO2017

    old_mapping = {
        0: "traffic sign",
        1: "traffic light",
        2: "person",
        3: "rider",
        4: "car",
        5: "truck",
        6: "bus",
        7: "train",
        8: "motorcycle",
        9: "bicycle"
    }# 👈BDD100K

    new_mapping = {
        0: 'person',
        1: 'bicycle',
        2: 'car',
        3: 'motorcycle',
        4: 'bus',
        5: 'truck',
        6: 'traffic light',
        7: 'fire hydrant',
        8: 'stop sign',
        9: 'parking meter',
        10: 'bench',
        11: 'bird',
        12: 'cat',
        13: 'dog',
        14: 'backpack',
        15: 'umbrella',
        16: 'handbag',
        17: 'suitcase',
        18: 'bottle',
        19: 'cup',
        20: 'chair',
        21: 'couch',
        22: 'potted plant',
        23: 'dining table',
        24: 'traffic sign',
        25: 'rider'
    }

    update_labels_and_rename(images_dir, labels_dir, output_images_dir, output_labels_dir, old_mapping, new_mapping)
