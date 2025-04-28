import json
import os

# 类别映射（你需要根据实际的类别文件来调整）
category_mapping = {
    "traffic sign": 0,
    "traffic light": 1,
    "person": 2,
    "rider": 3,
    "car": 4,
    "truck": 5,
    "bus": 6,
    "train": 7,
    "motorcycle": 8,
    "bicycle": 9,
}


def convert_to_yolo_format_single_file(json_path, image_width, image_height, output_txt_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    yolo_lines = []

    # 提取每一帧的物体标签
    for frame in data.get("frames", []):
        for obj in frame.get("objects", []):
            if "box2d" not in obj:  # 如果没有box2d，跳过
                continue

            category = obj["category"]
            if category not in category_mapping:
                continue

            cls_id = category_mapping[category]
            box = obj["box2d"]

            # 获取box2d的坐标
            x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]

            # 将坐标转换为相对比例
            x_center = ((x1 + x2) / 2) / image_width
            y_center = ((y1 + y2) / 2) / image_height
            width = (x2 - x1) / image_width
            height = (y2 - y1) / image_height

            # 生成YOLO格式的标签
            yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    if yolo_lines:
        with open(output_txt_path, 'w') as out_f:
            out_f.write("\n".join(yolo_lines))


# 主程序
if __name__ == "__main__":
    # 设置路径
    bdd_json_dir = 'D:\\Dataset\\BDD10K_dataset\\bdd100k_labels\\100k\\val'  # 每张图片一个 JSON 文件的路径
    output_folder = 'D:\\Dataset\\self-blind\\BDD100K\\new_dataset\\val\\labels'

    image_width = 1280
    image_height = 720

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(bdd_json_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(bdd_json_dir, filename)
            output_txt_name = filename.replace(".json", ".txt")
            output_txt_path = os.path.join(output_folder, output_txt_name)
            convert_to_yolo_format_single_file(json_path, image_width, image_height, output_txt_path)
