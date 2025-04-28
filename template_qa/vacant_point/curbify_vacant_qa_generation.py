import os
import json
from multiprocessing import Pool, cpu_count, set_start_method
from pathlib import Path
from tqdm import tqdm
from prompt import *
import traceback
import time
import numpy as np
import os
import json

# 目标 JSON 文件名（检测文件）
TARGET_FILENAME = "detections_with_bbox_label_qwen_spital_caption_mask_pcd.json"

def load_all_whether_have_platform(root_path):
    """
    从 root_path 中递归读取所有 JSON 文件，合并所有数组项，
    并筛选出 have_platform 为 True 的 frame_folder_path。

    返回：
        List[str] 所有符合条件的路径
    """
    all_items = []

    # 遍历所有 json 文件
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith(".json"):
                json_path = os.path.join(dirpath, filename)
                try:
                    with open(json_path, "r") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_items.extend(data)
                        else:
                            print(f"⚠️ 非数组结构跳过: {json_path}")
                except Exception as e:
                    print(f"❌ 读取失败: {json_path}\n{e}")

    return all_items

def check_and_clean_template_qa(frame_dir: dict, filename) -> str | None:
    """
    检查并尝试加载 frame_dir/template_qa.json。
    如果损坏则删除，返回被删除的路径；否则返回 None。
    """
    json_path = Path(frame_dir["frame_folder_path"]) / filename
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

def clean_all_template_qa(frame_dirs: list[dict], template_name):
    """
    批量检查并清理所有 template_qa.json 文件。
    """
    print(f"🧹 Checking {len(frame_dirs)} folders...")
    for frame_dir in tqdm(frame_dirs, desc="Checking folders"):
        if check_and_clean_template_qa(frame_dir, template_name) is not None:
            print(f"✅ Cleaned {frame_dir}/{template_name}")
    print("✅ Done.")

def find_unprocessed_frame_dirs(frame_dirs: list[dict], filename) -> list[str]:
    """
    找出还没有生成 template_qa.json 的帧目录
    """
    unprocessed = []
    for frame_dir in tqdm(frame_dirs, desc="🔍 Checking unprocessed frames"):
        template_path = Path(frame_dir["frame_folder_path"]) / filename
        if not template_path.exists():
            unprocessed.append(frame_dir)
    return unprocessed

def template_qa_generation(frame_dir, template_name):
    """
    生成 template_qa.json 并保存到 frame_dir 中
    """
    # 在每个子进程中重新创建 VisualPromptGenerator
    prompt_generator = PromptGenerator()
    data_root = frame_dir["frame_folder_path"]
    data_path = Path(data_root) / "wide" / TARGET_FILENAME
    with open(data_path, 'r') as f:
        data = json.load(f)
    if not frame_dir["have_platform"]:
        result = {
            "image_path": data["image_path"],
            "image_resize_path": data["image_resized_path"],
            "gt_depth_path": data["gt_depth_path"],
            "wide_depth_path": data["wide_depth_path"],
            "image_caption": data["image_caption"],
            "qa_pairs": []
        }
        with open(f"{data_root}/{template_name}", 'w') as f:
            json.dump(result, f, indent=4)

        return
    
    detections = data["objects"]
    gt_depth_path = data["gt_depth_path"]
    wide_depth_path = data["wide_depth_path"]
    instances_path = os.path.join(data_root, "wide", "instances.json")
    T_gravity_path = os.path.join(data_root, "wide", "T_gravity.json")
    K_path = os.path.join(data_root, "wide", "depth", "K.json")

    qa_pairs = prompt_generator.evaluate_predicates_on_pairs(detections, instances_path, gt_depth_path, wide_depth_path, T_gravity_path, K_path)
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
    with open(f"{data_root}/{template_name}", 'w') as f:
        json.dump(result, f, indent=4)

    return

def process_frame_dir(args):
    """
    包装 template_qa_generation 调用，并返回处理情况。
    """
    frame_dir, template_name = args
    try:
        template_qa_generation(frame_dir, template_name)
        return frame_dir  # 成功处理后返回处理的帧目录
    except Exception as e:
        print(f"Error processing {frame_dir}: {e}")
        traceback.print_exc()
        return None

def process_all_unprocessed_dirs(unprocessed_dirs: list[dict], template_name) -> list[str]:
    tasks = [(frame_dir, template_name) for frame_dir in unprocessed_dirs]
    processed_dirs = []
    pool = Pool(cpu_count())
    try:
        for result in tqdm(
            pool.imap_unordered(process_frame_dir, tasks, chunksize=1),
            total=len(tasks),
            desc="🔄 Processing unprocessed frames"
        ):
            if result is not None:
                processed_dirs.append(result)
    except KeyboardInterrupt:
        print("\n⚠️ KeyboardInterrupt detected, terminating pool and child processes...")
        pool.terminate()   # 强制终止所有子进程
        pool.join()
        raise             # 可选：重新抛出异常，或 return processed_dirs
    else:
        pool.close()
        pool.join()
    return processed_dirs

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

def merge_frame_paths(platform_paths, frame_dirs):
    # 1. 把已有的路径做成一个字典，便于查找
    platform_dict = {
        item['frame_folder_path']: item.get('have_platform', False)
        for item in platform_paths
    }
    # 2. 构建新的完整列表
    result = []
    for frame_path in frame_dirs:
        have_platform = platform_dict.get(frame_path, False)
        result.append({
            "frame_folder_path": frame_path,
            "have_platform": have_platform
        })

    return result
# 示例用法
if __name__ == "__main__":
    # 为避免 fork 带来的问题，使用 spawn 启动方式
    try:
        set_start_method('spawn', force=True)
    except RuntimeError:
        pass

    root_dir = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"
    template_name = "vacant_qa.json"
    whether_have_platform_path = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/whether_have_platform"

    platform_paths = load_all_whether_have_platform(whether_have_platform_path)
    # ✅ 第一步：查找所有合法的帧文件夹（包含目标 JSON）
    frame_dirs = find_all_frame_dirs(root_dir)
    all_platform_paths = merge_frame_paths(platform_paths, frame_dirs)
    # 第二步：检查并清理损坏的 vacant_qa.json 文件
    clean_all_template_qa(all_platform_paths, template_name)

    # 第三步：找出还未处理的帧目录（没有 vacant_qa.json）
    unprocessed_dirs = find_unprocessed_frame_dirs(all_platform_paths, template_name)

    # ✅ 第四步：多进程处理所有未处理帧
    processed_dirs = process_all_unprocessed_dirs(unprocessed_dirs, template_name)


