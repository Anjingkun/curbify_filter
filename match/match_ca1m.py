import os
import json
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# 配置路径
LABEL_ROOT = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_20_bbox_label_confidence_25"
NO_LABEL_ROOT = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"
IOU_THRESHOLD = 0.65

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

def match_boxes(label_boxes, no_label_boxes):
    """匹配两个列表中的 bbox，返回带 label 的 no_label_box"""
    matched = []
    for box in no_label_boxes:
        box_rend = box.get("box_2d_rend", None)
        if not box_rend:
            continue

        best_iou = 0
        best_name = None
        best_xyxy = None
        best_confidence = None
        for label in label_boxes:
            label_box = label["xyxy"]
            iou = compute_iou(box_rend, label_box)
            if iou > best_iou:
                best_iou = iou
                best_name = label["class_name"]
                best_xyxy = label_box
                best_confidence = label["confidence"]

        if best_iou >= IOU_THRESHOLD:
            box["class_name"] = best_name
            box["xyxy"] = best_xyxy
            box["confidence"] = best_confidence

            matched.append(box)

    return matched

def process_single_file(task):
    """处理单个文件匹配任务"""
    label_file, scene_id, frame_id = task

    try:
        with open(label_file, 'r') as f:
            label_boxes = json.load(f)
    except:
        return f"❌ 读取标签失败: {label_file}"

    instance_file = os.path.join(NO_LABEL_ROOT, scene_id, frame_id, "wide", "instances.json")
    if not os.path.exists(instance_file):
        return f"❌ 无标签文件不存在: {instance_file}"

    try:
        with open(instance_file, 'r') as f:
            no_label_boxes = json.load(f)
    except:
        return f"❌ 读取无标签失败: {instance_file}"

    matched = match_boxes(label_boxes, no_label_boxes)

    output_dir = os.path.join(NO_LABEL_ROOT, scene_id, frame_id, "wide")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "detection_with_GroungingDino_bbox_RAM_label_conf_20.json")

    with open(output_file, 'w') as f:
        json.dump(matched, f, indent=2)

    return f"✅ 匹配成功 Scene:{scene_id}, Frame:{frame_id}, 物体数:{len(matched)}"

def collect_tasks():
    """遍历所有路径，收集任务列表"""
    tasks = []
    for machine_id in range(8):
        machine_path = os.path.join(LABEL_ROOT, str(machine_id))
        if not os.path.isdir(machine_path):
            continue

        for scene_id in os.listdir(machine_path):
            scene_path = os.path.join(machine_path, scene_id)
            if not os.path.isdir(scene_path):
                continue

            for frame_file in os.listdir(scene_path):
                if not frame_file.endswith(".json"):
                    continue

                frame_id = frame_file[:-5]  # 去掉 .json 后缀
                label_file = os.path.join(scene_path, frame_file)
                tasks.append((label_file, scene_id, frame_id))
    return tasks

def main():
    tasks = collect_tasks()
    print(f"🧠 共收集到 {len(tasks)} 个匹配任务，启动多进程处理...")

    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(process_single_file, tasks), total=len(tasks)))

    print("\n📋 执行结果:")
    for res in results:
        print(res)

if __name__ == "__main__":
    main()