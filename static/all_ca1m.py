import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def count_wide_folders_in_video(video_folder):
    """
    只扫描 video_folder 下的某一层（非递归），统计 .wide 结尾的子文件夹
    """
    wide_folders = []
    # 寻找 video_xxx/frames 之类的唯一子文件夹
    subfolders = [
        os.path.join(video_folder, d)
        for d in os.listdir(video_folder)
        if os.path.isdir(os.path.join(video_folder, d))
    ]

    if len(subfolders) != 1:
        return 0, []  # 如果不是唯一子文件夹，跳过

    frame_root = subfolders[0]
    try:
        for d in os.listdir(frame_root):
            full_path = os.path.join(frame_root, d)
            if os.path.isdir(full_path) and d.endswith(".wide"):
                wide_folders.append(full_path)
    except Exception as e:
        print(f"读取出错: {frame_root} - {e}")

    return len(wide_folders), wide_folders

def main():
    root_path = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/train"

    # 获取所有 video_xxx 文件夹路径（一级目录）
    video_folders = [
        os.path.join(root_path, d)
        for d in os.listdir(root_path)
        if os.path.isdir(os.path.join(root_path, d))
    ]

    print(f"共找到 {len(video_folders)} 个视频文件夹，开始并行扫描...")

    total_count = 0
    all_wide_paths = []

    with Pool(processes=cpu_count()) as pool:
        for count, paths in tqdm(pool.imap_unordered(count_wide_folders_in_video, video_folders), total=len(video_folders)):
            total_count += count
            all_wide_paths.extend(paths)

    print(f"\n✅ 总共找到 {total_count} 个以 `.wide` 结尾的文件夹。")
    if total_count > 0:
        print("示例路径：")
        for i, path in enumerate(all_wide_paths[:10]):
            print(f"{i+1}. {path}")

if __name__ == "__main__":
    main()