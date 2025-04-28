import random
from itertools import combinations
from itertools import permutations
import imageio
import numpy as np
from fact_template import *
from fact_utils import *
from skimage.measure import label, regionprops
from scipy.spatial import cKDTree
import open3d as o3d
import json

# Obj predicate -------------------------------------------------------------------------------
def left_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = left_true_responses
    false_responses = left_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    is_left = A_pos[0] < B_pos[0]

    response_template = random.choice(true_responses if is_left else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def image_below_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = image_below_true_responses
    false_responses = image_below_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    is_below = A_pos[1] > B_pos[1]

    response_template = random.choice(true_responses if is_below else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def world_below_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = world_below_true_responses
    false_responses = world_below_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    # 1. 读取旋转矩阵（gravity 对齐矩阵）
    T_gravity_path = wide_depth_path.replace("depth.png", "T_gravity.json")
    with open(T_gravity_path, "r") as f:
        R = json.load(f)
    R = np.array(R, dtype=np.float64)

    # 2. 获取 A/B 的原始相机坐标系下的位置（3D）
    A_pos = np.array(A["position"], dtype=np.float64)  # shape (3,)
    B_pos = np.array(B["position"], dtype=np.float64)

    # 3. 应用旋转矩阵：从相机坐标 → 世界坐标（gravity aligned）
    # 注意：点是行向量，右乘 R
    A_world = A_pos @ R  # shape (3,)
    B_world = B_pos @ R

    is_below = A_world[1] > B_world[1]

    response_template = random.choice(true_responses if is_below else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def front_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = front_true
    false_responses = front_false

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    is_front = A_min_z < B_min_z

    response_template = random.choice(true_responses if is_front else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def thin_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = thin_true_responses
    false_responses = thin_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    width_A = A["scale"][0]
    width_B = B["scale"][0]

    is_thinner = width_A < width_B

    response_template = random.choice(true_responses if is_thinner else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def short_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = short_true_responses
    false_responses = short_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    height_A = A["scale"][1]
    height_B = B["scale"][1]

    is_shorter = height_A < height_B

    response_template = random.choice(true_responses if is_shorter else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def small_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = small_true_responses
    false_responses = small_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    volume_A = np.prod(A["scale"])
    volume_B = np.prod(B["scale"])

    is_smaller = volume_A < volume_B

    response_template = random.choice(true_responses if is_smaller else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def point_close_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = point_close_true_responses
    false_responses = point_close_false_responses

    A_rle = A["rle"]
    B_rle = B["rle"]

    A_mask = rle_2_mask(A_rle)
    B_mask = rle_2_mask(B_rle)
    image_depth = imageio.v2.imread(wide_depth_path).astype(np.float32) / 1000.0  # 毫米转米

    A_point_yx = get_random_point(A_mask)
    B_point_yx = get_random_point(B_mask)

    if A_point_yx is None or B_point_yx is None:
        print("No points found in masks for A and B.")
        return None, None

    A_depth = image_depth[A_point_yx[0] // 2, A_point_yx[1] // 2]
    B_depth = image_depth[B_point_yx[0] // 2, B_point_yx[1] // 2]

    img_shape = A_rle["size"]
    A_coord_str = f"({A_point_yx[1]/img_shape[1]:.3f}, {A_point_yx[0]/img_shape[0]:.3f})"
    B_coord_str = f"({B_point_yx[1]/img_shape[1]:.3f}, {B_point_yx[0]/img_shape[0]:.3f})"

    is_closer = A_depth < B_depth

    response_template = random.choice(true_responses if is_closer else false_responses)
    answer = response_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)

    return answer, f"point {A_coord_str}", f"point {A_coord_str}", f"point {B_coord_str}", f"point {B_coord_str}" , "", ""

def obj_depth_data(A, B, C, gt_depth_path, wide_depth_path):
    template_answers = obj_depth_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    A_pcd = A["pointcloud"]
    A_points = np.array(A_pcd["points"])

    # 提取z坐标列（基于numpy的向量化操作[1,6](@ref)）
    z_coords = A_points[:, 2]

    # 获取最小z值及其索引（优化算法[7](@ref)）
    min_z = np.min(z_coords)  # 性能优于纯Python循环
    human_readable_depth = human_like_distance(min_z)

    answer_template = random.choice(template_answers)

    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", human_readable_depth)

    return answer, A_desc, A_dense, "", "", "", ""

def point_depth_data(A, B, C, gt_depth_path, wide_depth_path):
    template_answers = point_depth_answers

    A_rle = A["rle"]

    image_depth = imageio.v2.imread(wide_depth_path).astype(np.float32) / 1000.0  # 毫米转米

    A_mask = rle_2_mask(A_rle)
    A_point_yx = get_random_point(A_mask)

    if A_point_yx is None:
        return None

    A_depth = image_depth[A_point_yx[0] // 2, A_point_yx[1] // 2]

    human_readable_depth = human_like_distance(A_depth)

    img_shape = A_rle["size"]

    # 构建坐标描述符
    A_coord_str = f"({A_point_yx[1]/img_shape[1]:.3f}, {A_point_yx[0]/img_shape[0]:.3f})"

    answer_template = random.choice(template_answers)

    answer = answer_template.replace("[A]", A_coord_str).replace("[X]", human_readable_depth)

    return answer, f"point {A_coord_str}", f"point {A_coord_str}", "", "", "", ""

def fine_grain_object_2_point(A, B, C, gt_depth_path, wide_depth_path):
    template_answers = fine_grain_object_2_point_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    A_rle = A["rle"]
    A_mask = rle_2_mask(A_rle)  # shape: (h, w), value: True/False
    
    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(A_mask, connectivity=1)
    props = regionprops(labeled_mask)
    largest_region = max(props, key=lambda x: x.area)
    largest_label = largest_region.label
    largest_mask = (labeled_mask == largest_label)  # 取出最大连通区域
    # ======================================================

    # 计算最大连通区域的质心
    centroid = np.round(largest_region.centroid).astype(int)  # (row, col) 格式
    centroid_row, centroid_col = centroid

    # 检查质心是否在 largest_mask 内
    if largest_mask[centroid_row, centroid_col]:
        selected_coord = centroid  # 直接使用质心
    else:
        # 如果质心不在区域内，寻找最近的有效坐标
        coords = np.column_stack(np.where(largest_mask > 0))  # 获取所有 True 坐标
        tree = cKDTree(coords)  # 生成 k-d 树
        _, nearest_idx = tree.query(centroid)  # 找到最近的点
        selected_coord = coords[nearest_idx]
    

    img_shape = A_rle["size"]
    A_coord_str = f"({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})"
    answer_template = random.choice(template_answers)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", A_coord_str)

    return answer, A_desc, A_dense, "", "", "", ""

def point_2_fine_grain_object(A, B, C, gt_depth_path, wide_depth_path):
    template_answers = point_2_caption_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    A_rle = A["rle"]
    A_mask = rle_2_mask(A_rle)  # shape: (h, w), value: True/False

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(A_mask, connectivity=1)
    props = regionprops(labeled_mask)
    largest_region = max(props, key=lambda x: x.area)
    largest_label = largest_region.label
    largest_mask = (labeled_mask == largest_label)  # 取出最大连通区域
    # ======================================================

    # 计算最大连通区域的质心
    centroid = np.round(largest_region.centroid).astype(int)  # (row, col) 格式
    centroid_row, centroid_col = centroid

    # 检查质心是否在 largest_mask 内
    if largest_mask[centroid_row, centroid_col]:
        selected_coord = centroid  # 直接使用质心
    else:
        # 如果质心不在区域内，寻找最近的有效坐标
        coords = np.column_stack(np.where(largest_mask > 0))  # 获取所有 True 坐标
        tree = cKDTree(coords)  # 生成 k-d 树
        _, nearest_idx = tree.query(centroid)  # 找到最近的点
        selected_coord = coords[nearest_idx]

    img_shape = A_rle["size"]
    A_coord_str = f"({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})" # (x, y)

    answer_template = random.choice(template_answers)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", A_coord_str)

    return answer, f"point {A_coord_str}", f"point {A_coord_str}", "", "", "", ""

def distance(A, B, C, gt_depth_path, wide_depth_path):
    template_answers = distance_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pcd_data = A["pointcloud"]
    B_pcd_data = B["pointcloud"]

    # 将 points 和 color 转换为 Open3D PointCloud
    A_o3d_pcd = o3d.geometry.PointCloud()
    A_o3d_pcd.points = o3d.utility.Vector3dVector(A_pcd_data["points"])
    A_o3d_pcd.colors = o3d.utility.Vector3dVector(A_pcd_data["color"])
    
    B_o3d_pcd = o3d.geometry.PointCloud()
    B_o3d_pcd.points = o3d.utility.Vector3dVector(B_pcd_data["points"])
    B_o3d_pcd.colors = o3d.utility.Vector3dVector(B_pcd_data["color"])

    # 计算距离
    distance = calculate_distances_between_point_clouds(A_o3d_pcd, B_o3d_pcd)

    answer_template = random.choice(template_answers)

    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)
    answer = answer.replace("[X]", distance)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def object_width_data(A, B, C, gt_depth_path, wide_depth_path):
    template_answers = width_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    width_A = A["scale"][0]

    human_readable_width = human_like_distance(width_A)
    answer_template = random.choice(template_answers)

    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", human_readable_width)

    return answer, A_desc, A_dense, "", "", "", ""

def object_height_data(A, B, C, gt_depth_path, wide_depth_path):
    template_answers = height_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    height_A = A["scale"][1]

    human_readable_height = human_like_distance(height_A)
    answer_template = random.choice(template_answers)

    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", human_readable_height)

    return answer, A_desc, A_dense, "", "", "", ""

def contain_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = contain_true_responses
    false_responses = contain_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pos = A["position"]
    A_scale = A["scale"]
    A_R = A["R"]
    A_corners = A["corners"]

    B_pos = B["position"]
    B_scale = B["scale"]
    B_R = B["R"]
    B_corners = B["corners"]

    # Step 1: 从 B 的单位立方体中采样点，并变换到世界坐标
    sample_pts_local = sample_points_in_unit_bbox(n=1000)
    B_sample_pts_world = transform_points(sample_pts_local, B_scale, B_R, B_pos)

    # Step 2: 把这些点变换到 A 的局部坐标系
    B_pts_in_A_local = inverse_transform_points(B_sample_pts_world, A_scale, A_R, A_pos)

    # Step 3: 判断这些点是否在 A 的单位立方体中
    inside_flags = np.all(np.abs(B_pts_in_A_local) <= 0.5, axis=1)
    inside_ratio = np.sum(inside_flags) / len(inside_flags)

    is_contain = inside_ratio > 0.3  # 超过30%则认为包含

    if is_contain:
        answer = random.choice(true_responses)
    else:
        answer = random.choice(false_responses)
    
    answer = smart_insert(A_desc, A_dense, "[A]", answer)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def is_facing_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = is_facing_true_responses
    false_responses = is_facing_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pos = np.array(A["position"])
    A_R = np.array(A["R"])
    A_front = normalize(A_R[:, 0])
    A_corners = np.array(A["corners"])
    B_corners = np.array(B["corners"])

    # 选出正面四角点
    scores = [np.dot(normalize(c - A_pos), A_front) for c in A_corners]
    sorted_indices = np.argsort(scores)[-4:]
    front_points = A_corners[sorted_indices]
    front_points = sort_points_cw(front_points, normal=A_front)

    P, F, t = find_point_with_angle_math(A_pos, A_front, front_points)

    B_center = np.array(B["position"])
    in_view_cone  = is_point_in_view_cone(B_center, P, front_points)

    # 判断 ray 是否穿过 B 的 OBB
    intersects_ray = ray_intersects_obb(A_pos, A_front, B_corners)
    
    is_face = in_view_cone or intersects_ray

    if is_face:
        answer = random.choice(true_responses)
    else:
        answer = random.choice(false_responses)
    
    answer = smart_insert(A_desc, A_dense, "[A]", answer)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def is_facing_away_predicate(A, B, C, gt_depth_path, wide_depth_path):
    true_responses = is_facing_away_from_true_responses
    false_responses = is_facing_away_from_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pos = np.array(A["position"])
    A_R = np.array(A["R"])
    A_back = normalize(-A_R[:, 0])
    A_corners = np.array(A["corners"])
    B_corners = np.array(B["corners"])

    # 选出背面四角点
    scores = [np.dot(normalize(c - A_pos), A_back) for c in A_corners]
    sorted_indices = np.argsort(scores)[-4:]
    back_points = A_corners[sorted_indices]
    back_points = sort_points_cw(back_points, normal=A_back)

    P, F, t = find_point_with_angle_math(A_pos, A_back, back_points)

    B_center = np.array(B["position"])
    in_view_cone  = is_point_in_view_cone(B_center, P, back_points)

    # 判断 ray 是否穿过 B 的 OBB
    intersects_ray = ray_intersects_obb(A_pos, A_back, B_corners)

    is_back = in_view_cone or intersects_ray

    if is_back:
        answer = random.choice(true_responses)
    else:
        answer = random.choice(false_responses)

    answer = smart_insert(A_desc, A_dense, "[A]", answer)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def angle_of_obj(A ,B, C, gt_depth_path, wide_depth_path):
    template_answers = angle_of_object_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()  

    R_a = np.array(A['R'])
    R_b = np.array(B['R'])
    front_a = normalize(R_a[:, 0])  # 假设正面是 X 轴
    front_b = normalize(R_b[:, 0])

    angle_of_degrees = angle_between_vectors(front_a, front_b)

    answer = random.choice(template_answers)

    answer = smart_insert(A_desc, A_dense, "[A]", answer)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)
    answer = answer.replace("[X]", str(angle_of_degrees))

    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def touch_predicate(A ,B, C, gt_depth_path, wide_depth_path):
    true_responses = touch_true_responses
    false_responses = touch_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pcd_data = A["pointcloud"]
    B_pcd_data = B["pointcloud"]

    # 将 points 和 color 转换为 Open3D PointCloud
    A_o3d_pcd = o3d.geometry.PointCloud()
    A_o3d_pcd.points = o3d.utility.Vector3dVector(A_pcd_data["points"])
    A_o3d_pcd.colors = o3d.utility.Vector3dVector(A_pcd_data["color"])
    
    B_o3d_pcd = o3d.geometry.PointCloud()
    B_o3d_pcd.points = o3d.utility.Vector3dVector(B_pcd_data["points"])
    B_o3d_pcd.colors = o3d.utility.Vector3dVector(B_pcd_data["color"])

    # 计算距离
    distance = calculate_distances_between_point_clouds(A_o3d_pcd, B_o3d_pcd, human_readable=False)

    if distance < 0.1:
        is_touching = True
    else:
        is_touching = False
    response_template = random.choice(true_responses if is_touching else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)
    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def far_from_predicate(A ,B, C, gt_depth_path, wide_depth_path):
    true_responses = far_from_true_responses
    false_responses = far_from_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pcd_data = A["pointcloud"]
    B_pcd_data = B["pointcloud"]

    # 将 points 和 color 转换为 Open3D PointCloud
    A_o3d_pcd = o3d.geometry.PointCloud()
    A_o3d_pcd.points = o3d.utility.Vector3dVector(A_pcd_data["points"])
    A_o3d_pcd.colors = o3d.utility.Vector3dVector(A_pcd_data["color"])
    
    B_o3d_pcd = o3d.geometry.PointCloud()
    B_o3d_pcd.points = o3d.utility.Vector3dVector(B_pcd_data["points"])
    B_o3d_pcd.colors = o3d.utility.Vector3dVector(B_pcd_data["color"])

    # 计算距离
    distance = calculate_distances_between_point_clouds(A_o3d_pcd, B_o3d_pcd, human_readable=False)

    if distance > 1:
        is_far_from = True
    else:
        is_far_from = False

    response_template = random.choice(true_responses if is_far_from else false_responses)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)
    
    return answer, A_desc, A_dense, B_desc, B_dense, "", ""

def close_to_anchor(A ,B, C, gt_depth_path, wide_depth_path):
    template_answers = close_anchor_answers

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    C_desc = random.choice(C["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    C_dense = C.get("dense_caption", C_desc).lower()

    A_pcd_data = A["pointcloud"]
    B_pcd_data = B["pointcloud"]
    C_pcd_data = C["pointcloud"]

    # 将 points 和 color 转换为 Open3D PointCloud
    A_o3d_pcd = o3d.geometry.PointCloud()
    A_o3d_pcd.points = o3d.utility.Vector3dVector(A_pcd_data["points"])
    A_o3d_pcd.colors = o3d.utility.Vector3dVector(A_pcd_data["color"])
    
    B_o3d_pcd = o3d.geometry.PointCloud()
    B_o3d_pcd.points = o3d.utility.Vector3dVector(B_pcd_data["points"])
    B_o3d_pcd.colors = o3d.utility.Vector3dVector(B_pcd_data["color"])

    C_o3d_pcd = o3d.geometry.PointCloud()
    C_o3d_pcd.points = o3d.utility.Vector3dVector(C_pcd_data["points"])
    C_o3d_pcd.colors = o3d.utility.Vector3dVector(C_pcd_data["color"])

    # 计算距离
    A_C_distance = calculate_distances_between_point_clouds(A_o3d_pcd, C_o3d_pcd, human_readable=False)
    B_C_distance = calculate_distances_between_point_clouds(B_o3d_pcd, C_o3d_pcd, human_readable=False)

    closer_obj_desc = A_desc if A_C_distance < B_C_distance else B_desc
    closer_obj_dense = A_dense if A_C_distance < B_C_distance else B_dense

    further_obj_desc = B_desc if A_C_distance < B_C_distance else A_desc
    further_obj_dense = B_dense if A_C_distance < B_C_distance else A_dense

    answer = random.choice(template_answers)

    answer = smart_insert(closer_obj_desc, closer_obj_dense, "[A]", answer)
    answer = smart_insert(further_obj_desc, further_obj_dense, "[B]", answer)
    answer = smart_insert(C_desc, C_dense, "[C]", answer)

    return answer, closer_obj_desc, closer_obj_dense, further_obj_desc, further_obj_dense, C_desc, C_dense

class FactGeneration:
    def evaluate_predicates_on_pairs(self, detections, gt_depth_path, wide_depth_path):

        results = []

        # ✅ 使用一个物体（A）的函数
        one_object_can = [
            obj_depth_data,
            point_depth_data,
            fine_grain_object_2_point,
            point_2_fine_grain_object,
            object_width_data,
            object_height_data
        ]

        # ✅ 使用两个物体（A 和 B）的函数
        two_object_can = [
            left_predicate,
            image_below_predicate,
            world_below_predicate,
            front_predicate,
            thin_predicate,
            short_predicate,
            small_predicate,
            point_close_predicate,
            contain_predicate,
            is_facing_predicate,
            is_facing_away_predicate,
            angle_of_obj,
            touch_predicate,
            far_from_predicate,
            distance
        ]

        # ✅ 使用三个物体（A, B, C）的函数
        three_object_can = [
            close_to_anchor
        ]

        # 无目标时，直接返回空列表
        if len(detections) == 0:
            return results
        
        # --------------------------
        # 处理单个物体的情况
        # --------------------------
        elif len(detections) == 1:
            # 获取所有单物体组合（只有一个）
            one_obj_all_combinations = list(permutations(range(len(detections)), 1))
            random.shuffle(one_obj_all_combinations)
            one_obj_selected_combinations = one_obj_all_combinations[:1]
            one_obj_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_obj_object_pairs:
                valid_prompt_variants = one_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 4)

                for prompt_func in selected_predicates_choices:
                    fact = prompt_func(A, '', '', gt_depth_path, wide_depth_path)
                    results.append((fact, A_index, '', '', prompt_func.__name__, 'one_object_fact'))

            return results

        # --------------------------
        # 处理两个物体的情况
        # --------------------------
        elif len(detections) == 2:
            # 一元谓词：对每个物体各选一次
            one_obj_all_combinations = list(permutations(range(len(detections)), 1))
            random.shuffle(one_obj_all_combinations)
            one_obj_selected_combinations = one_obj_all_combinations[:2]
            one_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_object_pairs:
                valid_prompt_variants = one_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 3)

                for prompt_func in selected_predicates_choices:
                    fact = prompt_func(A, '', '', gt_depth_path, wide_depth_path)
                    results.append((fact, A_index, '', '', prompt_func.__name__, 'one_object_fact'))

            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:2]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = two_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 8)

                for prompt_func in selected_predicates_choices:
                    fact = prompt_func(A, B, '', gt_depth_path, wide_depth_path)
                    results.append((fact, A_index, B_index, '', prompt_func.__name__, 'two_object_fact'))

            return results
        # --------------------------
        # 处理三个或大于三个物体的情况
        # --------------------------        
        elif len(detections) >= 3:
            # 一元谓词：对每个物体各选一次
            one_obj_all_combinations = list(combinations(range(len(detections)), 1))
            random.shuffle(one_obj_all_combinations)
            one_obj_selected_combinations = one_obj_all_combinations[:6]
            one_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_object_pairs:
                valid_prompt_variants = one_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 1)

                for prompt_func in selected_predicates_choices:
                    fact = prompt_func(A, '', '', gt_depth_path, wide_depth_path)
                    results.append((fact, A_index, '', '', prompt_func.__name__, 'one_object_fact'))

            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:8]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = two_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 2)

                for prompt_func in selected_predicates_choices:
                    fact = prompt_func(A, B, '', gt_depth_path, wide_depth_path)
                    results.append((fact, A_index, B_index, '', prompt_func.__name__, 'two_object_fact'))

            # 三元谓词：从有序组合中选取
            three_obj_all_combinations = list(permutations(range(len(detections)), 3))
            random.shuffle(three_obj_all_combinations)
            three_obj_selected_combinations = three_obj_all_combinations[:3]
            three_object_pairs = [(detections[i], detections[j], detections[k], i, j, k) for i, j ,k in three_obj_selected_combinations]

            for A, B, C, A_index, B_index, C_index in three_object_pairs:
                valid_prompt_variants = three_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 1)

                for prompt_func in selected_predicates_choices:
                    fact = prompt_func(A, B, C, gt_depth_path, wide_depth_path)
                    results.append((fact, A_index, B_index, C_index, prompt_func.__name__, 'three_object_fact'))

            return results


