import os
import json
from pycocotools.coco import COCO
#映射从0开始

# 定义 COCO 格式和 YOLO 格式的映射
def coco_to_yolo(annotation, img_width, img_height, category_id_map):
    x_min, y_min, width, height = annotation['bbox']
    x_center = (x_min + width / 2) / img_width
    y_center = (y_min + height / 2) / img_height
    norm_width = width / img_width
    norm_height = height / img_height

    # 将 COCO 的 category_id 映射为连续的 0-based index
    yolo_category_id = category_id_map[annotation['category_id']]

    return [yolo_category_id, x_center, y_center, norm_width, norm_height]


def convert_coco_to_yolo(coco_json_path, image_folder, output_folder):
    coco = COCO(coco_json_path)
    img_ids = coco.getImgIds()

    # 获取所有类别，并构建 category_id → 连续 index 的映射（从 0 开始）
    categories = coco.loadCats(coco.getCatIds())
    category_id_map = {cat['id']: idx for idx, cat in enumerate(categories)}

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    for img_id in img_ids:
        img_info = coco.loadImgs(img_id)[0]
        img_width, img_height = img_info['width'], img_info['height']

        ann_ids = coco.getAnnIds(imgIds=img_id)
        annotations = coco.loadAnns(ann_ids)

        yolo_labels = []
        for annotation in annotations:
            yolo_label = coco_to_yolo(annotation, img_width, img_height, category_id_map)
            yolo_labels.append(" ".join(map(str, yolo_label)))

        if yolo_labels:
            yolo_filename = os.path.splitext(img_info['file_name'])[0] + '.txt'
            yolo_filepath = os.path.join(output_folder, yolo_filename)
            with open(yolo_filepath, 'w') as f:
                f.write("\n".join(yolo_labels))
            print(f"Saved YOLO labels for {img_info['file_name']}")


if __name__ == "__main__":
    # 设置路径
    coco_json_path = 'D:\\Dataset\\coco2017_od\\annotations\\instances_val2017.json'
    image_folder = 'D:\\Dataset\\coco2017_od\\val2017'
    output_folder = 'D:\\Dataset\\self-blind\\coco2017\\output_yolo\\coco_val'

    convert_coco_to_yolo(coco_json_path, image_folder, output_folder)
