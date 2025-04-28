import os
import json
from collections import defaultdict
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# 根目录
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

def compute_iou(box1, box2):
    """计算两个 bbox 的 IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = max(0, box1[2] - box1[0]) * max(0, box1[3] - box1[1])
    area2 = max(0, box2[2] - box2[0]) * max(0, box2[3] - box2[1])
    union_area = area1 + area2 - inter_area
    return inter_area / union_area if union_area != 0 else 0

def process_file(file_path):
    """处理单个 detection JSON 文件，清除重复 xyxy 匹配"""
    try:
        with open(file_path, 'r') as f:
            objects = json.load(f)
    except Exception as e:
        return f"❌ Error reading {file_path}: {e}"

    grouped = defaultdict(list)
    for obj in objects:
        xyxy = tuple(obj.get("xyxy", []))
        if len(xyxy) == 4:
            grouped[xyxy].append(obj)

    final_objects = []
    for xyxy, group in grouped.items():
        if len(group) == 1:
            final_objects.append(group[0])
        else:
            best_obj = None
            best_iou = -1
            for obj in group:
                if "box_2d_rend" in obj and "xyxy" in obj:
                    iou = compute_iou(obj["box_2d_rend"], obj["xyxy"])
                    if iou > best_iou:
                        best_iou = iou
                        best_obj = obj
            if best_obj:
                final_objects.append(best_obj)

    try:
        with open(file_path, 'w') as f:
            json.dump(final_objects, f, indent=2)
    except Exception as e:
        return f"❌ Error writing {file_path}: {e}"

    return f"✅ {os.path.basename(file_path)}: kept {len(final_objects)} of {len(objects)} objects"

def find_all_json_files():
    """查找所有 detection_with_GroungingDino_bbox_RAM_label_conf_20.json 文件"""
    target_files = []
    for scene_id in os.listdir(ROOT_DIR):
        scene_path = os.path.join(ROOT_DIR, scene_id)
        if not os.path.isdir(scene_path):
            continue
        for frame_id in os.listdir(scene_path):
            wide_path = os.path.join(scene_path, frame_id, "wide")
            if not os.path.isdir(wide_path):
                continue
            file_path = os.path.join(wide_path, "detection_with_GroungingDino_bbox_RAM_label_conf_20.json")
            if os.path.exists(file_path):
                target_files.append(file_path)
    return target_files

def main():
    all_files = find_all_json_files()
    print(f"🚀 Found {len(all_files)} files to process.")

    with Pool(processes=min(cpu_count(), 128)) as pool:
        results = list(tqdm(pool.imap_unordered(process_file, all_files), total=len(all_files)))

    print("\n📋 Summary:")
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
