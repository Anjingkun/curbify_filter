import json
from pathlib import Path
import shutil
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# 文件名常量
TARGET_FILENAME = "detections_with_bbox_label_qwen_spital_caption_mask_pcd.json"
SOURCE_FILENAME = "detection_GroundingDino_bbox_RAM_label_qwen_caption_confidence25.json"

# ✅ 替换为你的根目录
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"


def find_all_frame_dirs(root_path: str) -> list[str]:
    """
    自动扫描 root_path 下的所有 video_id/frame_id 形式的帧目录
    """
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")

    candidate_dirs = [p.resolve() for p in root.glob("*/*") if p.is_dir()]
    print(f"🔍 Found {len(candidate_dirs)} frame folders under {root}")
    return [str(p) for p in candidate_dirs]


def patch_missing_json(frame_dir: str) -> str | None:
    """
    如果目标 JSON 缺失，但有备用 JSON，则复制并添加路径信息。
    """
    frame_path = Path(frame_dir)
    target_json_path = frame_path / "wide" / TARGET_FILENAME
    if target_json_path.exists():
        return None  # 已存在，无需处理

    source_json_path = frame_path / "wide" / SOURCE_FILENAME
    if not source_json_path.exists():
        print(f"⚠️ No SOURCE JSON found for {frame_dir}")
        return None  # 没有备份文件，跳过

    try:
        with open(source_json_path, "r") as f:
            data = json.load(f)

        # 添加路径字段
        base_path = frame_path.resolve()
        data["image_resized_path"] = str(base_path / "wide" / "image_resized.png")
        data["gt_depth_path"] = str(base_path / "gt" / "depth.png")
        data["wide_depth_path"] = str(base_path / "wide" / "depth.png")

        # 保存到目标 JSON
        with open(target_json_path, "w") as f:
            json.dump(data, f, indent=2)

        return str(target_json_path)

    except Exception as e:
        print(f"❌ Failed to patch {frame_dir}: {e}")
        return None


def patch_all_missing_json_parallel(frame_dirs: list[str], num_workers: int = None) -> list[str]:
    """
    多进程处理所有帧目录，补充缺失 JSON。
    """
    print(f"🔧 Patching missing JSON files in {len(frame_dirs)} frame folders with multiprocessing...")
    num_workers = num_workers or min(cpu_count(), 16)
    with Pool(num_workers) as pool:
        results = list(tqdm(pool.imap(patch_missing_json, frame_dirs), total=len(frame_dirs)))

    patched = [r for r in results if r is not None]
    print(f"✅ Patched {len(patched)} missing JSON files.")
    return patched


def delete_template_json_worker(frame_dir: str, filename: str) -> str | None:
    """
    工作进程：删除给定帧目录下指定的 JSON 文件（例如 visual_choice.json），
    如果删除成功则返回文件路径，否则返回 None。
    """
    file_path = Path(frame_dir) / filename
    if file_path.exists():
        try:
            file_path.unlink()
            return str(file_path)
        except Exception as e:
            print(f"❌ Failed to delete {file_path}: {e}")
    return None


def delete_template_json_parallel(frame_dirs: list[str], filename="visual_choice.json", num_workers: int = None) -> list[str]:
    """
    多进程删除每个帧目录下的指定 JSON 文件，并返回成功删除的文件路径列表。
    """
    print(f"🗑️ Deleting {filename} files in {len(frame_dirs)} frame folders with multiprocessing...")
    num_workers = num_workers or min(cpu_count(), 16)
    # 构造任务列表，每个任务是 (frame_dir, filename)
    tasks = [(frame_dir, filename) for frame_dir in frame_dirs]
    with Pool(num_workers) as pool:
        results = list(tqdm(pool.starmap(delete_template_json_worker, tasks), total=len(tasks)))
    deleted_files = [r for r in results if r is not None]
    print(f"✅ Deleted {len(deleted_files)} {filename} files.")
    return deleted_files


def delete_folder_worker(frame_dir: str, folder_name: str) -> str | None:
    """
    工作进程：删除给定帧目录下指定名称的文件夹（例如 image_with_bbox），
    如果删除成功则返回文件夹路径，否则返回 None。
    """
    folder_path = Path(frame_dir) / folder_name
    if folder_path.exists() and folder_path.is_dir():
        try:
            shutil.rmtree(folder_path)
            return str(folder_path)
        except Exception as e:
            print(f"❌ Failed to delete {folder_path}: {e}")
    return None


def delete_folder_parallel(frame_dirs: list[str], folder_name="image_with_bbox", num_workers: int = None) -> list[str]:
    """
    多进程删除每个帧目录下的指定文件夹，并返回成功删除的文件夹路径列表。
    """
    print(f"🗑️ Deleting '{folder_name}' folders in {len(frame_dirs)} frame folders with multiprocessing...")
    num_workers = num_workers or min(cpu_count(), 16)
    # 构造任务列表，每个任务是 (frame_dir, folder_name)
    tasks = [(frame_dir, folder_name) for frame_dir in frame_dirs]
    with Pool(num_workers) as pool:
        results = list(tqdm(pool.starmap(delete_folder_worker, tasks), total=len(tasks)))
    deleted_folders = [r for r in results if r is not None]
    print(f"✅ Deleted {len(deleted_folders)} '{folder_name}' folders.")
    return deleted_folders


if __name__ == "__main__":
    # 自动扫描帧目录
    frame_dirs = find_all_frame_dirs(ROOT_DIR)

    # 多进程删除 visual_choice.json 文件
    deleted_json_files = delete_template_json_parallel(frame_dirs, filename="choice_qa.json")

    # # 多进程删除子目录，例如 image_with_bbox 和 image_with_points
    # deleted_bbox_folders = delete_folder_parallel(frame_dirs, folder_name="image_with_bbox")
    # deleted_points_folders = delete_folder_parallel(frame_dirs, folder_name="image_with_points")

    # 如果需要多进程补全缺失 JSON，也可以启用下面这行：
    # patched_files = patch_all_missing_json_parallel(frame_dirs)

# import json
# from pathlib import Path
# import shutil
# from tqdm import tqdm
# from multiprocessing import Pool, cpu_count

# # 文件名常量
# TARGET_FILENAME = "detections_with_bbox_label_qwen_spital_caption_mask_pcd.json"
# SOURCE_FILENAME = "detection_GroundingDino_bbox_RAM_label_qwen_caption_confidence25.json"

# # ✅ 替换为你的根目录
# ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

# def find_all_frame_dirs(root_path: str) -> list[str]:
#     """
#     自动扫描 root_path 下的所有 video_id/frame_id 形式的帧目录
#     """
#     root = Path(root_path).resolve()
#     if not root.exists():
#         raise FileNotFoundError(f"Root path does not exist: {root}")

#     candidate_dirs = [p.resolve() for p in root.glob("*/*") if p.is_dir()]
#     print(f"🔍 Found {len(candidate_dirs)} frame folders under {root}")
#     return [str(p) for p in candidate_dirs]

# def patch_missing_json(frame_dir: str) -> str | None:
#     """
#     如果目标 JSON 缺失，但有备用 JSON，则复制并添加路径信息。
#     """
#     frame_path = Path(frame_dir)

#     target_json_path = frame_path / "wide" / TARGET_FILENAME
#     if target_json_path.exists():
#         return None  # 已存在，无需处理

#     source_json_path = frame_path / "wide" / SOURCE_FILENAME
#     if not source_json_path.exists():
#         print(f"⚠️ No SOURCE JSON found for {frame_dir}")
#         return None  # 没有备份文件，跳过

#     try:
#         with open(source_json_path, "r") as f:
#             data = json.load(f)

#         # 添加路径字段
#         base_path = frame_path.resolve()
#         data["image_resized_path"] = str(base_path / "wide" / "image_resized.png")
#         data["gt_depth_path"] = str(base_path / "gt" / "depth.png")
#         data["wide_depth_path"] = str(base_path / "wide" / "depth.png")

#         # 保存到目标 JSON
#         with open(target_json_path, "w") as f:
#             json.dump(data, f, indent=2)

#         return str(target_json_path)

#     except Exception as e:
#         print(f"❌ Failed to patch {frame_dir}: {e}")
#         return None

# def patch_all_missing_json_parallel(frame_dirs: list[str], num_workers: int = None) -> list[str]:
#     """
#     多进程处理所有帧目录，补充缺失 JSON。
#     """
#     print(f"🔧 Patching missing JSON files in {len(frame_dirs)} frame folders with multiprocessing...")

#     num_workers = num_workers or min(cpu_count(), 16)
#     with Pool(num_workers) as pool:
#         results = list(tqdm(pool.imap(patch_missing_json, frame_dirs), total=len(frame_dirs)))

#     patched = [r for r in results if r is not None]
#     print(f"✅ Patched {len(patched)} missing JSON files.")
#     return patched


# import os
# from pathlib import Path
# from tqdm import tqdm

# def delete_tamplate_json(frame_dirs: list[str], filename="fact.json") -> list[str]:
#     """
#     删除每个 frame_dir 下的 fact.json 文件（如果存在）。
#     返回删除成功的文件路径列表。
#     """
#     deleted_files = []

#     for frame_dir in tqdm(frame_dirs, desc="🗑️ Deleting fact.json"):
#         file_path = Path(frame_dir) / filename
#         if file_path.exists():
#             try:
#                 file_path.unlink()
#                 deleted_files.append(str(file_path))
#             except Exception as e:
#                 print(f"❌ Failed to delete {file_path}: {e}")

#     print(f"✅ Deleted {len(deleted_files)} fact.json files.")
#     return deleted_files

# def delete_bbox_folder(frame_dirs: list[str], folder_name="image_with_bbox") -> list[str]:
#     """
#     删除每个 frame_dir 下的 image_with_bbox 子目录。
#     返回成功删除的目录路径列表。
#     """
#     deleted_folders = []

#     for frame_dir in tqdm(frame_dirs, desc=f"🗑️ Deleting {folder_name}/ folders"):
#         folder_path = Path(frame_dir) / folder_name
#         if folder_path.exists() and folder_path.is_dir():
#             try:
#                 shutil.rmtree(folder_path)
#                 deleted_folders.append(str(folder_path))
#             except Exception as e:
#                 print(f"❌ Failed to delete {folder_path}: {e}")

#     print(f"✅ Deleted {len(deleted_folders)} '{folder_name}' folders.")
#     return deleted_folders

# if __name__ == "__main__":
#     # 自动扫描帧目录
#     frame_dirs = find_all_frame_dirs(ROOT_DIR)
#     # 删除 tamplate.json 文件
#     deleted = delete_tamplate_json(frame_dirs, filename="visual_choice.json")
#     # # 删除 image_with_bbox 子目录
#     deleted_folders = delete_bbox_folder(frame_dirs, folder_name="image_with_bbox")
#     deleted_folders = delete_bbox_folder(frame_dirs, folder_name="image_with_points")
#     # 多进程补全缺失 JSON
#     # patched_files = patch_all_missing_json_parallel(frame_dirs)