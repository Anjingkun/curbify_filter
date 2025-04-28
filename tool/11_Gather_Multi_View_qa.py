import os
import json
import shutil
import imageio
import numpy as np
import re
from tqdm import tqdm

with open("/home_sfs/zhouenshen/dataset/3D/cubifyanything/multi_view_qa.json", "r") as f:
    data = json.load(f)

# 基础目录
base_dir = "/home_sfs/zhouenshen/dataset/3D/cubifyanything"

# 创建输出文件夹（如果不存在则创建）
images_out_dir = os.path.join(base_dir, "images_multi_view")
depths_out_dir = os.path.join(base_dir, "depths_multi_view")
os.makedirs(images_out_dir, exist_ok=True)
os.makedirs(depths_out_dir, exist_ok=True)

# 深度图处理函数（按照给定代码预处理深度图）
def process_and_save_depth(depth_path, save_path):
    # 1) 读取
    img = imageio.v2.imread(depth_path)
    # 2) 如果是彩色图，先转灰度（简单加权转换）
    if img.ndim == 3:
        img = (0.2989 * img[..., 0] + 0.5870 * img[..., 1] + 0.1140 * img[..., 2]).astype(np.float32)
    else:
        img = img.astype(np.float32)

    # 3) 根据读入的位深度决定是否转米
    #    常见：uint16 存的是毫米 -> 除 1000 得到米
    if img.dtype == np.float32 and img.max() > 1000:
        depth_m = img / 1000.0
    elif img.dtype == np.uint16 or img.max() > 255:
        depth_m = img / 1000.0
    else:
        # 已经是 [0,255]，先归一到 [0,1]
        depth_m = img / 255.0

    # 4) 归一化到 [0,1]
    d_min, d_max = float(depth_m.min()), float(depth_m.max())
    if abs(d_max - d_min) < 1e-8:
        norm = np.zeros_like(depth_m, dtype=np.uint8)
    else:
        norm = (((d_max - depth_m) / (d_max - d_min)) * 255.0).clip(0, 255).astype(np.uint8)

    # 5) 拓展到 3 通道
    depth_rgb = np.repeat(norm[..., np.newaxis], 3, axis=-1)

    # 6) 保存图片
    imageio.v2.imwrite(save_path, depth_rgb)

# 用于存放所有转换后的记录
output_list = []

for item in tqdm(data):
    # 提取图片和深度图的原始路径
    frame1_image_path = item["frame1_image"]
    frame2_image_path = item["frame2_image"]
    frame1_depth_path = item["frame1_depth"]
    frame2_depth_path = item["frame2_depth"]

    question = item["question"]  # 原始问题文本
    answer = item["answer"]      # 如 "(B)"
    # 注：question_type 这里不再用来构造提示内容，human 的文本就是原始 question

    # --- 提取 video_id 与 frame_id ---
    # 假设图像路径类似于：
    # .../ca1m-train-42444711/42444711/74020814498416.wide/image_resized.png
    # video_id 取倒数第三个目录，例如 "42444711"
    # frame_id 取倒数第二个目录中的数字部分，去除 ".wide" 后缀
    video_id = os.path.basename(os.path.dirname(os.path.dirname(frame1_image_path)))
    frame1_folder = os.path.basename(os.path.dirname(frame1_image_path))  # 例如 "74020814498416.wide"
    frame2_folder = os.path.basename(os.path.dirname(frame2_image_path))
    frame1_id = frame1_folder.replace(".wide", "")
    frame2_id = frame2_folder.replace(".wide", "")

    # --- 生成新 RGB 图像和深度图的文件名称 ---
    new_frame1_image_name = f"{video_id}_{frame1_id}_wide_image.png"
    new_frame2_image_name = f"{video_id}_{frame2_id}_wide_image.png"
    new_frame1_depth_name = f"{video_id}_{frame1_id}_wide_depth.png"
    new_frame2_depth_name = f"{video_id}_{frame2_id}_wide_depth.png"

    # --- 保存 RGB 图像 ---
    shutil.copy(frame1_image_path, os.path.join(images_out_dir, new_frame1_image_name))
    shutil.copy(frame2_image_path, os.path.join(images_out_dir, new_frame2_image_name))

    # --- 保存深度图（经过预处理） ---
    process_and_save_depth(frame1_depth_path, os.path.join(depths_out_dir, new_frame1_depth_name))
    process_and_save_depth(frame2_depth_path, os.path.join(depths_out_dir, new_frame2_depth_name))

    # --- 构造最终 JSON 对象的 id 与 image/depth 列表 ---
    new_id = f"{video_id}_{frame1_id}"
    image_list = [new_frame1_image_name, new_frame2_image_name]
    depth_list = [new_frame1_depth_name, new_frame2_depth_name]

    # --- 构造 conversations ---
    # human 部分的文本直接使用原始 question 文本
    human_text = question

    # 利用正则表达式从 question 中提取选项
    # 假设 question 格式中包含类似 "(A) rotated left (B) rotated right"
    options = {}
    for match in re.finditer(r"\((A|B)\)\s*([^()]+)", question):
        letter = match.group(1)
        text = match.group(2).strip()
        options[letter] = text

    # 提取 answer 字母，例如 "(B)" -> "B"
    ans_letter = answer.strip("()").upper()
    option_text = options.get(ans_letter, "")
    # 构造 gpt 的回答： "answer" + 对应的选项文本
    # 示例为 "(B) right"
    gpt_text = f"{answer} {option_text}" if option_text else answer

    conversations = [
        {"from": "human", "value": human_text},
        {"from": "gpt", "value": gpt_text}
    ]

    # --- 生成最终 JSON 对象 ---
    out_item = {
        "id": new_id,
        "image": image_list,
        "depth": depth_list,
        "conversations": conversations
    }
    output_list.append(out_item)

# 将所有转换后的记录保存到 output_multi_view_reasoning.json 中
with open("/home_sfs/zhouenshen/dataset/3D/cubifyanything/ca1m_multi_view_qa.json", "w") as f:
    json.dump(output_list, f, indent=2)

# 可打印一项进行检查
print(json.dumps(output_list[0], indent=2))