import os
import multiprocessing
from functools import partial

# 根目录
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

# 删除函数：处理单个帧文件夹
def delete_detection_jsons_in_frame(video_id, frame_id):
    frame_path = os.path.join(ROOT_DIR, video_id, frame_id)
    # wide_path = os.path.join(frame_path, "wide")
    deleted = []

    if not os.path.isdir(frame_path):
        return deleted

    for filename in os.listdir(frame_path):
        if filename.startswith("detection") and filename.endswith(".json"):
            file_path = os.path.join(frame_path, filename)
            try:
                os.remove(file_path)
                deleted.append(file_path)
                print(f"✅ Deleted: {file_path}")
            except Exception as e:
                print(f"❌ Failed to delete {file_path}: {e}")
    return deleted

# 收集所有 (video_id, frame_id) 对
def collect_all_frame_folders(root_dir):
    frame_tasks = []
    for video_id in os.listdir(root_dir):
        video_path = os.path.join(root_dir, video_id)
        if not os.path.isdir(video_path):
            continue
        for frame_id in os.listdir(video_path):
            frame_path = os.path.join(video_path, frame_id)
            if os.path.isdir(frame_path):
                frame_tasks.append((video_id, frame_id))
    return frame_tasks

if __name__ == "__main__":
    print("🚀 Scanning for detection JSONs to delete...")

    # 获取所有帧路径任务
    all_frame_tasks = collect_all_frame_folders(ROOT_DIR)
    print(f"📦 Found {len(all_frame_tasks)} frame folders to process.")

    # 设置进程池数量（可根据机器调整）
    num_processes = min(multiprocessing.cpu_count(), 128)

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(delete_detection_jsons_in_frame, all_frame_tasks)

    # 汇总删除结果
    all_deleted = [item for sublist in results for item in sublist]
    print(f"\n🧹 Done! Total deleted: {len(all_deleted)} files.")