import os
import cv2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT_DIR = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20")

def get_image_size(path):
    """读取图像并返回尺寸 (W, H)，如果不存在或读取失败返回 None"""
    if not path.exists():
        return None
    img = cv2.imread(str(path))
    if img is None:
        return None
    return (img.shape[1], img.shape[0])  # (W, H)

def is_double_size(size_big, size_small):
    """判断 size_big 是否是 size_small 的两倍"""
    return size_big[0] == 2 * size_small[0] and size_big[1] == 2 * size_small[1]

def check_frame_folder(frame_path: Path):
    """对单个帧目录进行验证，返回错误列表"""
    wide_image = frame_path / "wide/image.png"
    gt_depth = frame_path / "gt/depth.png"
    wide_img_resized = frame_path / "wide/image_resized.png"
    wide_depth_resized = frame_path / "wide/depth_resized.png"
    wide_depth = frame_path / "wide/depth.png"

    sizes = {
        "wide/image.png": get_image_size(wide_image),
        "gt/depth.png": get_image_size(gt_depth),
        "wide/image_resized.png": get_image_size(wide_img_resized),
        "wide/depth_resized.png": get_image_size(wide_depth_resized),
        "wide/depth.png": get_image_size(wide_depth),
    }

    errors = []

    for name, size in sizes.items():
        if size is None:
            errors.append(f"[MISSING] {name} not found or unreadable in {frame_path}")
            return errors  # 跳过此帧

    # 验证 1：wide/image.png 是否是其他三个的两倍
    for name in ["gt/depth.png", "wide/image_resized.png", "wide/depth_resized.png"]:
        if not is_double_size(sizes["wide/image.png"], sizes[name]):
            errors.append(f"[SIZE ERROR] wide/image.png is not 2x of {name} in {frame_path}")

    # 验证 2：这三者是否尺寸一致
    ref_size = sizes["gt/depth.png"]
    for name in ["wide/image_resized.png", "wide/depth_resized.png"]:
        if sizes[name] != ref_size:
            errors.append(f"[MISMATCH] {name} size does not match gt/depth.png in {frame_path}")

    # 验证 3：这三者是否是 wide/depth.png 的两倍
    for name in ["gt/depth.png", "wide/image_resized.png", "wide/depth_resized.png"]:
        if not is_double_size(sizes[name], sizes["wide/depth.png"]):
            errors.append(f"[SIZE ERROR] {name} is not 2x of wide/depth.png in {frame_path}")

    return errors

def collect_all_frame_paths(root_dir: Path):
    """多进程收集所有帧路径"""
    frame_paths = []
    video_folders = [f for f in root_dir.iterdir() if f.is_dir()]
    for video in video_folders:
        frame_folders = [f for f in video.iterdir() if f.is_dir()]
        frame_paths.extend(frame_folders)
    return frame_paths

def main():
    print("[🔍] 正在收集所有帧路径...")
    frame_paths = collect_all_frame_paths(ROOT_DIR)
    print(f"[✅] 共找到 {len(frame_paths)} 个帧目录，开始多进程验证...")

    all_errors = []

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(check_frame_folder, frame): frame for frame in frame_paths}

        for future in as_completed(futures):
            errors = future.result()
            if errors:
                all_errors.extend(errors)

    if not all_errors:
        print("[✅] 所有尺寸验证通过！")
    else:
        print(f"[❌] 共发现 {len(all_errors)} 个问题：")
        for err in all_errors:
            print(err)

if __name__ == "__main__":
    main()