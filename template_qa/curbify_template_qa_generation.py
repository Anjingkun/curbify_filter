import os
import json
from multiprocessing import Pool, cpu_count
from pathlib import Path
from tqdm import tqdm
from prompt import PromptGenerator
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import time

# 目标 JSON 文件名（检测文件）
TARGET_FILENAME = "detections_with_bbox_label_qwen_spital_caption_mask_pcd.json"

def check_and_clean_template_qa(frame_dir: str, filename) -> str | None:
    """
    检查并尝试加载 frame_dir/template_qa.json。
    如果损坏则删除，返回被删除的路径；否则返回 None。
    """
    json_path = Path(frame_dir) / filename
    if not json_path.exists():
        return None

    try:
        with open(json_path, "r") as f:
            json.load(f)
    except Exception as e:
        print(f"⚠️ Invalid JSON: {json_path} — {e}. Deleting...")
        try:
            json_path.unlink()
            return str(json_path)
        except Exception as delete_error:
            print(f"❌ Failed to delete {json_path}: {delete_error}")
    return None

def clean_all_template_qa(frame_dirs: list[str], template_name):
    """
    批量检查并清理所有 template_qa.json 文件。
    """
    print(f"🧹 Checking {len(frame_dirs)} folders...")

    for frame_dir in tqdm(frame_dirs):
        if check_and_clean_template_qa(frame_dir, template_name) is not None:
            print(f"✅ Cleaned {frame_dir}/{template_name}")
    print("✅ Done.")

def check_frame_has_json(frame_path: Path) -> str | None:
    """
    检查某个帧目录下是否存在指定的 wide/json 文件。
    如果存在，返回 frame_path；否则返回 None。
    """
    json_path = frame_path / "wide" / TARGET_FILENAME
    if json_path.exists():
        return str(frame_path.resolve())
    return None

def find_all_frame_dirs(root_path: str, num_workers: int = None) -> list[str]:
    """
    多进程查找所有包含目标 JSON 的帧目录。
    假设结构为 root/video_id/frame_id。
    """
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root_path}")

    # 查找所有两级目录：video_id/frame_id
    candidate_frame_dirs = [
        p.resolve() for p in tqdm(root.glob("*/*"), desc="Scanning folders")
        if p.is_dir()
    ]

    print(f"🔍 Found {len(candidate_frame_dirs)} candidate frame folders. Verifying...")
    
    valid_frame_dirs = []
    for candidate_frame_dir in tqdm(candidate_frame_dirs, desc="🔍 Checking frame folders"):
        if check_frame_has_json(candidate_frame_dir) is not None:
            valid_frame_dirs.append(str(candidate_frame_dir.resolve()))

    print(f"✅ Found {len(valid_frame_dirs)} valid frame folders with expected JSON.")
    return valid_frame_dirs

def find_unprocessed_frame_dirs(frame_dirs: list[str], filename) -> list[str]:
    """
    找出还没有生成 template_qa.json 的帧目录
    """
    unprocessed = []
    for frame_dir in tqdm(frame_dirs, desc="🔍 Checking unprocessed frames"):
        template_path = Path(frame_dir) / filename
        if not template_path.exists():
            unprocessed.append(frame_dir)
    return unprocessed

# ✅ 假设你已经定义好了这个函数
def template_qa_generation(frame_dir, template_name):
    """
    你已有的函数：生成 template_qa.json 并保存到 frame_dir 中
    """
    prompt_generator = PromptGenerator()
    data_path = Path(frame_dir) / "wide" / TARGET_FILENAME
    with open(data_path, 'r') as f:
        data = json.load(f)
    detections = data["objects"]
    gt_depth_path = data["gt_depth_path"]
    wide_depth_path = data["wide_depth_path"]
    qa_pairs = prompt_generator.evaluate_predicates_on_pairs(detections, gt_depth_path, wide_depth_path)
    result = {
        "image_path": data["image_path"],
        "image_resize_path": data["image_resized_path"],
        "gt_depth_path": data["gt_depth_path"],
        "wide_depth_path": data["wide_depth_path"],
        "image_caption": data["image_caption"],
        "qa_pairs": [{
            "question": qa[0][0],
            "answer": qa[0][1],
            "object_A_index": qa[1],
            "object_B_index": qa[2],
            "object_C_index": qa[3],
            "qa_function": qa[4],
            "qa_type": qa[5],
        } for qa in qa_pairs]
    }
    with open(f"{frame_dir}/{template_name}", 'w') as f:
        json.dump(result, f, indent=4)


    
def process_all_unprocessed_dirs(unprocessed_dirs: list[str], template_name) -> list[str]:

    for unprocessed_dir in tqdm(unprocessed_dirs, desc="🔄 Processing unprocessed frames"):
        template_qa_generation(unprocessed_dir, template_name)


# 示例用法
if __name__ == "__main__":
    root_dir = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"
    template_name = "template_qa.json"
    # ✅ 第一步：查找所有合法的帧文件夹（包含目标 JSON）
    frame_dirs = find_all_frame_dirs(root_dir)

    # ✅ 第二步：检查并清理损坏的 template_qa.json 文件
    deleted_files = clean_all_template_qa(frame_dirs, template_name)

    # ✅ 第三步：找出还未处理的帧目录（没有 template_qa.json）
    unprocessed_dirs = find_unprocessed_frame_dirs(frame_dirs, template_name)

    # ✅ 第四步：多进程处理所有未处理帧
    processed_dirs = process_all_unprocessed_dirs(unprocessed_dirs, template_name)
