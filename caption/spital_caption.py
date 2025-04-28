import random
from collections import defaultdict
from caption_template import TEMPLATES, ORDINALS
import os
import json
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from functools import partial

# 设置根路径和阈值
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"
JSON_FILENAME = "wide/detection_GroundingDino_bbox_RAM_label_qwen_caption_confidence25.json"
RATIO_THRESHOLD = 0.7

# ---------- 工具函数 ----------
def get_bbox_extent_along_axis(corners, axis):
    values = [corner[axis] for corner in corners]
    return max(values) - min(values)

def get_min_z_from_corners(corners):
    return min(corner[2] for corner in corners)

def compute_lr_score(group, ratio_threshold):
    """
    评估一组物体是否适合进行左右排序（left-to-right），返回得分。
    score = extent_x / total_width - (1 - ratio_threshold) / N
    """
    if len(group) < 2:
        return 0.0  # 不适合排序

    all_xs = [corner[0] for obj in group for corner in obj["corners"]]
    extent_x = max(all_xs) - min(all_xs)
    widths = [get_bbox_extent_along_axis(obj["corners"], 0) for obj in group]
    total_width = sum(widths)
    n = len(group)

    score = (extent_x / total_width) - ((1 - ratio_threshold) / n) if total_width > 0 else 0.0
    return score

def compute_tb_score(group, ratio_threshold):
    """
    评估一组物体是否适合上下排序（top-to-bottom），返回得分。
    score = extent_y / total_height - (1 - ratio_threshold) / N
    """
    if len(group) < 2:
        return 0.0

    all_ys = [corner[1] for obj in group for corner in obj["corners"]]
    extent_y = max(all_ys) - min(all_ys)
    heights = [get_bbox_extent_along_axis(obj["corners"], 1) for obj in group]
    total_height = sum(heights)
    n = len(group)

    score = (extent_y / total_height) - ((1 - ratio_threshold) / n) if total_height > 0 else 0.0
    return score

def compute_fb_score(group, ratio_threshold):
    """
    评估一组物体是否适合进行前后排序（front-to-back），返回得分。
    score = extent_z / total_depth - (1 - ratio_threshold) / N
    """
    if len(group) < 2:
        return 0.0

    all_zs = [corner[2] for obj in group for corner in obj["corners"]]
    extent_z = max(all_zs) - min(all_zs)
    depths = [get_bbox_extent_along_axis(obj["corners"], 2) for obj in group]
    total_depth = sum(depths)
    n = len(group)

    score = (extent_z / total_depth) - ((1 - ratio_threshold) / n) if total_depth > 0 else 0.0
    return score

def sort_objects(group, direction):
    if direction == "left_to_right":
        return sorted(group, key=lambda o: o["position"][0])
    elif direction == "right_to_left":
        return sorted(group, key=lambda o: -o["position"][0])
    elif direction == "front_to_back":
        return sorted(group, key=lambda o: get_min_z_from_corners(o["corners"]))
    elif direction == "back_to_front":
        return sorted(group, key=lambda o: -get_min_z_from_corners(o["corners"]))
    elif direction == "top_to_bottom":
        return sorted(group, key=lambda o: o["position"][1])
    elif direction == "bottom_to_top":
        return sorted(group, key=lambda o: -o["position"][1])
    else:
        print("🚨 Invalid direction")
        return group

def generate_caption(obj, ordinal_index, direction):
    index = ordinal_index + 1
    # 获取英文序数词
    ordinal_word = ORDINALS.get(index)
    ordinal_number = f"{index}th"

    # 如果英文序数词存在，则随机用 word 或数字形式
    if ordinal_word:
        ordinal = random.choice([ordinal_word, ordinal_number])
    else:
        ordinal = ordinal_number

    template = random.choice(TEMPLATES[direction])
    return template.format(
        dense_caption=obj["dense_caption"],
        ordinal=ordinal,
        class_name=obj["class_name"]
    )

# ---------- 主函数 ----------
def process_objects(objects, ratio_threshold=0.7):
    grouped_objects = defaultdict(list)

    # 按类分组
    for obj in objects:
        obj["spatial_caption"] = []
        grouped_objects[obj["class_name"]].append(obj)

    # 每组处理
    for class_name, group in grouped_objects.items():
        if len(group) < 2:
            for obj in group:
                obj["spatial_caption"] = [obj["dense_caption"]]
            continue

        # 计算各方向的排序适配得分
        lr_score = compute_lr_score(group, ratio_threshold)
        fb_score = compute_fb_score(group, ratio_threshold)
        tb_score = compute_tb_score(group, ratio_threshold)

        directions_to_use = []

        if lr_score >= ratio_threshold:
            directions_to_use += ["left_to_right", "right_to_left"]
        if fb_score >= ratio_threshold:
            directions_to_use += ["front_to_back", "back_to_front"]
        if tb_score >= ratio_threshold:
            directions_to_use += ["top_to_bottom", "bottom_to_top"]

        if not directions_to_use:
            # 如果都不满足阈值，选得分最高的那个方向的两个方向（正向 + 反向）
            scores = {
                "lr": lr_score,
                "fb": fb_score,
                "tb": tb_score
            }
            best = max(scores, key=scores.get)
            if best == "lr":
                directions_to_use += ["left_to_right", "right_to_left"]
            elif best == "fb":
                directions_to_use += ["front_to_back", "back_to_front"]
            else:
                directions_to_use += ["top_to_bottom", "bottom_to_top"]  
        # 对每个方向进行排序并赋 caption
        for direction in directions_to_use:
            sorted_group = sort_objects(group, direction)
            for idx, obj in enumerate(sorted_group):
                caption = generate_caption(obj, idx, direction)
                if "spatial_caption" not in obj:
                    obj["spatial_caption"] = []
                obj["spatial_caption"].append(caption)

    return objects

def find_jsons_in_video(video_path, json_name):
    """在单个视频目录下查找所有 JSON 文件路径"""
    json_paths = []
    if not os.path.isdir(video_path):
        return json_paths
    try:
        for frame_folder in os.listdir(video_path):
            frame_path = os.path.join(video_path, frame_folder)
            json_path = os.path.join(frame_path, json_name)
            if os.path.isfile(json_path):
                json_paths.append(json_path)
    except Exception as e:
        print(f"❌ Error reading {video_path}: {e}")
    return json_paths

def find_all_json_files_parallel(root_dir, json_name, num_workers=None):
    video_dirs = [
        os.path.join(root_dir, d)
        for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d))
    ]

    if num_workers is None:
        num_workers = max(1, cpu_count())

    print(f"🔍 Found {len(video_dirs)} video dirs, launching {num_workers} workers to search for JSON...")

    with Pool(processes=num_workers) as pool:
        func = partial(find_jsons_in_video, json_name=json_name)
        all_json_lists = list(tqdm(pool.imap_unordered(func, video_dirs), total=len(video_dirs), desc="Searching"))

    # Flatten the nested list
    json_paths = [path for sublist in all_json_lists for path in sublist]
    return json_paths

# ---------- 单个文件的处理函数 ----------
def process_single_json(json_path, ratio_threshold):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        if "objects" not in data or not isinstance(data["objects"], list):
            return

        # 使用传入的 ratio_threshold
        data["objects"] = process_objects(data["objects"], ratio_threshold=ratio_threshold)

        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        return True
    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")
        return False

def process_all_jsons_parallel(json_paths, ratio_threshold=0.7, num_workers=None):
    if num_workers is None:
        num_workers = max(1, cpu_count())

    print(f"🚀 Launching pool with {num_workers} workers...")

    with Pool(processes=num_workers) as pool:
        # 创建部分函数
        worker_fn = partial(process_single_json, ratio_threshold=ratio_threshold)
        list(tqdm(pool.imap_unordered(worker_fn, json_paths), total=len(json_paths), desc="Processing"))

    print("✅ All JSON files processed.")

# ---------- 主入口 ----------
if __name__ == "__main__":
    all_jsons = find_all_json_files_parallel(ROOT_DIR, JSON_FILENAME)
    print(f"🔍 Found {len(all_jsons)} JSON files.")
    process_all_jsons_parallel(all_jsons, RATIO_THRESHOLD)