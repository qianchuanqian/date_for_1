#由于输出的BDD100K的image的顺序有点对不上，于是进行脚本确定标签所包含的图片
#通用于所有和转换yolo标签后和原来的图片数量对不上的情况

import os
import shutil
from pathlib import Path

def is_image_file(file):
    return file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']

def copy_yolo_pairs(images_dir, labels_dir, dst_dir):
    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)
    dst_dir = Path(dst_dir)

    out_images = dst_dir / "images"
    out_labels = dst_dir / "labels"

    out_images.mkdir(parents=True, exist_ok=True)
    out_labels.mkdir(parents=True, exist_ok=True)

    count = 0

    for img_file in images_dir.rglob("*"):
        if is_image_file(img_file):
            label_file = labels_dir / (img_file.stem + ".txt")
            if label_file.exists():
                shutil.copyfile(img_file, out_images / img_file.name)
                shutil.copyfile(label_file, out_labels / label_file.name)
                print(f"✓ 拷贝: {img_file.name}")
                count += 1
            else:
                print(f"✗ 缺少标签: {img_file.name}")

    print(f"\n完成：共复制了 {count} 对 image-label。输出目录：{dst_dir}")

# 示例用法
if __name__ == "__main__":
    images_path = 'D:\\Dataset\\coco2017_od\\val2017'  # 替换为你的图片路径
    labels_path = 'D:\\Dataset\\retry\\yolo_labels\\val'  # 替换为你的labels路径
    output_path = "D:\\Dataset\\retry\\search\\val"  # 输出目录
    copy_yolo_pairs(images_path, labels_path, output_path)

