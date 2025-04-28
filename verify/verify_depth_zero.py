import os
import cv2
import numpy as np
from multiprocessing import Pool, cpu_count
from pathlib import Path
from tqdm import tqdm

# 根目录路径
ROOT_PATH = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20")

def find_depth_pngs_in_video(video_dir):
    """在一个视频目录中查找所有 wide/depth.png 路径"""
    depth_paths = []
    for depth_path in video_dir.rglob("wide/depth_resized.png"):
        depth_paths.append(depth_path)
    return depth_paths

def check_depth_has_zero(depth_path):
    """检查 depth.png 是否包含 0 值"""
    try:
        depth = cv2.imread(str(depth_path), cv2.IMREAD_UNCHANGED)
        if depth is None:
            return (str(depth_path), "NOT_LOADED")
        if (depth == 0).any():
            return (str(depth_path), True)
        else:
            return (str(depth_path), False)
    except Exception as e:
        return (str(depth_path), f"ERROR: {e}")

def parallel_find_all_depth_paths(root_path):
    """多进程查找所有 depth.png 路径"""
    video_dirs = [p for p in root_path.iterdir() if p.is_dir()]
    all_paths = []

    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(find_depth_pngs_in_video, video_dirs), 
                            total=len(video_dirs), desc="查找 depth.png"))
        for r in results:
            all_paths.extend(r)
    return all_paths

def parallel_check_depths(depth_paths):
    """多进程检查每个 depth.png 是否有0"""
    results = []
    with Pool(processes=cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(check_depth_has_zero, depth_paths), 
                           total=len(depth_paths), desc="检查是否包含 0"):
            results.append(result)
    return results

def main():
    print(f"[INFO] 开始多进程查找 {ROOT_PATH} 下所有 depth_resized.png...")
    all_depth_paths = parallel_find_all_depth_paths(ROOT_PATH)
    print(f"[INFO] 共找到 {len(all_depth_paths)} 个 depth_resized.png 文件，开始分析...")

    results = parallel_check_depths(all_depth_paths)

    print("\n[RESULT] 以下文件包含值为 0 的像素：\n")
    for path, has_zero in results:
        if has_zero == True:
            print(path)
        elif has_zero == "NOT_LOADED":
            print(f"[警告] 无法读取图像: {path}")
        elif isinstance(has_zero, str) and has_zero.startswith("ERROR"):
            print(f"[错误] {path} -> {has_zero}")

if __name__ == "__main__":
    main()