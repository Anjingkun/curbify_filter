import os
import json
from pathlib import Path
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from functools import partial
from typing import List

# 设置根目录和 JSON 文件名
ROOT_DIR = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20")
JSON_NAME = "detection_GroundingDino_bbox_RAM_label_qwen_caption_confidence25.json"

def find_jsons_in_video_dir(video_dir: Path, json_name: str) -> List[Path]:
    """在一个视频目录下查找所有 wide/xxx.json 文件"""
    results = []
    try:
        for frame_dir in video_dir.iterdir():
            json_path = frame_dir / "wide" / json_name
            if json_path.exists():
                results.append(json_path)
    except Exception as e:
        print(f"❌ Error in {video_dir}: {e}")
    return results

def find_all_json_files_parallel(root_dir: Path, json_name: str, num_workers: int = None) -> List[Path]:
    """多进程查找所有帧目录中的目标 JSON 文件"""
    video_dirs = [d for d in root_dir.iterdir() if d.is_dir()]

    if num_workers is None:
        num_workers = max(1, cpu_count())

    print(f"🔍 Found {len(video_dirs)} video dirs. Using {num_workers} workers to search JSON files...")
    json_paths = []
    with Pool(processes=num_workers) as pool:
        func = partial(find_jsons_in_video_dir, json_name=json_name)
        for json_list in tqdm(pool.imap_unordered(func, video_dirs), total=len(video_dirs), desc="Scanning"):
            json_paths.extend(json_list)
    print(f"✅ Total JSON files found: {len(json_paths)}")
    return json_paths

def resize_bbox(bbox):
    """将 bbox 缩小为原来的 1/2"""
    return [coord / 2 for coord in bbox]

def process_single_json(json_path: Path, overwrite=True):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        # 检查 objects
        if "objects" not in data or not isinstance(data["objects"], list):
            print("❌ No 'objects' found in the JSON file.")
            return False

        # 修改每个 object 的 bbox
        for obj in data["objects"]:
            if "xyxy" in obj and isinstance(obj["xyxy"], list) and len(obj["xyxy"]) == 4:
                obj["bbox_resized"] = resize_bbox(obj["xyxy"])
            else:
                print(f"❌ Invalid bbox format in {json_path}")

        # 写回文件
        if overwrite:
            output_path = json_path
        else:
            output_path = json_path.with_name(json_path.stem + "_resized.json")

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        return True

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")
        return False

def main():
    json_paths = find_all_json_files_parallel(ROOT_DIR, JSON_NAME)
    print(f"🔍 找到 {len(json_paths)} 个 JSON 文件，开始多进程处理...")

    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(process_single_json, json_paths), total=len(json_paths)))

    success = sum(results)
    print(f"✅ 完成处理：成功 {success}，失败 {len(results) - success}")

if __name__ == "__main__":
    main()