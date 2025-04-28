#!/usr/bin/env python3
import json
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# ✅ 修改为你的根目录
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/llm_qa"

def find_all_frame_json_files(root_path: str) -> list[Path]:
    """
    查找 root_path 下所有符合以下目录结构的 JSON 文件：
      ROOT_DIR/数字文件夹/video_id/frame_id.json
    使用 glob 模式： "*/*/*.json"
    返回所有 JSON 文件的完整路径列表（Path 对象）。
    """
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")
    json_files = list(root.glob("*/*/*.json"))
    print(f"🔍 Found {len(json_files)} json files under {root}")
    return json_files

def process_frame_json(json_file: Path) -> dict | None:
    """
    处理单个 JSON 文件，转换为目标数据格式：
      - id: f"{video_id}_{frame_id}"，其中 video_id 为父文件夹名称，frame_id 为文件名去掉 .json 后缀。
      - image: [ f"{video_id}{frame_id}_wide_image.png" ]
      - depth: [ f"{video_id}{frame_id}_wide_depth.png" ]
      - conversations: 对原 conversations 中每个对话条目，
          按顺序生成两条消息，一条 human（取 question 字段），一条 gpt（取 answer 字段）。
    """
    try:
        # 获取 video_id 和 frame_id（注意：这里 video_id 来自 JSON 文件所在的视频文件夹名称）
        video_id = json_file.parent.name
        frame_id = json_file.stem  # 文件名去掉 .json 后缀

        with open(json_file, 'r', encoding="utf8") as f:
            data = json.load(f)

        # 构造输出中的 id、image、depth 字段
        new_id = f"{video_id}_{frame_id}"
        image_file = f"{video_id}{frame_id}_wide_image.png"
        depth_file = f"{video_id}{frame_id}_wide_depth.png"

        # 构造 conversations，对每个原对话条目生成 human 与 gpt 两个轮次
        convs = []
        for item in data.get("conversations", []):
            question = item.get("question", "").strip()
            answer = item.get("answer", "").strip()
            # 如果 question 或 answer 存在内容则添加，避免空白字符串
            if question:
                convs.append({"from": "human", "value": question})
            if answer:
                convs.append({"from": "gpt", "value": answer})

        new_item = {
            "id": new_id,
            "image": [image_file],
            "depth": [depth_file],
            "conversations": convs
        }
        # 如果 conversations 为空，则跳过
        if len(new_item["conversations"]) == 0:
            # print(f"❌ 目录 {frame_dir} 没有找到有效的 QA 数据，跳过")
            return None
        return new_item
    except Exception as e:
        print(f"⚠️ Error processing {json_file}: {e}")
        return None

if __name__ == "__main__":
    # 获取所有 frame_json 文件
    json_files = find_all_frame_json_files(ROOT_DIR)

    results = []
    # 利用多进程并行处理，利用 tqdm 显示进度条
    with Pool(cpu_count()) as pool:
        for item in tqdm(pool.imap(process_frame_json, json_files), total=len(json_files)):
            if item is not None:
                results.append(item)

    # 保存合并后的结果到 ca1m_reasoning_qa.json 文件
    output_path = Path(ROOT_DIR).parent / "ca1m_reasoning_qa.json"
    with open(output_path, "w", encoding="utf8") as f_out:
        json.dump(results, f_out, indent=2, ensure_ascii=False)

    print(f"🎉 合成大 metadata JSON 完成，保存路径：{output_path}")