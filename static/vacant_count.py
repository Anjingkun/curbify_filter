import os
import json
from pathlib import Path
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def process_frame_folder(frame_folder):
    """
    处理一个帧文件夹，返回该文件夹中的 QA 总数和 qa_function 分布。
    """
    qa_json_path = Path(frame_folder) / "vacant_qa.json"
    result = {
        "total": 0,
        "functions": defaultdict(int)
    }

    if not qa_json_path.exists():
        return result

    try:
        with open(qa_json_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取失败: {qa_json_path}，错误: {e}")
        return result

    qa_pairs = data.get("qa_pairs", [])
    result["total"] = len(qa_pairs)

    for qa in qa_pairs:
        func = qa.get("qa_function", "unknown")
        result["functions"][func] += 1

    return result

def collect_qa_statistics_parallel(root_path):
    root = Path(root_path)
    total_qa_count = 0
    function_counter = defaultdict(int)

    # 收集所有帧目录路径
    frame_dirs = []
    for video_folder in root.iterdir():
        if not video_folder.is_dir():
            continue
        for frame_folder in video_folder.iterdir():
            if frame_folder.is_dir():
                frame_dirs.append(frame_folder)

    print(f"📁 帧目录总数: {len(frame_dirs)}")
    print(f"🚀 使用 {cpu_count()} 核心进行并行处理")

    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(process_frame_folder, frame_dirs), total=len(frame_dirs), desc="🔍 统计中"))

    # 聚合结果
    for result in results:
        total_qa_count += result["total"]
        for func, count in result["functions"].items():
            function_counter[func] += count

    # 显示结果
    print("\n✅ 统计完成")
    print(f"📊 QA 总数: {total_qa_count}")
    print("📈 QA Function 分布:")
    for func, count in sorted(function_counter.items(), key=lambda x: -x[1]):
        print(f"  {func:20s} : {count}")

# ✅ 调用主函数
if __name__ == "__main__":
    dataset_root = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"
    collect_qa_statistics_parallel(dataset_root)