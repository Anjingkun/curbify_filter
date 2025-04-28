#!/usr/bin/env python3
import json
import random
from pathlib import Path
from math import ceil
from tqdm import tqdm

# 定义输入文件路径（请根据实际情况调整路径）
TEMPLATE_FILE = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/ca1m_template_qa.json")
REASONING_FILE = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/ca1m_reasoning_qa.json")
CHOICE_FILE    = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/ca1m_choice_qa.json")

# 定义输出文件路径（文件将保存在当前工作目录）
OUTPUT_MERGED = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/ca1m_reasoning_template_qa_split.json")
OUTPUT_CHOICE = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/ca1m_choice_qa_split.json")

# 每条数据最多允许的QA数量（注意，一个QA对对应2条对话记录）
MAX_QA = 15  
CHUNK_SIZE = MAX_QA * 2  # 对应 conversations 的条目数

def load_json(file_path: Path) -> list:
    with open(file_path, "r", encoding="utf8") as f:
        return json.load(f)

def merge_template_reasoning(template_list: list, reasoning_list: list) -> list:
    """
    对两个列表按 id 进行合并：
      - 如果相同 id 出现，则将 conversations 拼接
      - 如果不重合则直接保留
    返回合并后以列表形式存储的条目。
    """
    merged_dict = {}
    # 先添加模板数据
    for item in template_list:
        item_id = item.get("id")
        if item_id is None:
            continue
        # 确保 conversations 字段存在
        item.setdefault("conversations", [])
        merged_dict[item_id] = item

    # 遍历推理数据
    for item in reasoning_list:
        item_id = item.get("id")
        if item_id is None:
            continue
        item.setdefault("conversations", [])
        if item_id in merged_dict:
            # 合并 conversations；简单拼接即可
            merged_dict[item_id]["conversations"].extend(item["conversations"])
        else:
            merged_dict[item_id] = item

    return list(merged_dict.values())

def split_item_by_max_qa(item: dict, chunk_size: int = CHUNK_SIZE) -> list:
    """
    检查 item["conversations"] 中的 QA 对数(两条数据为一组）。
    如果超过 chunk_size（即条数超过MAX_QA*2），
    则按顺序拆分成多个新的 item，除了 conversations 外其它字段保持不变。
    如果未超过则原样返回列表中单个元素
    """
    convs = item.get("conversations", [])
    if len(convs) <= chunk_size:
        return [item]
    
    new_items = []
    # 按 chunk_size 拆分 conversations（注意，顺序必须保持）
    # 如果对话记录总数不能被 chunk_size 整除，最后一次拆分可能不足 chunk_size 条记录
    for i in range(0, len(convs), chunk_size):
        new_item = item.copy()
        # 使用切片保证只包含本次拆分的对话记录
        new_item["conversations"] = convs[i:i+chunk_size]
        # （可选）如果想保证每个输出条目的 id 唯一，可在 id 后加上序号后缀，不加也符合“其余信息不变”
        if len(convs) > chunk_size:
            suffix = f"_{i // chunk_size}"
            new_item["id"] = item["id"] + suffix
        new_items.append(new_item)
    return new_items

def split_dataset(dataset: list) -> list:
    """
    对输入的列表中每条数据检测 QA 对是否超过限制，如超过则拆分成为多个数据返回，
    返回拆分后的完整列表。
    """
    new_dataset = []
    for item in dataset:
        new_dataset.extend(split_item_by_max_qa(item))
    return new_dataset

def main():
    print("加载 ca1m_template_qa 数据...")
    template_data = load_json(TEMPLATE_FILE)
    print("加载 ca1m_reasoning_qa 数据...")
    reasoning_data = load_json(REASONING_FILE)
    print("加载 ca1m_choice_qa 数据...")
    choice_data = load_json(CHOICE_FILE)
    
    # 任务1：合并 template 与 reasoning 对话数据
    merged_data = merge_template_reasoning(template_data, reasoning_data)
    print(f"合并后数据条数：{len(merged_data)}")
    
    # 任务2：打乱合并后的顺序
    random.shuffle(merged_data)
    
    # 任务3：拆分 QA 对超过10对的数据，分别对 merged_data 和 choice_data 进行拆分
    print("拆分合并数据中 QA 数超过限制的条目...")
    merged_split = split_dataset(merged_data)
    print(f"拆分后合并数据条数：{len(merged_split)}")
    
    print("拆分 ca1m_choice_qa 数据中 QA 数超过限制的条目...")
    choice_split = split_dataset(choice_data)
    print(f"拆分后 ca1m_choice_qa 数据条数：{len(choice_split)}")
    
    # 保存结果
    with open(OUTPUT_MERGED, "w", encoding="utf8") as f:
        json.dump(merged_split, f, indent=2, ensure_ascii=False)
    print(f"合并并拆分后的模板+推理数据已保存至 {OUTPUT_MERGED}")

    with open(OUTPUT_CHOICE, "w", encoding="utf8") as f:
        json.dump(choice_split, f, indent=2, ensure_ascii=False)
    print(f"拆分后的 choice 数据已保存至 {OUTPUT_CHOICE}")

if __name__ == "__main__":
    main()