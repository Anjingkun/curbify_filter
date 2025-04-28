#!/usr/bin/env python3
import json
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# 文件名常量（如有需要，可自行扩展）
TARGET_FILENAME = "detections_with_bbox_label_qwen_spital_caption_mask_pcd.json"
SOURCE_FILENAME = "detection_GroundingDino_bbox_RAM_label_qwen_caption_confidence25.json"

# ✅ 修改为你的根目录
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

def find_all_frame_dirs(root_path: str) -> list[str]:
    """
    自动扫描 root_path 下所有形如 video_id/frame_id 的帧目录
    """
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")
    
    candidate_dirs = [p.resolve() for p in root.glob("*/*") if p.is_dir()]
    print(f"🔍 Found {len(candidate_dirs)} frame folders under {root}")
    return [str(p) for p in candidate_dirs]

def process_frame(frame_dir: str) -> list:
    """
    对单个帧目录进行处理：
    1. 从路径中解析出 video_id 和 frame_id。
    2. 查找该目录下的 choice_qa.json 文件，读取并解析内容。
    3. 对于 choice_qa.json 中的每个 qa_pair 单独生成一条新的数据：
       - id 为 "{video_id}_{frame_id}_{qa_index}"（qa_index 从 1 开始计数）
       - image 为 [ "{video_id}_{frame_id}_wide_image.png" ]
       - depth 为 [ "{video_id}_{frame_id}_wide_depth.png" ]
       - conversations 为包含两个轮次：
            第一条："human" 对应 qa_pair 中的 question
            第二条："gpt" 对应 qa_pair 中的 answer
    """
    new_items = []
    try:
        frame_path = Path(frame_dir)
        # 计算相对于 ROOT_DIR 的相对路径，并从中解析出 video_id 和 frame_id
        relative_parts = frame_path.relative_to(ROOT_DIR).parts
        if len(relative_parts) < 2:
            print(f"跳过目录 {frame_dir}，路径格式不符合 video_id/frame_id")
            return []
        
        video_id, frame_id = relative_parts[0], relative_parts[1]
        qa_json_path = frame_path / "vacant_qa.json"
        
        if not qa_json_path.exists():
            print(f"❌ 未找到 {qa_json_path}，跳过该目录")
            return []

        with open(qa_json_path, 'r', encoding="utf8") as f:
            data = json.load(f)
        
        qa_pairs = data.get("qa_pairs", [])
        if not qa_pairs:
            # 没有有效的 QA 数据
            return []

        # 对每个 qa_pair 分别构造一条新的记录
        for idx, pair in enumerate(qa_pairs):
            question = pair.get("question", "")
            answer = pair.get("answer", "")
            # 如果问题或回答为空，则跳过该 qa_pair
            if not question or not answer:
                continue

            new_item = {
                "id": f"{video_id}_{frame_id}_{idx+1}",
                "image": [f"{video_id}_{frame_id}_wide_image.png"],
                "depth": [f"{video_id}_{frame_id}_wide_depth.png"],
                "conversations": [
                    {
                        "from": "human",
                        "value": question
                    },
                    {
                        "from": "gpt",
                        "value": answer
                    }
                ]
            }
            new_items.append(new_item)

        return new_items
    except Exception as e:
        print(f"⚠️ 处理 {frame_dir} 时出现错误: {e}")
        return []

if __name__ == "__main__":
    # 扫描所有帧目录
    frame_dirs = find_all_frame_dirs(ROOT_DIR)

    results = []
    # 使用多进程加速处理
    with Pool(cpu_count()) as pool:
        for result in tqdm(pool.imap(process_frame, frame_dirs), total=len(frame_dirs)):
            if result:
                results.extend(result)
    
    # 将所有处理结果写入大 JSON 文件
    output_path = Path(ROOT_DIR).parent / "ca1m_vacant_qa.json"
    with open(output_path, "w", encoding="utf8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(len(results))
    print(f"🎉 合成大 metadata JSON 完成，结果保存在 {output_path}")