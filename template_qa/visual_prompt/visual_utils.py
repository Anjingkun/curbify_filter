import os
from pathlib import Path
import cv2
import random
import numpy as np
from typing import Dict

def draw_one_bbox_on_image(image_path, A, bbox_color=(0, 0, 255), output_folder_name="image_with_bbox"):
    # 1. 获取帧目录路径
    frame_dir = str(Path(image_path).parent.parent)  # 上两级目录

    # 2. 创建 image_with_bbox 文件夹
    output_dir = Path(frame_dir) / output_folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. 统计已有文件数量
    existing_files = list(output_dir.glob("*.png"))
    next_index = len(existing_files)
    output_image_path = output_dir / f"{next_index}.png"

    # 4. 读取图片并绘制 bbox
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    x1, y1, x2, y2 = map(int, A["bbox_resized"])
    color = bbox_color  # 红色（注意 OpenCV 用的是 BGR 顺序）
    thickness = 2

    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    # 5. 保存图片
    cv2.imwrite(str(output_image_path), image)

    return str(output_image_path)

def draw_two_bbox_on_image(image_path, A, B, A_bbox_color=(0, 0, 255), B_bbox_color=(255, 0, 0), output_folder_name="image_with_bbox"):
    # 1. 获取帧目录路径（上两级）
    frame_dir = str(Path(image_path).parent.parent)

    # 2. 创建 image_with_bbox 文件夹
    output_dir = Path(frame_dir) / output_folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. 统计已有文件数量
    existing_files = list(output_dir.glob("*.png"))
    next_index = len(existing_files)
    output_image_path = output_dir / f"{next_index}.png"

    # 4. 读取图片
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 5. 画 A 的红框
    x1, y1, x2, y2 = map(int, A["bbox_resized"])
    cv2.rectangle(image, (x1, y1), (x2, y2), A_bbox_color, 2)

    # 6. 画 B 的蓝框
    x1_b, y1_b, x2_b, y2_b = map(int, B["bbox_resized"])
    cv2.rectangle(image, (x1_b, y1_b), (x2_b, y2_b), B_bbox_color, 2)

    # 7. 保存图像
    cv2.imwrite(str(output_image_path), image)

    return str(output_image_path)

def draw_three_bbox_on_image(image_path, A, B, C,
                           A_bbox_color=(255, 0, 0),   # 蓝色
                           B_bbox_color=(0, 255, 0),   # 绿色
                           C_bbox_color=(0, 0, 255),   # 红色
                           output_folder_name="image_with_bbox"):

    # 1. 获取帧目录路径（上两级）
    frame_dir = str(Path(image_path).parent.parent)

    # 2. 创建 image_with_bbox 文件夹
    output_dir = Path(frame_dir) / output_folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. 统计已有文件数量
    existing_files = list(output_dir.glob("*.png"))
    next_index = len(existing_files)
    output_image_path = output_dir / f"{next_index}.png"

    # 4. 读取图片
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 5. 画 C 的红框
    x1_c, y1_c, x2_c, y2_c = map(int, C["bbox_resized"])
    cv2.rectangle(image, (x1_c, y1_c), (x2_c, y2_c), C_bbox_color, 2)

    # 6. 画 A 的蓝框
    x1_a, y1_a, x2_a, y2_a = map(int, A["bbox_resized"])
    cv2.rectangle(image, (x1_a, y1_a), (x2_a, y2_a), A_bbox_color, 2)

    # 7. 画 B 的绿框
    x1_b, y1_b, x2_b, y2_b = map(int, B["bbox_resized"])
    cv2.rectangle(image, (x1_b, y1_b), (x2_b, y2_b), B_bbox_color, 2)

    # 8. 保存图像
    cv2.imwrite(str(output_image_path), image)

    return str(output_image_path)

def calculate_distances_between_point_clouds(A, B, human_readable=True):
    dist_pcd1_to_pcd2 = np.asarray(A.compute_point_cloud_distance(B))
    dist_pcd2_to_pcd1 = np.asarray(B.compute_point_cloud_distance(A))
    combined_distances = np.concatenate((dist_pcd1_to_pcd2, dist_pcd2_to_pcd1))
    avg_dist = np.mean(combined_distances)
    if human_readable:
        return human_like_distance(avg_dist)
    else:
        return avg_dist

def human_like_distance(distance_meters):
    # Define the choices with units included, focusing on the 0.1 to 10 meters range
    if distance_meters < 1:  # For distances less than 1 meter
        choices = [
            (
                round(distance_meters * 100, 2),
                "centimeters",
                0.2,
            ),  # Centimeters for very small distances
            (
                round(distance_meters * 39.3701, 2),
                "inches",
                0.8,
            ),  # Inches for the majority of cases under 1 meter
        ]
    elif distance_meters < 3:  # For distances less than 3 meters
        choices = [
            (round(distance_meters, 2), "meters", 0.5),
            (
                round(distance_meters * 3.28084, 2),
                "feet",
                0.5,
            ),  # Feet as a common unit within indoor spaces
        ]
    else:  # For distances from 3 up to 10 meters
        choices = [
            (
                round(distance_meters, 2),
                "meters",
                0.7,
            ),  # Meters for clarity and international understanding
            (
                round(distance_meters * 3.28084, 2),
                "feet",
                0.3,
            ),  # Feet for additional context
        ]

    # Normalize probabilities and make a selection
    total_probability = sum(prob for _, _, prob in choices)
    cumulative_distribution = []
    cumulative_sum = 0
    for value, unit, probability in choices:
        cumulative_sum += probability / total_probability  # Normalize probabilities
        cumulative_distribution.append((cumulative_sum, value, unit))

    # Randomly choose based on the cumulative distribution
    r = random.random()
    for cumulative_prob, value, unit in cumulative_distribution:
        if r < cumulative_prob:
            return f"{value:.2f} {unit}"

    # Fallback to the last choice if something goes wrong
    return f"{choices[-1][0]:.2f} {choices[-1][1]}"

# RLE解码函数（根据之前提供的实现）
def rle_2_mask(rle: Dict) -> np.ndarray:
    """支持COCO压缩和未压缩RLE格式的解码"""
    if isinstance(rle['counts'], str):
        from pycocotools import mask as mask_utils
        rle_obj = {
            'size': rle['size'],
            'counts': rle['counts'].encode('utf-8')
        }
        decoded = mask_utils.decode(rle_obj)
        return decoded.astype(bool)
    else:
        h, w = rle['size']
        counts = list(map(int, rle['counts']))
        mask = np.zeros(h * w, dtype=bool)
        idx = 0
        parity = False
        for count in counts:
            mask[idx:idx+count] = parity
            idx += count
            parity ^= True
        return mask.reshape((w, h)).transpose()

# 在mask上随机采样点
def get_random_point(mask):
    y_indices, x_indices = np.where(mask)
    if len(y_indices) == 0:
        return None  # 处理空mask异常
    idx = np.random.choice(len(y_indices))
    return (y_indices[idx], x_indices[idx])  # 返回(y,x)格式

def draw_two_point_on_image(image_path, A_point_yx, B_point_yx, output_folder_name="image_with_points"):
    # 1. 获取帧目录路径（上两级）
    frame_dir = str(Path(image_path).parent.parent)

    # 2. 创建输出目录
    output_dir = Path(frame_dir) / output_folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. 自动编号保存图像
    existing_files = list(output_dir.glob("*.png"))
    next_index = len(existing_files)
    output_image_path = output_dir / f"{next_index}.png"

    # 4. 读取图像
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 5. 绘制点函数
    def draw_labeled_point(img, point_yx, label):
        y, x = map(int, point_yx)
        radius = 6
        circle_color = (0, 0, 255)  # 红色
        text_color = (255, 255, 255)  # 白字
        bg_color = (0, 0, 0)  # 黑底
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1

        # 画圆圈
        cv2.circle(img, (x, y), radius, circle_color, -1)

        # 计算文字大小
        (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)
        padding = 4
        text_x = x - text_w // 2
        text_y = y - radius - 10

        # 画黑底方框
        cv2.rectangle(img,
                      (text_x - padding, text_y - text_h - padding),
                      (text_x + text_w + padding, text_y + baseline + padding),
                      bg_color, -1)

        # 写白字
        cv2.putText(img, label, (text_x, text_y), font, font_scale, text_color, thickness, cv2.LINE_AA)

    # 6. 绘制 A 和 B 点
    draw_labeled_point(image, A_point_yx, "A")
    draw_labeled_point(image, B_point_yx, "B")

    # 7. 保存图像
    cv2.imwrite(str(output_image_path), image)

    return str(output_image_path)