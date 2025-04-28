import os
import random
import shutil
from collections import defaultdict
import chardet  # 导入 chardet 库

def collect_balanced_yolo_dataset(samples_per_class, label_src_dir, image_src_dir, label_dst_dir, image_dst_dir, id_to_name_mapping):
    os.makedirs(label_dst_dir, exist_ok=True)
    os.makedirs(image_dst_dir, exist_ok=True)

    target_class_ids = set(id_to_name_mapping.keys())
    class_counts = defaultdict(int)

    # 设置固定的随机种子，保证每次洗牌的顺序一致
    random.seed(42)  # 设置随机种子

    # 所有标签文件打乱顺序
    label_files = [f for f in os.listdir(label_src_dir) if f.endswith('.txt')]
    random.shuffle(label_files)

    for label_file in label_files:
        label_path = os.path.join(label_src_dir, label_file)

        # 使用 chardet 检测文件编码
        with open(label_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # 使用检测到的编码读取文件
        try:
            with open(label_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # 如果检测到的编码仍然无法读取，可以回退到 utf-8
            print(f"警告: {label_file} 使用 {encoding} 编码读取失败，尝试使用 utf-8 编码")
            with open(label_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

        # 读取当前文件中涉及的目标类别
        current_file_target_classes = set()
        for line in lines:
            if line.strip():
                try:
                    cls_id = int(line.split()[0])
                    if cls_id in target_class_ids:
                        current_file_target_classes.add(cls_id)
                except ValueError:
                    continue

        if any(class_counts[c] < samples_per_class for c in current_file_target_classes):
            # 拷贝图片和标签文件
            image_name = os.path.splitext(label_file)[0] + '.jpg'
            src_image_path = os.path.join(image_src_dir, image_name)
            dst_image_path = os.path.join(image_dst_dir, image_name)
            dst_label_path = os.path.join(label_dst_dir, label_file)

            if os.path.exists(src_image_path):
                shutil.copyfile(label_path, dst_label_path)
                shutil.copyfile(src_image_path, dst_image_path)

                for line in lines:
                    if line.strip():
                        cls_id = int(line.split()[0])
                        if cls_id in target_class_ids:
                            class_counts[cls_id] += 1

        # 所有目标类别都满足数量时停止
        if all(class_counts[c] >= samples_per_class for c in target_class_ids):
            break

    print("\n✅ 数据收集完成！新目录下各目标类别样本数如下：")
    for cls_id in sorted(target_class_ids):
        if class_counts[cls_id] < samples_per_class:
            print(f"警告: 类别 {cls_id}（{id_to_name_mapping[cls_id]}）样本数不足！实际收集数量：{class_counts[cls_id]}")
        else:
            print(f"类别 {cls_id}（{id_to_name_mapping[cls_id]}）: {class_counts[cls_id]}")
    print("\n数据收集过程结束！")


collect_balanced_yolo_dataset(
    #---**⚠️源数据中对应类别的数据较少的情况下会出现不足要求的样本数的结果
    samples_per_class=200,  # 每个目标类别想收集的样本数

    label_src_dir=r'D:\Dataset\self-blind\coco2017\filter_datasets\val\labels',  # 原标签路径
    image_src_dir=r'D:\Dataset\self-blind\coco2017\filter_datasets\val\images',  # 原图像路径

    label_dst_dir=r'D:\Dataset\self-blind\coco2017\divide-category_datasets\val\labels',  # 新标签保存路径
    image_dst_dir=r'D:\Dataset\self-blind\coco2017\divide-category_datasets\val\images',  # 新图像保存路径

    id_to_name_mapping={
        0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 5: "bus",
        7: "truck", 9: "traffic light", 10: "fire hydrant", 11: "stop sign",
        12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
        16: "dog", 24: "backpack", 25: "umbrella", 26: "handbag", 28: "suitcase",
        39: "bottle", 41: "cup", 56: "chair", 57: "couch", 58: "potted plant",
        60: "dining table"
    }
)
