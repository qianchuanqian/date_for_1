import os
import glob
import fiftyone as fo

#⚠️⚠️运行前cmd运行⚠️⚠️
#taskkill /F /IM python.exe 和 taskkill /F /IM fiftyone.exe 和 taskkill /F /IM mongod.exe
#来关闭python和mongo进程，然后再运行 rd /s /q "C:\Users\Administrator\.fiftyone\var\lib\mongo"
#来删除mongo目录
#💡也可以通过执行同目录下的 kill.bat 后再运行


# 数据集目录
#dataset_dir = "D:/Dataset/self-blind/BDD100K/divide-category_datasets"     #BDD100K
dataset_dir = "D:/Dataset/self-blind/coco2017/divide-category_datasets"     #COCO2017
images_dir = os.path.join(dataset_dir, "images")
labels_dir = os.path.join(dataset_dir, "labels")
yaml_file_path = os.path.join(dataset_dir, "dataset.yaml")

# 定义类别名称
class_names = [
    "person", "bicycle", "car", "motorcycle", "bus",
    "truck", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog",
    "backpack", "umbrella", "handbag", "suitcase", "bottle",
    "cup", "chair", "couch", "potted plant", "dining table"
] #--coco2017


# 创建一个新的数据集,取名字
dataset = fo.Dataset("qianchuan_coco")

# 是否要永久保存，测试时建议设置为 False，等测试通过再设为 True
dataset.persistent = True  # 设置为 False 以便测试时不会永久保存

# 生成 annotations 字典
annotations = {}

# 遍历 train 和 val 文件夹
for split in ['train', 'val']:
    image_folder = os.path.join(images_dir, split)
    label_folder = os.path.join(labels_dir, split)

    # 检查图像和标签文件夹是否存在
    if not os.path.exists(image_folder):
        print(f"图像文件夹不存在：{image_folder}")
        continue  # 如果文件夹不存在，跳过该分割
    if not os.path.exists(label_folder):
        print(f"标签文件夹不存在：{label_folder}")
        continue  # 如果文件夹不存在，跳过该分割

    # 获取每个图像的路径
    for image_file in os.listdir(image_folder):
        if image_file.endswith(('.jpg', '.png')):
            image_path = os.path.join(image_folder, image_file)
            label_path = os.path.join(label_folder, os.path.splitext(image_file)[0] + '.txt')

            # 如果对应的标签文件存在
            if os.path.exists(label_path):
                # 读取标签文件并生成标注信息
                with open(label_path, 'r') as label_file:
                    objects = [
                        {"bbox": [float(coord) for coord in line.strip().split()[1:]],
                         "label": class_names[int(line.strip().split()[0])]}
                        for line in label_file.readlines()
                    ]
                    # 将图像路径和对应的标注信息添加到字典
                    annotations[image_path] = objects

# 打印生成的 annotations
print(f"Annotations generated for {len(annotations)} images.")

# 使用glob创建样本
# 匹配 train 和 val 图像
image_patterns = [os.path.join(images_dir, split, "*.jpg") for split in ['train', 'val']]

samples = []
for pattern in image_patterns:
    for filepath in glob.glob(pattern):
        sample = fo.Sample(filepath=filepath)

        # Convert detections to FiftyOne format
        detections = []
        if filepath in annotations:  # 仅当路径在 annotations 中时处理
            for obj in annotations[filepath]:
                label = obj["label"]

                # Bounding box coordinates should be relative values
                # in [0, 1] in the following format:
                # [top-left-x, top-left-y, width, height]
                bounding_box = obj["bbox"]

                detections.append(
                    fo.Detection(label=label, bounding_box=bounding_box)
                )

            # Store detections in a field name of your choice
            sample["ground_truth"] = fo.Detections(detections=detections)

        samples.append(sample)

# 确保 dataset.yaml 文件在正确的位置，并且路径正确
if os.path.exists(yaml_file_path):
    print(f"Found dataset.yaml at {yaml_file_path}. Loading dataset...")
else:
    print(f"dataset.yaml 文件未找到，请确保文件在 {yaml_file_path} 路径下。")

# 添加样本到数据集中
dataset.add_samples(samples)

# 打印数据集信息
print(dataset)

# 查看数据集的前几项
print(dataset.head())

# 启动FiftyOne应用
session = fo.launch_app(dataset)

# 等待应用关闭
session.wait()
