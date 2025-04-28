#!/usr/bin/env python3
import json
from collections import Counter

# JSON 文件路径
json_path = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/multi_view_qa.json"

# 读取 JSON 文件
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 统计 JSON 记录总数
total_records = len(data)
print("JSON 中记录总数:", total_records)

# 统计每一类问题的个数，假设记录中使用 "question_type" 字段来表示问题类别 
# （如果不是，请将 "question_type" 改为实际字段名称）
question_type_counter = Counter()
for record in data:
    # 如果 record 中没有该键，则归类到 "Unknown"（可选处理）
    question_type = record.get("question_type", "Unknown")
    question_type_counter[question_type] += 1

print("\n各类问题的数量统计:")
for q_type, count in question_type_counter.items():
    print(f"{q_type}: {count}")