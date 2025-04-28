#!/usr/bin/env python3
import shutil
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# 文件名常量（如有需要，可自行扩展）
TARGET_FILENAME = "detections_with_bbox_label_qwen_spital_caption_mask_pcd.json"
SOURCE_FILENAME = "detection_GroundingDino_bbox_RAM_label_qwen_caption_confidence25.json"

# ✅ 修改为你的根目录
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

# 定位与 ROOT_DIR 同级的父目录，然后创建 images 和 depths 目录
parent_dir = Path(ROOT_DIR).parent
images_dir = parent_dir / "images"
depths_dir = parent_dir / "depths"

# 如果目标目录不存在，则创建
images_dir.mkdir(exist_ok=True)
depths_dir.mkdir(exist_ok=True)

def find_all_frame_dirs(root_path: str) -> list[str]:
    """
    自动扫描 root_path 下所有形如 video_id/frame_id 的帧目录
    """
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")
        
    # 查找一级目录中的子文件夹（video_id/frame_id）
    candidate_dirs = [p.resolve() for p in root.glob("*/*") if p.is_dir()]
    print(f"🔍 Found {len(candidate_dirs)} frame folders under {root}")
    return [str(p) for p in candidate_dirs]

def process_frame(frame_dir: str) -> None:
    """
    对单个帧目录进行处理：
    1. 从相对于 ROOT_DIR 的路径中解析出 video_id 和 frame_id。
    2. 对 wide 文件夹下 image_resized.png 或 depth_normalized.png 文件进行复制，
       并根据规则重命名后，分别复制到 images_dir 和 depths_dir 中。
    """
    try:
        frame_path = Path(frame_dir)
        # 相对路径应该为 video_id/frame_id 格式
        relative_parts = frame_path.relative_to(ROOT_DIR).parts
        if len(relative_parts) < 2:
            print(f"跳过目录 {frame_dir}，路径格式不符合 video_id/frame_id")
            return

        video_id, frame_id = relative_parts[0], relative_parts[1]
        wide_folder = frame_path / "wide"

        # 待复制的源文件路径
        image_src = wide_folder / "image_resized.png"
        depth_src = wide_folder / "depth_normalized.png"

        # 复制 image_resized.png 到 images 目录并重命名
        if image_src.exists():
            new_image_name = f"{video_id}_{frame_id}_wide_image.png"
            shutil.copy2(image_src, images_dir / new_image_name)
        else:
            print(f"❌ 图像文件未找到: {image_src}")

        # 复制 depth_normalized.png 到 depths 目录并重命名
        if depth_src.exists():
            new_depth_name = f"{video_id}_{frame_id}_wide_depth.png"
            shutil.copy2(depth_src, depths_dir / new_depth_name)
        else:
            print(f"❌ 深度文件未找到: {depth_src}")

    except Exception as e:
        print(f"⚠️ 处理 {frame_dir} 时出现错误: {e}")

if __name__ == "__main__":
    # 扫描所有帧目录
    frame_dirs = find_all_frame_dirs(ROOT_DIR)

    # 使用多进程加速批量处理
    with Pool(cpu_count()) as pool:
        list(tqdm(pool.imap(process_frame, frame_dirs), total=len(frame_dirs)))

    print("🎉 复制任务完成！")