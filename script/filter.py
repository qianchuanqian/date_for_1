#2-进行类别过滤
import os
import shutil

# 类别映射（YOLO格式，从0开始）
all_classes_dict = {
    "person": 0, "bicycle": 1, "car": 2, "motorcycle": 3, "airplane": 4,
    "bus": 5, "train": 6, "truck": 7, "boat": 8, "traffic light": 9,
    "fire hydrant": 10, "stop sign": 11, "parking meter": 12, "bench": 13,
    "bird": 14, "cat": 15, "dog": 16, "horse": 17, "sheep": 18, "cow": 19,
    "elephant": 20, "bear": 21, "zebra": 22, "giraffe": 23, "backpack": 24,
    "umbrella": 25, "handbag": 26, "tie": 27, "suitcase": 28, "frisbee": 29,
    "skis": 30, "snowboard": 31, "sports ball": 32, "kite": 33, "baseball bat": 34,
    "baseball glove": 35, "skateboard": 36, "surfboard": 37, "tennis racket": 38,
    "bottle": 39, "wine glass": 40, "cup": 41, "fork": 42, "knife": 43,
    "spoon": 44, "bowl": 45, "banana": 46, "apple": 47, "sandwich": 48,
    "orange": 49, "broccoli": 50, "carrot": 51, "hot dog": 52, "pizza": 53,
    "donut": 54, "cake": 55, "chair": 56, "couch": 57, "potted plant": 58,
    "bed": 59, "dining table": 60, "toilet": 61, "tv": 62, "laptop": 63,
    "mouse": 64, "remote": 65, "keyboard": 66, "cell phone": 67, "microwave": 68,
    "oven": 69, "toaster": 70, "sink": 71, "refrigerator": 72, "book": 73,
    "clock": 74, "vase": 75, "scissors": 76, "teddy bear": 77, "hair drier": 78,
    "toothbrush": 79
}

def filter_yolo_labels(
    label_dir,
    image_dir,
    output_label_dir,
    output_image_dir,
    keep_class_ids  # 👈 修改为编号列表输入
):
    os.makedirs(output_label_dir, exist_ok=True)
    os.makedirs(output_image_dir, exist_ok=True)

    deleted_labels = 0
    deleted_images = 0

    for filename in os.listdir(label_dir):
        if not filename.endswith(".txt"):
            continue

        label_path = os.path.join(label_dir, filename)
        with open(label_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.strip() == "":
                continue
            class_id = int(line.strip().split()[0])
            if class_id in keep_class_ids:
                new_lines.append(line.strip())
            else:
                deleted_labels += 1

        if new_lines:
            # 保存新标签
            new_label_path = os.path.join(output_label_dir, filename)
            with open(new_label_path, 'w') as f:
                f.write('\n'.join(new_lines))
            # 拷贝图像
            image_filename = os.path.splitext(filename)[0] + '.jpg'  # 根据图像后缀可修改
            image_src = os.path.join(image_dir, image_filename)
            image_dst = os.path.join(output_image_dir, image_filename)
            if os.path.exists(image_src):
                shutil.copy(image_src, image_dst)
        else:
            # 删除图片（不拷贝）
            deleted_images += 1

    print(f"处理完成！删除标签数：{deleted_labels}，删除图片数：{deleted_images}")


#调用
#---**⚠️可能会出现某个output文件夹什么都没生成的情况。请检查文件名字是否正确特别是label_dir和image_dir
if __name__ == "__main__":
    label_dir = "D:\\Dataset\\retry\\search\\val\\labels"
    image_dir = "D:\\Dataset\\retry\\search\\val\\images"
    output_label_dir = "D:\\Dataset\\retry\\fifter\\labels"
    output_image_dir = "D:\\Dataset\\retry\\fifter\\images"

    keep_class_ids = [0, 1, 2, 3, 5,
                      7, 9, 10, 11,
                      12, 13, 14, 15,
                      16, 24, 25, 26,
                      28, 39, 41,
                      56, 57, 58, 60]  # 👈盲人出行  # 👈 使用编号方式保留

    filter_yolo_labels(label_dir, image_dir, output_label_dir, output_image_dir, keep_class_ids)

