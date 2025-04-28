#!/usr/bin/env python3
import json
from pathlib import Path
from tqdm import tqdm

# 请替换为你的根目录路径
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

def process_visual_choice_qa_file(json_file: Path) -> list:
    """
    针对一个 choice_qa.json 文件，
    每个 qa_pair 独立生成一条记录，格式如下：
    {
      "id": "{video_id}_{frame_id}",
      "image": ["{video_id}_{frame_id}_{folder}_{filename}"],
      "depth": ["{video_id}_{frame_id}_wide_depth.png"],
      "conversations": [
        {"from": "human", "value": "question text"},
        {"from": "gpt", "value": "(选项) 选项描述"}
      ]
    }
    """
    # 从文件路径中提取 video_id 和 frame_id
    # 假设结构为: ROOT_DIR / video_id / frame_id / "choice_qa.json"
    frame_dir = json_file.parent
    video_dir = frame_dir.parent
    video_id = video_dir.name
    frame_id = frame_dir.name
    entry_id = f"{video_id}_{frame_id}"

    # 读取 choice_qa.json 内容
    with open(json_file, "r") as f:
        data = json.load(f)

    qa_pairs = data.get("qa_pairs", [])
    items = []

    if len(qa_pairs) == 0:
        return None

    for qa in qa_pairs:
        # 每个 qa_pair 分别使用其独有的 visual_image_path
        visual_image_path = qa.get("visual_image_path", "")
        if visual_image_path:
            vip_path = Path(visual_image_path)
            folder_name = vip_path.parent.name  # 例如 "image_with_points" 或 "image_with_bbox"
            file_name = vip_path.name           # 例如 "0.png"
            image_name = f"{video_id}_{frame_id}_{folder_name}_{file_name}"
        else:
            image_name = f"{video_id}_{frame_id}_image.png"

        # depth 字段固定为 wide_depth.png 格式
        depth_name = f"{video_id}_{frame_id}_wide_depth.png"

        # 处理问句：
        human_question = qa.get("question", "")
        lines = human_question.splitlines()

        # 提取 question 中的选项（假设每个选项以类似 "(A)" 开头）
        options = {}
        for line in lines:
            line = line.strip()
            if line.startswith("(") and ")" in line:
                closing_idx = line.find(")")
                option_key = line[:closing_idx + 1]  # 如 "(A)"
                option_text = line[closing_idx + 1:].strip()
                if option_text:
                    options[option_key] = option_text

        answer_key = qa.get("answer", "").strip()
        if answer_key in options:
            full_answer = f"{answer_key} {options[answer_key]}"
        else:
            full_answer = answer_key

        # 构造该 qa_pair 对应的 conversation：仅包含一轮 QA（human->gpt）
        conversation = [
            {"from": "human", "value": human_question},
            {"from": "gpt", "value": full_answer}
        ]

        item = {
            "id": entry_id,
            "image": [image_name],
            "depth": [depth_name],
            "conversations": conversation
        }
        items.append(item)

    return items

def main():
    root = Path(ROOT_DIR).resolve()
    # 搜索所有形如 ROOT_DIR/video_id/frame_id/visual_choice.json 的文件
    qa_files = list(root.glob("*/*/visual_choice.json"))
    print(f"🔍 找到 {len(qa_files)} 个 visual_choice.json 文件。")

    all_items = []
    for qa_file in tqdm(qa_files, desc="处理文件"):
        try:
            items = process_visual_choice_qa_file(qa_file)
            if items:
                all_items.extend(items)
        except Exception as e:
            print(f"处理文件 {qa_file} 时出错：{e}")

    # 保存所有 item 到 ca1m_visual_choice_qa.json 中
    output_file = Path(ROOT_DIR).parent / "ca1m_visual_choice_qa.json"
    with open(output_file, "w") as f:
        json.dump(all_items, f, indent=2)
    print(f"✅ 汇总后的 metadata 已保存到 {output_file}")

if __name__ == "__main__":
    main()