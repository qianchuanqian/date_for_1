#用于存储各类转化为yolo格式的数据集的 mapping dict

#-------------------------------$coco2017$-------------------------------#
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

keep_class_ids = [0, 1, 2, 3, 5,
                  7, 9, 10, 11,
                  12, 13, 14, 15,
                  16, 24, 25, 26,
                  28, 39, 41,
                  56, 57, 58, 60]  # 👈盲人出行

#divide_category要用的mapping
id_to_name_mapping = {
    0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 5: "bus",
    7: "truck", 9: "traffic light", 10: "fire hydrant", 11: "stop sign",
    12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
    16: "dog", 24: "backpack", 25: "umbrella", 26: "handbag", 28: "suitcase",
    39: "bottle", 41: "cup", 56: "chair", 57: "couch", 58: "potted plant",
    60: "dining table"
}

#用于fiftyone可视化数据集的dataset.yaml 取消注释后加到.yaml文件里
# names:
#   0: "person"
#   1: "bicycle"
#   2: "car"
#   3: "motorcycle"
#   5: "bus"
#   7: "truck"
#   9: "traffic light"
#   10: "fire hydrant"
#   11: "stop sign"
#   12: "parking meter"
#   13: "bench"
#   14: "bird"
#   15: "cat"
#   16: "dog"
#   24: "backpack"
#   25: "umbrella"
#   26: "handbag"
#   28: "suitcase"
#   39: "bottle"
#   41: "cup"
#   56: "chair"
#   57: "couch"
#   58: "potted plant"
#   60: "dining table"


#-------------------------------$BDD100K$-------------------------------#
all_classes_dict = {
    "traffic sign": 0,
    "traffic light": 1,
    "person": 2,
    "rider": 3,
    "car": 4,
    "truck": 5,
    "bus": 6,
    "train": 7,
    "motorcycle": 8,
    "bicycle": 9
}

keep_class_ids = [0,1,2,3,4,5,6,8,9]  # 👈盲人出行


#divide_category要用的mapping
id_to_name_mapping = {
    0: "traffic sign",
    1: "traffic light",
    2: "person",
    3: "rider",
    4: "car",
    5: "truck",
    6: "bus",
    8: "motorcycle",
    9: "bicycle"
}

#----用于fiftyone可视化数据集的dataset.yaml  取消注释后加到.yaml文件里
# names:
#   0: "traffic sign"
#   1: "traffic light"
#   2: "person"
#   3: "rider"
#   4: "car"
#   5: "truck"
#   6: "bus"
#   7: "train"
#   8: "motorcycle"
#   9: "bicycle"

#----用于fiftyone可视化数据集的加载脚本里的类别名列表
class_names = [
    "traffic sign", "traffic light", "person", "rider", "car",
    "truck", "bus", "train", "motorcycle", "bicycle"
] #--BDD100K