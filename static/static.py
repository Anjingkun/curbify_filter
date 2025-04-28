import os
import json
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# 根目录
ROOT = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def collect_tasks():
    """遍历所有 scene/frame，收集每帧的路径任务"""
    tasks = []
    for scene_id in os.listdir(ROOT):
        scene_path = os.path.join(ROOT, scene_id)
        if not os.path.isdir(scene_path):
            continue

        for frame_id in os.listdir(scene_path):
            wide_path = os.path.join(scene_path, frame_id, "wide")
            if not os.path.isdir(wide_path):
                continue

            instance_file = os.path.join(wide_path, "instances.json")
            detection_file = os.path.join(wide_path, "detection_with_GroungingDino_bbox_RAM_label_conf_20.json")
            tasks.append((instance_file, detection_file))

    return tasks

def process_frame(task):
    """单帧处理函数，返回 (原始物体数, 匹配后物体数)"""
    instance_file, detection_file = task
    instances = load_json(instance_file)
    detections = load_json(detection_file)
    return (len(instances), len(detections))

def main():
    tasks = collect_tasks()
    print(f"📦 共 {len(tasks)} 帧，使用 {cpu_count()} 核心并行统计...\n")

    total_before = 0
    total_after = 0

    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(process_frame, tasks), total=len(tasks)))

    for before, after in results:
        total_before += before
        total_after += after

    total_frames = len(results)
    avg_per_frame = total_after / total_frames if total_frames > 0 else 0
    retain_rate = total_after / total_before * 100 if total_before > 0 else 0

    print("📊 匹配结果汇总：")
    print(f"✅ 总帧数：{total_frames}")
    print(f"✅ 原始总物体数：{total_before}")
    print(f"✅ 匹配后总物体数：{total_after}")
    print(f"✅ 平均每帧保留物体数：{avg_per_frame:.2f}")
    print(f"✅ 总体保留率：{retain_rate:.2f}%")

if __name__ == "__main__":
    main()