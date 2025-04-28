import os
import shutil
import random
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

def process_ca1m_folder(args):
    ca1m_path, train_root, save_root, stride = args

    video_id = os.path.basename(ca1m_path).split("-")[-1]
    video_root = os.path.join(ca1m_path, video_id)

    if not os.path.isdir(video_root):
        print(f"Video folder {video_root} does not exist.")
        return 0  # 跳过不存在的目录

    # 收集所有帧前缀并按字典序排序
    all_frames = set()
    for name in os.listdir(video_root):
        if name.endswith(".wide"):
            prefix = name.split(".")[0]
            all_frames.add(prefix)
    
    sorted_frames = sorted(all_frames)  # 关键修改：字典排序
    total_frames = len(sorted_frames)
    
    if total_frames > 20:
        remaining_frames = sorted_frames[20:]  # 正常情况舍弃前20
    else:
        remaining_frames = sorted_frames  # 帧数不足时使用全部
    
    # 在剩余帧的前20个（原排序的21-40）中随机选择起始点
    start_candidates = remaining_frames[:20]
    if not start_candidates:
        print(f"No start frames are left in {video_root}.")
        return 0
    
    start_frame = random.choice(start_candidates)
    
    # 找到起始点在剩余帧中的位置
    try:
        start_index = remaining_frames.index(start_frame)
    except ValueError:
        print(f"Start frame {start_frame} not found in {video_root}.")
        return 0
    
    # 按指定步长采样
    sampled_frames = remaining_frames[start_index::stride]

    # 确保每个视频的起始帧随机性独立
    random.seed()  # 重置随机种子

    for frame_id in sampled_frames:
        for suffix in ["gt", "wide"]:
            src = os.path.join(video_root, f"{frame_id}.{suffix}")
            dst = os.path.join(save_root, video_id, frame_id, suffix)
            if os.path.exists(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
    return 1

def sample_and_copy_frames_parallel(train_root, save_root, stride=20):
    ca1m_folders = [f for f in os.listdir(train_root) if f.startswith("ca1m-")]
    ca1m_paths = [os.path.join(train_root, f) for f in ca1m_folders]

    args_list = [(path, train_root, save_root, stride) for path in ca1m_paths]

    print(f"Found {len(args_list)} ca1m-* folders. Using {cpu_count()} processes.")

    total = 0
    with Pool(processes=cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(process_ca1m_folder, args_list), total=len(args_list)):
            total += result

    print(f"Done. Total copied frame folders: {total}")

# 使用示例
train_dir = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/train/"
save_dir = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20/"
sample_and_copy_frames_parallel(train_dir, save_dir, stride=20)