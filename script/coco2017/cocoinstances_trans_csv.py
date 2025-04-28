import json
import csv
import re

def load_clean_json(json_path):
    """尝试以兼容方式读取并清洗 JSON 内容"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        with open(json_path, 'r', encoding='mbcs', errors='ignore') as f:
            raw_text = f.read()
        # 去除非法控制字符
        cleaned_text = re.sub(r'[\x00-\x1F]+', '', raw_text)
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解码失败：{e}")
        raise

def coco_images_to_csv(json_path, csv_path):
    data = load_clean_json(json_path)

    licenses = {lic["id"]: lic["name"] for lic in data.get("licenses", [])}
    images = data.get("images", [])

    if not images:
        print("⚠️ 没有找到 images 字段内容，可能不是 COCO 格式。")
        return

    csv_rows = []
    for img in images:
        license_id = img.get("license")
        csv_rows.append({
            "id": img.get("id"),
            "file_name": img.get("file_name"),
            "width": img.get("width"),
            "height": img.get("height"),
            "license": license_id,
            "license_name": licenses.get(license_id, "Unknown"),
            "date_captured": img.get("date_captured"),
            "coco_url": img.get("coco_url"),
            "flickr_url": img.get("flickr_url")
        })

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✅ 共处理 {len(csv_rows)} 张图片，结果已保存到 {csv_path}")

#目标检测需要的只有instances的labels
# 示例调用
#train文件
# coco_images_to_csv(
#     'D:\\Dataset\\coco2017_od\\annotations\\instances_train2017.json',
#     'D:\\Dataset\\coco2017_od\\annotations\\output_csv\\instances_train2017.csv'
# )

# val文件
coco_images_to_csv(
    'D:\\Dataset\\coco2017_od\\annotations\\instances_val2017.json',
    'D:\\Dataset\\coco2017_od\\annotations\\output_csv\\instances_val2017.csv'
)
