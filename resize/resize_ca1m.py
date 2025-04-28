import os
from pathlib import Path
import cv2
import multiprocessing
from tqdm import tqdm

ROOT_DIR = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20")

def find_image_paths_in_video(video_dir: Path):
    """在一个视频目录中查找所有 wide/depth.png 路径"""
    return list(video_dir.glob("**/wide/depth.png"))

def collect_all_image_paths_multithreaded(root_dir: Path):
    """多进程并发查找所有 depth.png 路径"""
    video_dirs = [d for d in root_dir.iterdir() if d.is_dir()]
    print(f"🔍 找到 {len(video_dirs)} 个视频目录，开始并行查找 depth.png...")

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        all_image_lists = list(tqdm(pool.imap_unordered(find_image_paths_in_video, video_dirs), total=len(video_dirs)))

    # 展平二维列表
    image_paths = [img for sublist in all_image_lists for img in sublist]
    return image_paths

def process_image(image_path: Path):
    try:
        if not image_path.exists():
            return

        # 读取图像
        img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"无法读取图像: {image_path}")
            return

        # Resize 为原图的一半
        h, w = img.shape[:2]
        resized = cv2.resize(img, (w * 2, h * 2), interpolation=cv2.INTER_NEAREST)

        # 保存为 image_resized.png
        output_path = image_path.parent / "depth_resized.png"
        cv2.imwrite(str(output_path), resized)

    except Exception as e:
        print(f"处理失败 {image_path}: {e}")

def main():
    # 多进程查找 image.png
    image_paths = collect_all_image_paths_multithreaded(ROOT_DIR)
    print(f"✅ 共找到 {len(image_paths)} 张 depth.png，开始多进程 resize...")

    # 多进程 resize 处理
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        list(tqdm(pool.imap_unordered(process_image, image_paths), total=len(image_paths)))

if __name__ == "__main__":
    main()