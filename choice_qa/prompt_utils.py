import numpy as np
from typing import Dict
import random
import trimesh

def smart_insert(desc, dense, placeholder, sentence):
    """根据是否含定语从句，智能插入描述，加不加逗号"""
    
    # 如果找不到占位符，直接返回原句（不做替换）
    if placeholder not in sentence:
        return sentence

    if desc == dense:
        return sentence.replace(placeholder, desc)

    # 查找 placeholder 后的内容
    idx = sentence.find(placeholder)
    after = sentence[idx + len(placeholder):].lstrip()

    # 如果是结尾或后面是标点，不加逗号
    if not after or after[0] in {",", ".", "?"}:
        return sentence.replace(placeholder, desc)

    # 其他情况加逗号
    return sentence.replace(placeholder, desc + ",")

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

def calculate_distances_between_point_clouds(A, B, human_readable=True):
    dist_pcd1_to_pcd2 = np.asarray(A.compute_point_cloud_distance(B))
    dist_pcd2_to_pcd1 = np.asarray(B.compute_point_cloud_distance(A))
    combined_distances = np.concatenate((dist_pcd1_to_pcd2, dist_pcd2_to_pcd1))
    avg_dist = np.mean(combined_distances)
    if human_readable:
        return human_like_distance(avg_dist)
    else:
        return avg_dist

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

def ray_intersects_obb(ray_origin, ray_dir, corners):
    box = trimesh.Trimesh(vertices=corners, faces=[
        [0, 1, 2], [0, 2, 3],  # bottom
        [4, 5, 6], [4, 6, 7],  # top
        [0, 1, 5], [0, 5, 4],  # side
        [2, 3, 7], [2, 7, 6],  # side
        [1, 2, 6], [1, 6, 5],  # side
        [3, 0, 4], [3, 4, 7]   # side
    ])
    locations, index_ray, index_tri = box.ray.intersects_location(
        ray_origins=[ray_origin],
        ray_directions=[ray_dir]
    )
    return len(locations) > 0

def normalize(v):
    return v / np.linalg.norm(v)

def angle_between_vectors(v1, v2):
    v1 = normalize(v1)
    v2 = normalize(v2)
    cos_theta = np.clip(np.dot(v1, v2), -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    return np.degrees(angle_rad)

def is_point_in_view_cone(B_center, apex, front_points):
    """
    判断 B_center 是否在由 apex → front_points 四方向张成的四棱‘视线锥体’中

    参数:
        B_center: 目标点位置
        apex: 锥体顶点（A 的中心）
        front_points: A 正面的四个角点 (4,3)

    返回:
        bool: 是否在 cone 中（无限延伸）
    """
    # 构建 4 个方向向量（Apex → 正面四角点）
    dirs = [normalize(pt - apex) for pt in front_points]
    B_dir = normalize(B_center - apex)

    # 构建四个面的法向量，每个面由两条相邻方向向量组成
    for i in range(4):
        v1 = dirs[i]
        v2 = dirs[(i + 1) % 4]
        normal = normalize(np.cross(v1, v2))

        # 判断 B_dir 是否在这个面“内侧”
        if np.dot(normal, B_dir) < 0:
            return False  # 在面外

    return True  # 所有面都在内侧

def sort_points_cw(points, normal):
    """
    将 3D 点按在 normal 平面上的投影进行顺时针排序
    """
    center = np.mean(points, axis=0)
    normal = normalize(normal)
    ref_axis = normalize(points[0] - center)

    def angle_from_ref(p):
        v = normalize(p - center)
        angle = np.arctan2(
            np.dot(np.cross(ref_axis, v), normal),
            np.dot(ref_axis, v)
        )
        return angle  # 顺时针

    sorted_points = sorted(points, key=angle_from_ref)
    return np.array(sorted_points)

def solve_t_for_angle(u: np.ndarray, f: np.ndarray, angle_deg: float):
    """
    求解在 u - t*f 与 f 夹角为 angle_deg 时的 t 值
    """
    cos_theta = np.cos(np.deg2rad(angle_deg))
    f_dot_f = np.dot(f, f)
    u_dot_u = np.dot(u, u)
    u_dot_f = np.dot(u, f)

    # 构造方程: c^2 * ||u - t f||^2 = (u - t f)·f)^2
    # 左边: c^2 * (u·u - 2t u·f + t^2 f·f)
    # 右边: (u·f - t f·f)^2

    # 展开后得到二次方程: At^2 + Bt + C = 0
    A = cos_theta**2 * f_dot_f - f_dot_f**2
    B = -2 * cos_theta**2 * u_dot_f + 2 * u_dot_f * f_dot_f
    C = cos_theta**2 * u_dot_u - u_dot_f**2

    # 解二次方程
    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        return None  # 无实数解

    sqrt_disc = np.sqrt(discriminant)
    t1 = (-B + sqrt_disc) / (2 * A)
    t2 = (-B - sqrt_disc) / (2 * A)

    # 返回正数解
    t_candidates = [t1, t2]
    return min(t_candidates) if t_candidates else None

def find_point_with_angle_math(A_pos, A_front, front_points, angle_deg=30):
    A_pos = np.array(A_pos)
    A_front = normalize(np.array(A_front))

    for F in front_points:
        u = np.array(F) - A_pos
        t = solve_t_for_angle(u, A_front, angle_deg)
        if t is not None:
            P = A_pos + t * A_front
            return P, F, t

    return None, None, None

def sample_points_in_unit_bbox(n=1000):
    """在单位立方体 [-0.5, 0.5]^3 中均匀采样 n 个点"""
    return np.random.uniform(low=-0.5, high=0.5, size=(n, 3))

def transform_points(points, scale, R, pos):
    """从局部坐标系变换到世界坐标系"""
    return (R @ (points * scale).T).T + pos

def inverse_transform_points(points, scale, R, pos):
    """将世界坐标系中的点变换为 A 的局部坐标系"""
    return ((np.linalg.inv(R) @ (points - pos).T).T) / scale