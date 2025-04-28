
import os
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import cv2
# ========== Supporting Functions ==========
def sort_points_ccw(points):
    """
    将一组 2D 点按逆时针方向排序
    """
    points = np.array(points)
    centroid = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
    sorted_points = points[np.argsort(angles)]
    return sorted_points

def load_json(path):
    import json
    with open(path, 'r') as f:
        return json.load(f)

def load_objects_from_instances(json_path):
    data = load_json(json_path)
    return data["objects"]

def bbox_top_surface_y(corners):
    # 顶部 → y 最小
    return np.min(np.array(corners)[:, 1])

def bbox_bottom_surface_y(corners):
    # 底部 → y 最大
    return np.max(np.array(corners)[:, 1])

def bbox_xz_polygon(corners):
    corners = np.array(corners)
    top_y = np.min(corners[:, 1])  # ✅ Y 向下时，顶部是 y 最小
    top_face = corners[np.abs(corners[:, 1] - top_y) < 1e-3]
    
    xz = top_face[:, [0, 2]]  # 投影到 XZ 平面
    # ✅ 对点进行逆时针排序
    sorted_xz = sort_points_ccw(xz)
    return sorted_xz

def transform_points_with_rotation(R, pts):
    R_inv = np.linalg.inv(R)
    return (R_inv @ pts.T).T

def construct_3d_points(sampled_xz_points, platform_surface_y):
    """
    输入：2D XZ 点 + 平台表面高度 y
    输出：世界坐标系（重力对齐）下的 3D 点
    """
    pts_3d = []
    for x, z in sampled_xz_points:
        pts_3d.append([x, platform_surface_y, z])
    return np.array(pts_3d)

def transform_to_camera_coords(R_gravity, pts_3d):
    """
    将 3D 点从重力对齐坐标系变换回相机坐标系
    """
    return (R_gravity @ pts_3d.T).T

def project_to_image(points_3d_camera, K):
    """
    3D 相机坐标系 → 图像像素坐标
    输入：N x 3 的点，输出：N x 2 的图像像素坐标
    """
    points_3d = points_3d_camera.T  # shape: 3 x N
    points_2d = K @ points_3d       # shape: 3 x N
    points_2d = points_2d[:2, :] / points_2d[2, :]  # 除以 z
    return points_2d.T  # shape: N x 2

def sample_points_in_bbox_xz(obj, num_points=200, scale_rate=0.9):
    """
    在目标物体的 XZ 投影范围内采样点。
    可用于上下方向。

    - margin: 控制点不贴边
    """
    poly = Polygon(bbox_xz_polygon(obj["corners"]))
    scaled_poly = scale_polygon_around_center(poly, scale_rate=scale_rate)  # 缩放
    points = sample_points_in_polygon_uniform(scaled_poly, num_points=num_points)  # 采样点
    return points

from shapely.affinity import scale

def scale_polygon_around_center(poly: Polygon, scale_rate: float) -> Polygon:
    """
    缩放多边形（以质心为中心缩放）
    """
    origin = poly.centroid
    return scale(poly, xfact=scale_rate, yfact=scale_rate, origin=origin)

from shapely.geometry import Polygon, Point, MultiPolygon
import numpy as np
import random
from shapely.ops import triangulate
from typing import Union

def sample_points_in_polygon_uniform(polygon: Union[Polygon, MultiPolygon], num_points: int):
    """
    在 Polygon 或 MultiPolygon 内部均匀采样点，使用三角剖分 + 面积加权方式。

    参数：
    - polygon: shapely.geometry.Polygon 或 MultiPolygon
    - num_points: 总采样数量

    返回：
    - List of (x, z) 点坐标
    """

    # 如果是 MultiPolygon，拆分为多个 Polygon
    polygons = []
    if isinstance(polygon, Polygon):
        polygons = [polygon]
    elif isinstance(polygon, MultiPolygon):
        polygons = list(polygon.geoms)
    else:
        raise ValueError(f"Unsupported geometry type: {type(polygon)}")

    # Step 1: 对每个 polygon 进行三角剖分，并收集所有有效三角形
    all_triangles = []
    all_areas = []

    for poly in polygons:
        tris = triangulate(poly)
        valid_tris = [t for t in tris if poly.contains(t.centroid)]
        all_triangles.extend(valid_tris)
        all_areas.extend([t.area for t in valid_tris])

    if not all_triangles:
        print("⚠️ 没有有效的三角形用于采样")
        return []

    # Step 2: 建立面积加权概率分布
    areas = np.array(all_areas)
    cumulative_areas = np.cumsum(areas)
    total_area = cumulative_areas[-1]

    points = []

    for _ in range(num_points):
        r = random.uniform(0, total_area)
        tri_index = np.searchsorted(cumulative_areas, r)
        triangle = all_triangles[tri_index]

        # Step 3: 在三角形内均匀采点
        a, b, c = triangle.exterior.coords[:3]  # 只取前三个点
        r1 = np.sqrt(random.random())
        r2 = random.random()
        x = (1 - r1) * a[0] + r1 * (1 - r2) * b[0] + r1 * r2 * c[0]
        z = (1 - r1) * a[1] + r1 * (1 - r2) * b[1] + r1 * r2 * c[1]
        points.append((x, z))

    return points

def draw_points_on_image(image, points_2d, color=(0, 255, 0)):
    """
    在图像上绘制 2D 点
    """
    img = image.copy()
    for pt in points_2d:
        x, y = int(pt[0]), int(pt[1])
        if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
            cv2.circle(img, (x, y), radius=1, color=color, thickness=-1)
    return img

def overlap_ratio_with_target(poly_platform, poly_target):
    p1 = Polygon(poly_platform)
    p2 = Polygon(poly_target)
    if not p1.intersects(p2):
        return 0.0
    return p1.intersection(p2).area / p2.area

def find_platform_for_target(target_obj, all_objects, height_thresh=0.02, overlap_thresh=0.7):
    target_bottom_y = bbox_bottom_surface_y(target_obj["corners"])
    target_poly = bbox_xz_polygon(target_obj["corners"])

    for obj in all_objects:
        if obj["id"] == target_obj["id"]:
            continue
        obj_top_y = bbox_top_surface_y(obj["corners"])
        if abs(target_bottom_y - obj_top_y) < height_thresh:
            platform_poly = bbox_xz_polygon(obj["corners"])
            overlap = overlap_ratio_with_target(platform_poly, target_poly)
            if overlap > overlap_thresh:
                return obj
    return None

def compute_placeable_area(platform_obj, obstacles):
    platform_poly = Polygon(bbox_xz_polygon(platform_obj["corners"]))
    for obj in obstacles:
        if obj["id"] == platform_obj["id"]:
            continue
        poly = Polygon(bbox_xz_polygon(obj["corners"]))
        if poly.intersects(platform_poly):
            platform_poly = platform_poly.difference(poly)
    return platform_poly

def find_objects_on_platform(target_obj, platform_obj, all_objects):
    target_top_y = bbox_top_surface_y(target_obj["corners"])
    platform_top_y = bbox_top_surface_y(platform_obj["corners"])
    platform_poly = Polygon(bbox_xz_polygon(platform_obj["corners"]))
    target_scale = target_obj["scale"]

    objects_on_platform = []

    for obj in all_objects:
        if obj["id"] == platform_obj["id"]:
            continue
        if obj["id"] == target_obj["id"]:
            objects_on_platform.append(obj)
            continue

        obj_bottom_y = bbox_bottom_surface_y(obj["corners"])
        obj_top_y = bbox_top_surface_y(obj["corners"])
        obj_scale = obj["scale"]

        # ✅ 条件 1：底部高于目标物体顶部，舍弃
        if obj_bottom_y < target_top_y:
            continue

        # ✅ 条件 2：顶部低于平台顶部，舍弃
        if obj_top_y > platform_top_y:
            continue
          
        # ✅ 条件 3：底部高于平台顶部20cm，舍弃  
        if obj_bottom_y < platform_top_y - 0.2: 
            continue

        # ✅ 条件 5：物体的体积比目标物体的体积的4.236倍大，舍弃（平均每个边是目标物体的0.5倍）
        if obj_scale[0] * obj_scale[1] * obj_scale[2] > target_scale[0] * target_scale[1] * target_scale[2] * 4.236:
            continue

        # ✅ 条件 4：XZ 平面有交集
        try:
            obj_poly = Polygon(bbox_xz_polygon(obj["corners"])).buffer(0)
            if obj_poly.is_valid and obj_poly.intersects(platform_poly):
                objects_on_platform.append(obj)
        except Exception as e:
            print(f"[WARNING] Failed to process object {obj['id']}: {e}")
            continue

    return objects_on_platform

import cv2
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
from shapely.geometry import Point

def sample_placeable_points_in_fan(placeable_poly, target_obj, direction="left", base_radius=0.3, fan_angle_deg=90, num_rays=90, num_samples_per_ray=100):
    """
    在目标物体指定方向的扇形区域内采样点并返回其中属于 placeable_poly 的点。

    direction: 'left', 'right', 'front', 'back'
    """
    direction_map = {
        "left": np.pi,            # 180°
        "right": 0,               # 0°
        "front": 3* np.pi / 2,       # 270°
        "back": np.pi / 2     # 90°
    }

    if direction not in direction_map:
        raise ValueError(f"Invalid direction: {direction}")

    fan_center_angle_rad = direction_map[direction]
    fan_half_angle_rad = np.radians(fan_angle_deg / 2)

    corners = np.array(target_obj["corners"])
    center = np.mean(corners[:, [0, 2]], axis=0)

    # 计算对角线长度作为参考半径
    xz = corners[:, [0, 2]]
    diag_len = np.max(np.linalg.norm(xz - center, axis=1)) * 2
    radius = max(base_radius, diag_len)

    angles = np.linspace(fan_center_angle_rad - fan_half_angle_rad,
                         fan_center_angle_rad + fan_half_angle_rad,
                         num_rays)

    valid_points = []

    for angle in angles:
        direction_vec = np.array([np.cos(angle), np.sin(angle)])
        for r in np.linspace(0.05, radius, num_samples_per_ray):
            point = center + direction_vec * r
            shapely_point = Point(point[0], point[1])
            if placeable_poly.contains(shapely_point):
                valid_points.append((point[0], point[1]))

    return valid_points
def compute_center_of_points(points):
    """
    给定一组 (x, z) 点，返回中心点坐标 (x_center, z_center)
    """
    if not points:
        return None
    points = np.array(points)
    center = np.mean(points, axis=0)
    return tuple(center)
def plot_single_direction_fan(platform_obj, target_obj, obstacles, placeable_poly, sampled_points, direction):
    fig, ax = plt.subplots(figsize=(8, 8))

    def draw_poly(poly, color, label, alpha=0.5):
        if isinstance(poly, Polygon):
            x, z = poly.exterior.xy
            ax.fill(x, z, alpha=alpha, color=color, label=label)

    draw_poly(Polygon(bbox_xz_polygon(platform_obj["corners"])), 'blue', "Platform")
    draw_poly(Polygon(bbox_xz_polygon(target_obj["corners"])), 'red', "Target")
    for obj in obstacles:
        draw_poly(Polygon(bbox_xz_polygon(obj["corners"])), 'gray', "Obstacle")
    draw_poly(placeable_poly, 'green', "Placeable Area")

    if sampled_points:
        pts = np.array(sampled_points)
        ax.scatter(pts[:, 0], pts[:, 1], color='orange', label=f"{direction.capitalize()} Points", s=20, zorder=10)

        # ✅ 添加中心点（红色星星）
        center = np.mean(pts, axis=0)
        ax.plot(center[0], center[1], marker='*', color='red', markersize=18, label="Center Point", zorder=20)

    ax.set_aspect('equal')
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Z (meters)")
    ax.set_title(f"Sampled Placeable Points - {direction.capitalize()}")
    ax.legend()
    ax.grid(True)
    plt.show()

def filter_visible_points_by_depth(pts_img, pts_cam, depth_map, depth_threshold=0.025):
    """
    通过对比相机深度图来剔除被遮挡的点

    参数：
    - pts_img: N x 2 的图像坐标
    - pts_cam: N x 3 的相机坐标，Z 是深度
    - depth_map: H x W 的深度图（单位需一致）
    - depth_threshold: 允许的最大深度误差（单位：米）

    返回：
    - visible_pts_img, visible_pts_cam：可见的点
    """
    visible_pts_img = []
    visible_pts_cam = []

    h, w = depth_map.shape
    for (u, v), cam_pt in zip(pts_img, pts_cam):
        x, y = int(round(u)), int(round(v))
        if 0 <= x < w and 0 <= y < h:
            depth_from_map = depth_map[y, x]
            depth_from_cam = cam_pt[2]
            if abs(depth_from_cam - depth_from_map) < depth_threshold:
                visible_pts_img.append([u, v])
                visible_pts_cam.append(cam_pt)

    return np.array(visible_pts_img), np.array(visible_pts_cam)

def plot_placeable_area(platform_obj, target_obj, obstacles, placeable_poly):
    fig, ax = plt.subplots(figsize=(8, 8))

    def draw_poly(poly, color, label, alpha=0.5):
        if isinstance(poly, Polygon):
            x, z = poly.exterior.xy
            ax.fill(x, z, alpha=alpha, color=color, label=label)

    draw_poly(Polygon(bbox_xz_polygon(platform_obj["corners"])), 'blue', "Platform")
    draw_poly(Polygon(bbox_xz_polygon(target_obj["corners"])), 'red', "Target")
    for obj in obstacles:
        draw_poly(Polygon(bbox_xz_polygon(obj["corners"])), 'yellow', "Obstacle")
    draw_poly(placeable_poly, 'green', "Placeable Area")

    ax.set_aspect('equal')
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Z (meters)")
    ax.set_title("Top-Down View on X-Z Plane")
    ax.legend()
    ax.grid(True)
    plt.show()
    
def select_and_draw_representative_point(
    image, pts_img, pts_cam, depth_map, direction, min_required=150,
    depth_threshold=0.025, point_color=(0, 0, 255)
):
    """
    从一组投影点中选一个代表点（平均点或最近点），并绘制在图像上。

    参数：
    - image: 原图像
    - pts_img: N x 2 图像点
    - pts_cam: N x 3 相机坐标点
    - depth_map: 深度图
    - direction: 当前方向字符串（用于标题）
    - min_required: 最小合法点数，少于此视为无放置点
    - depth_threshold: 判断遮挡的深度误差阈值
    """
    if len(pts_img) < min_required:
        print(f"[{direction}] Too few points ({len(pts_img)}), skipping.")
        return image, None, None

    # 1. 计算平均点
    avg_pt = np.mean(pts_img, axis=0)
    avg_depth = np.mean(pts_cam[:, 2])

    h, w = depth_map.shape
    x, y = int(round(avg_pt[0])), int(round(avg_pt[1]))

    # 2. 判断是否遮挡
    if 0 <= x < w and 0 <= y < h:
        depth_map_val = depth_map[y, x]
        depth_diff = abs(depth_map_val - avg_depth)
        if depth_diff <= depth_threshold:
            chosen_pt = avg_pt
            reason = "avg OK"
        else:
            # 3. 遮挡 → 找最近点
            dists = np.linalg.norm(pts_img - avg_pt, axis=1)
            nearest_idx = np.argmin(dists)
            chosen_pt = pts_img[nearest_idx]
            reason = "avg blocked → nearest used"
    else:
        chosen_pt = pts_img[np.argmin(np.linalg.norm(pts_img - avg_pt, axis=1))]
        reason = "avg out of bounds → nearest used"

    # 4. 绘图
    img_out = image.copy()
    cx, cy = int(round(chosen_pt[0])), int(round(chosen_pt[1]))
    if 0 <= cx < w and 0 <= cy < h:
        cv2.circle(img_out, (cx, cy), radius=6, color=point_color, thickness=-1)

    # 5. 显示
    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB))
    plt.title(f"{direction.upper()} Representative Point ({reason})")
    plt.axis("off")
    plt.show()

    return img_out, chosen_pt, reason


def select_representative_point(
    pts_img, pts_cam, depth_map,
    depth_threshold=0.025
):
    """
    从一组投影点中选一个代表点（平均点或最近点），并绘制在图像上。

    参数：
    - pts_img: N x 2 图像点
    - pts_cam: N x 3 相机坐标点
    - depth_map: 深度图
    - depth_threshold: 判断遮挡的深度误差阈值
    """

    # 1. 计算平均点
    avg_pt = np.mean(pts_img, axis=0)
    avg_depth = np.mean(pts_cam[:, 2])

    h, w = depth_map.shape
    x, y = int(round(avg_pt[0])), int(round(avg_pt[1]))

    # 2. 判断是否遮挡
    if 0 <= x < w and 0 <= y < h:
        depth_map_val = depth_map[y, x]
        depth_diff = abs(depth_map_val - avg_depth)
        if depth_diff <= depth_threshold:
            chosen_pt = avg_pt
            reason = "avg OK"
        else:
            # 3. 遮挡 → 找最近点
            dists = np.linalg.norm(pts_img - avg_pt, axis=1)
            nearest_idx = np.argmin(dists)
            chosen_pt = pts_img[nearest_idx]
            reason = "avg blocked → nearest used"
    else:
        chosen_pt = pts_img[np.argmin(np.linalg.norm(pts_img - avg_pt, axis=1))]
        reason = "avg out of bounds → nearest used"

    return chosen_pt

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

def find_objects_on_platform_below_target(target_obj, platform_obj, all_objects):
    target_top_y = bbox_top_surface_y(target_obj["corners"])
    platform_top_y = bbox_top_surface_y(platform_obj["corners"])
    target_poly = Polygon(bbox_xz_polygon(target_obj["corners"]))

    objects_on_platform = []

    for obj in all_objects:
        if obj["id"] == platform_obj["id"]:
            continue
            
        if obj["id"] == target_obj["id"]:
            continue

        obj_bottom_y = bbox_bottom_surface_y(obj["corners"])
        obj_top_y = bbox_top_surface_y(obj["corners"])
        
        obj_poly = Polygon(bbox_xz_polygon(obj["corners"])).buffer(0)
        
        # ✅ 条件 4：XZ 平面有交集
        if not obj_poly.is_valid or not obj_poly.intersects(target_poly):
            continue

        # ✅ 条件 1：底部高于目标物体顶部，舍弃
        if obj_bottom_y < target_top_y:
            continue

        # ✅ 条件 2：顶部低于平台顶部，舍弃
        if obj_top_y > platform_top_y:
            continue
          
        # ✅ 条件 3：底部高于平台顶部20cm，舍弃  
        if obj_bottom_y < platform_top_y - 0.2: 
            continue

        objects_on_platform.append(obj)

    return objects_on_platform

def find_platform_below_target(target_obj, all_objects, height_buffer=0.02, overlap_thresh=0.7):
    """
    找到位于目标物体下方的平台（适用于“below”情形）
    - 平台顶部必须低于目标物体底部上方 height_buffer 范围内
    - 平台的 XZ 投影需与目标物体有重叠
    - 若多个平台满足，返回离目标最近的
    """
    target_bottom_y = bbox_bottom_surface_y(target_obj["corners"])
    threshold_y = target_bottom_y - height_buffer
    target_poly = bbox_xz_polygon(target_obj["corners"])


    candidate_platforms = []

    for obj in all_objects:
        if obj["id"] == target_obj["id"]:
            continue

        obj_top_y = bbox_top_surface_y(obj["corners"])
        platform_poly = bbox_xz_polygon(obj["corners"])

        # 1. 平台顶部必须低于目标底部 - buffer
        if obj_top_y < threshold_y:
            continue

        # 2. XZ 平面有重叠
        overlap = overlap_ratio_with_target(platform_poly, target_poly)
        if overlap > overlap_thresh:
            candidate_platforms.append((obj, abs(target_bottom_y - obj_top_y)))

    # 3. 选择距离目标最近的平台（最小的 y 差值）
    if candidate_platforms:
        candidate_platforms.sort(key=lambda x: x[1])  # 按 y 距离升序排序
        return candidate_platforms[0][0]

    return None

def sample_points_in_bbox_xz_below(obj, placeable_poly, num_points=300, scale_rate=0.75):
    """
    在目标物体的 XZ 投影范围内采样点。
    可用于上下方向。

    - margin: 控制点不贴边
    """
    poly = Polygon(bbox_xz_polygon(obj["corners"]))
    scaled_poly = scale_polygon_around_center(poly, scale_rate=scale_rate)  # 缩放
    points = sample_points_in_polygon_uniform(scaled_poly, num_points=num_points)  # 采样点
    valid_points = []
    for point in points:
        shapely_point = Point(point[0], point[1])
        if placeable_poly.contains(shapely_point):
            valid_points.append(point)
    return valid_points

def find_objects_on_two_target_platform(target_obj_1, target_obj_2, platform_obj, all_objects):
    target_1_top_y = bbox_top_surface_y(target_obj_1["corners"])
    target_1_scale = target_obj_1["scale"]
    target_2_top_y = bbox_top_surface_y(target_obj_2["corners"])
    target_2_scale = target_obj_2["scale"]
    platform_top_y = bbox_top_surface_y(platform_obj["corners"])
    platform_poly = Polygon(bbox_xz_polygon(platform_obj["corners"]))

    objects_on_platform = []

    for obj in all_objects:
        if obj["id"] == platform_obj["id"]:
            continue
        if obj["id"] == target_obj_1["id"] or obj["id"] == target_obj_2["id"]:
            objects_on_platform.append(obj)
            continue

        obj_bottom_y = bbox_bottom_surface_y(obj["corners"])
        obj_top_y = bbox_top_surface_y(obj["corners"])
        obj_scale = obj["scale"]

        # ✅ 条件 1：底部高于目标物体顶部，舍弃
        if obj_bottom_y < max(target_1_top_y, target_2_top_y):
            continue

        # ✅ 条件 2：顶部低于平台顶部，舍弃
        if obj_top_y > platform_top_y:
            continue
          
        # ✅ 条件 3：底部高于平台顶部20cm，舍弃  
        if obj_bottom_y < platform_top_y - 0.2: 
            continue

        # ✅ 条件 5：物体的体积比目标物体的体积的4.236(黄金分割比倒数的三次方）倍大，舍弃（平均每个边是目标物体的1/0.618倍），
        # 为什么舍弃，因为如果是实心物体，depth会过滤掉，如果是空心，比如桌子等下面是空的也认为是不占用空间的
        if obj_scale[0] * obj_scale[1] * obj_scale[2] > max(target_1_scale[0] * target_1_scale[1] * target_1_scale[2] * 4.236, target_2_scale[0] * target_2_scale[1] * target_2_scale[2] * 2):
            continue

        # ✅ 条件 4：XZ 平面有交集
        try:
            obj_poly = Polygon(bbox_xz_polygon(obj["corners"])).buffer(0)
            if obj_poly.is_valid and obj_poly.intersects(platform_poly):
                objects_on_platform.append(obj)
        except Exception as e:
            print(f"[WARNING] Failed to process object {obj['id']}: {e}")
            continue
    
    return objects_on_platform

from shapely.ops import unary_union

def compute_between_placeable_area(target_obj_1, target_obj_2, platform_obj, obstacles):
    """
    计算两个物体之间的可放置区域
    """

    poly_1 = Polygon(bbox_xz_polygon(target_obj_1["corners"]))
    poly_2 = Polygon(bbox_xz_polygon(target_obj_2["corners"]))

    # 计算凸包区域（包括两个矩形）
    union_poly = unary_union([poly_1, poly_2])
    convex_hull = union_poly.convex_hull

    # 从凸包中减去两个矩形，得到中间区域
    between_area = convex_hull.difference(poly_1.union(poly_2))

    platform_poly = Polygon(bbox_xz_polygon(platform_obj["corners"]))

    between_area = between_area.intersection(platform_poly)

    for obj in obstacles:
        poly = Polygon(bbox_xz_polygon(obj["corners"]))
        if poly.intersects(between_area):
            between_area = between_area.difference(poly)

    return between_area

def get_between_area(target_obj_1, target_obj_2, platform_obj):

    poly_1 = Polygon(bbox_xz_polygon(target_obj_1["corners"]))
    poly_2 = Polygon(bbox_xz_polygon(target_obj_2["corners"]))

    # 计算凸包区域（包括两个矩形）
    union_poly = unary_union([poly_1, poly_2])
    convex_hull = union_poly.convex_hull

    # 从凸包中减去两个矩形，得到中间区域
    between_area = convex_hull.difference(poly_1.union(poly_2))

    platform_poly = Polygon(bbox_xz_polygon(platform_obj["corners"]))

    between_area = between_area.intersection(platform_poly)

    return between_area


def sample_placeable_points_in_between_area(between_placeable_poly, target_obj_1, target_obj_2, platform_obj, num_samples=1000):
    """
    在两个物体之间的可放置区域内采样点
    """
    poly_1 = Polygon(bbox_xz_polygon(target_obj_1["corners"]))
    poly_2 = Polygon(bbox_xz_polygon(target_obj_2["corners"]))

    # 计算凸包区域（包括两个矩形）
    union_poly = unary_union([poly_1, poly_2])
    convex_hull = union_poly.convex_hull

    # 从凸包中减去两个矩形，得到中间区域
    between_area = convex_hull.difference(poly_1.union(poly_2))

    platform_poly = Polygon(bbox_xz_polygon(platform_obj["corners"]))

    between_area = between_area.intersection(platform_poly)

    points = sample_points_in_polygon_uniform(between_area, num_points=num_samples)  # 采样点

    valid_points = []

    for point in points:
        shapely_point = Point(point[0], point[1])
        if between_placeable_poly.contains(shapely_point):
            valid_points.append(point)
    return valid_points

def find_max_variance_direction(A, B):
    objs = [A, B]

    # 提取各个方向的值
    x_vals = [obj['position'][0] for obj in objs]
    z_vals = [np.min(np.array(obj['corners'])[:, 2]) for obj in objs]

    # 计算方差
    variances = {
        'x': np.var(x_vals),
        'z': np.var(z_vals)
    }

    # 选择最大方差的方向
    max_dir = max(variances, key=variances.get)
    return max_dir