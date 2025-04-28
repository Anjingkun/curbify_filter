import random
from itertools import combinations
from itertools import permutations
import imageio
import numpy as np
from prompt_template import *
from prompt_utils import *
from skimage.measure import label, regionprops
from scipy.spatial import cKDTree
import open3d as o3d
import json

# Obj predicate -------------------------------------------------------------------------------
def left_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = left_predicate_questions
    true_responses = left_true_responses
    false_responses = left_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    is_left = A_pos[0] < B_pos[0]

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_left else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def right_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = right_predicate_questions
    true_responses = right_true_responses
    false_responses = right_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    is_right = A_pos[0] > B_pos[0]

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_right else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def image_above_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = image_above_predicate_questions
    true_responses = image_above_true_responses
    false_responses = image_above_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    is_above = A_pos[1] < B_pos[1]

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_above else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def image_below_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = image_below_predicate_questions
    true_responses = image_below_true_responses
    false_responses = image_below_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    is_below = A_pos[1] > B_pos[1]

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_below else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer


def world_above_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = world_above_predicate_questions
    true_responses = world_above_true_responses
    false_responses = world_above_false_responses

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

    # 4. 判断谁在上（Y 越小表示越高）
    is_above = A_world[1] < B_world[1]

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_above else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def world_below_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = world_below_predicate_questions
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

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_below else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def front_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = front_predicate_questions
    true_responses = front_true_responses
    false_responses = front_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    is_front = A_min_z < B_min_z

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_front else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def behind_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = behind_predicate_questions
    true_responses = behind_true_responses
    false_responses = behind_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    is_behind = A_min_z > B_min_z

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_behind else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def wide_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = wide_predicate_questions
    true_responses = wide_true_responses
    false_responses = wide_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    width_A = A["scale"][0]
    width_B = B["scale"][0]

    is_wider = width_A > width_B

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_wider else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def thin_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = thin_predicate_questions
    true_responses = thin_true_responses
    false_responses = thin_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    width_A = A["scale"][0]
    width_B = B["scale"][0]

    is_thinner = width_A < width_B

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_thinner else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def tall_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = tall_predicate_questions
    true_responses = tall_true_responses
    false_responses = tall_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    height_A = A["scale"][1]
    height_B = B["scale"][1]

    is_taller = height_A > height_B

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_taller else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def short_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = short_predicate_questions
    true_responses = short_true_responses
    false_responses = short_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    height_A = A["scale"][1]
    height_B = B["scale"][1]

    is_shorter = height_A < height_B

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_shorter else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def big_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = big_predicate_questions
    true_responses = big_true_responses
    false_responses = big_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    volume_A = np.prod(A["scale"])
    volume_B = np.prod(B["scale"])

    is_bigger = volume_A > volume_B

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_bigger else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def small_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = small_predicate_questions
    true_responses = small_true_responses
    false_responses = small_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    volume_A = np.prod(A["scale"])
    volume_B = np.prod(B["scale"])

    is_smaller = volume_A < volume_B

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_smaller else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def touch_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = touch_predicate_questions
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

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_touching else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def far_from_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = far_from_predicate_questions
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

    if distance > 1.0:
        is_far = True
    else:
        is_far = False

    question_template = random.choice(template_questions)
    response_template = random.choice(true_responses if is_far else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def contain_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    # A 包含 B，B在A里面
    template_questions = contain_predicate_questions
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

    # Step 4: 构造 QA
    question_template = random.choice(template_questions)
    answer_template = random.choice(true_responses if is_contain else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def outside_predicate(A, B, C, gt_depth_path, wide_depth_path, detections):
    # A 在 B 外面
    template_questions = outside_predicate_questions
    true_responses = outside_true_responses
    false_responses = outside_false_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pos = np.array(A["position"])
    A_scale = np.array(A["scale"])
    A_R = np.array(A["R"])

    B_pos = np.array(B["position"])
    B_scale = np.array(B["scale"])
    B_R = np.array(B["R"])

    # Step 1: 从 A 的单位立方体中采样点
    sample_pts_local = sample_points_in_unit_bbox(n=1000)

    # Step 2: 将 A 的采样点变换为世界坐标
    A_sample_pts_world = transform_points(sample_pts_local, A_scale, A_R, A_pos)

    # Step 3: 将这些点变换到 B 的局部坐标系
    A_pts_in_B_local = inverse_transform_points(A_sample_pts_world, B_scale, B_R, B_pos)

    # Step 4: 判断这些点是否在 B 的单位立方体外
    outside_flags = np.any(np.abs(A_pts_in_B_local) > 0.5, axis=1)
    outside_ratio = np.sum(outside_flags) / len(outside_flags)

    is_outside = outside_ratio > 0.7  # 超过70%的点不在 B 内部

    # Step 5: 构造问答
    question_template = random.choice(template_questions)
    answer_template = random.choice(true_responses if is_outside else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer
# Obj choice 

def left_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = left_choice_questions
    template_responses = left_choice_responses
        
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    more_left_desc  = A_desc if A_pos[0] < B_pos[0] else B_desc
    more_left_dense = A_dense if A_pos[0] < B_pos[0] else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)
    
    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    # 插入 more_left 到 answer
    answer = smart_insert(more_left_desc, more_left_dense, "[X]", answer_template)

    return question, answer

def right_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = right_choice_questions
    template_responses = right_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    more_right_desc = A_desc if A_pos[0] > B_pos[0] else B_desc
    more_right_dense = A_dense if A_pos[0] > B_pos[0] else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(more_right_desc, more_right_dense, "[X]", answer_template)

    return question, answer

def image_above_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = image_above_choice_questions
    template_responses = image_above_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    more_above_desc = A_desc if A_pos[1] < B_pos[1] else B_desc
    more_above_dense = A_dense if A_pos[1] < B_pos[1] else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(more_above_desc, more_above_dense, "[X]", answer_template)

    return question, answer

def image_below_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = image_below_choice_questions
    template_responses = image_below_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_pos = A["position"]
    B_pos = B["position"]

    more_below_desc = A_desc if A_pos[1] > B_pos[1] else B_desc
    more_below_dense = A_dense if A_pos[1] > B_pos[1] else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(more_below_desc, more_below_dense, "[X]", answer_template)

    return question, answer

def world_above_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = world_above_choice_questions
    template_responses = world_above_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    
    # 1. 读取旋转矩阵（gravity 对齐矩阵）
    T_gravity_path = wide_depth_path.replace("depth.png", "T_gravity.json")
    with open(T_gravity_path, "r") as f:
        R = json.load(f)
    R = np.array(R, dtype=np.float64)

    # ✅ 注意：R 是 camera → world，对行向量直接右乘 R
    A_pos = np.array(A["position"], dtype=np.float64)
    B_pos = np.array(B["position"], dtype=np.float64)

    A_world = A_pos @ R
    B_world = B_pos @ R

    more_above_desc = A_desc if A_world[1] < B_world[1] else B_desc
    more_above_dense = A_dense if A_world[1] < B_world[1] else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(more_above_desc, more_above_dense, "[X]", answer_template)

    return question, answer

def world_below_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = world_below_choice_questions
    template_responses = world_below_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    # 1. 读取旋转矩阵（gravity 对齐矩阵）
    T_gravity_path = wide_depth_path.replace("depth.png", "T_gravity.json")
    with open(T_gravity_path, "r") as f:
        R = json.load(f)
    R = np.array(R, dtype=np.float64)

    # ✅ 注意：R 是 camera → world，对行向量直接右乘 R
    A_pos = np.array(A["position"], dtype=np.float64)
    B_pos = np.array(B["position"], dtype=np.float64)

    A_world = A_pos @ R
    B_world = B_pos @ R

    more_below_desc = A_desc if A_world[1] > B_world[1] else B_desc
    more_below_dense = A_dense if A_world[1] > B_world[1] else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(more_below_desc, more_below_dense, "[X]", answer_template)

    return question, answer

def front_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = front_choice_questions
    template_responses = front_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    more_front_desc = A_desc if A_min_z < B_min_z else B_desc
    more_front_dense = A_dense if A_min_z < B_min_z else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(more_front_desc, more_front_dense, "[X]", answer_template)

    return question, answer

def behind_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = behind_choice_questions
    template_responses = behind_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    more_behind_desc = A_desc if A_min_z > B_min_z else B_desc
    more_behind_dense = A_dense if A_min_z > B_min_z else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(more_behind_desc, more_behind_dense, "[X]", answer_template)

    return question, answer

def wide_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = wide_choice_questions
    template_responses = wide_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    width_A = A["scale"][0]
    width_B = B["scale"][0]

    wider_desc = A_desc if width_A > width_B else B_desc
    wider_dense = A_dense if width_A > width_B else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(wider_desc, wider_dense, "[X]", answer_template)

    return question, answer

def thin_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = thin_choice_questions
    template_responses = thin_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    width_A = A["scale"][0]
    width_B = B["scale"][0]

    thinner_desc = A_desc if width_A < width_B else B_desc
    thinner_dense = A_dense if width_A < width_B else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(thinner_desc, thinner_dense, "[X]", answer_template)

    return question, answer

def tall_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = tall_choice_questions
    template_responses = tall_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    height_A = A["scale"][1]
    height_B = B["scale"][1]

    taller_desc = A_desc if height_A > height_B else B_desc
    taller_dense = A_dense if height_A > height_B else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(taller_desc, taller_dense, "[X]", answer_template)

    return question, answer

def short_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = short_choice_questions
    template_responses = short_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    height_A = A["scale"][1]
    height_B = B["scale"][1]

    shorter_desc = A_desc if height_A < height_B else B_desc
    shorter_dense = A_dense if height_A < height_B else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(shorter_desc, shorter_dense, "[X]", answer_template)

    return question, answer

def big_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = big_choice_questions
    template_responses = big_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    volume_A = np.prod(A["scale"])
    volume_B = np.prod(B["scale"])

    bigger_desc = A_desc if volume_A > volume_B else B_desc
    bigger_dense = A_dense if volume_A > volume_B else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(bigger_desc, bigger_dense, "[X]", answer_template)

    return question, answer

def small_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = small_choice_questions
    template_responses = small_choice_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()
    volume_A = np.prod(A["scale"])
    volume_B = np.prod(B["scale"])

    smaller_desc = A_desc if volume_A < volume_B else B_desc
    smaller_dense = A_dense if volume_A < volume_B else B_dense

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(smaller_desc, smaller_dense, "[X]", answer_template)

    return question, answer

# point predection ------------------------------------------------

def point_close_prediction(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = point_close_predicate_questions
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

    question_template = random.choice(template_questions)
    answer_template = random.choice(true_responses if is_closer else false_responses)

    question = question_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)
    answer = answer_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)

    return question, answer

def point_far_prediction(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = point_far_predicate_questions
    true_responses = point_far_true_responses
    false_responses = point_far_false_responses

    A_rle = A["rle"]
    B_rle = B["rle"]
    A_mask = rle_2_mask(A_rle)
    B_mask = rle_2_mask(B_rle)
    image_depth = imageio.v2.imread(wide_depth_path).astype(np.float32) / 1000.0  # 毫米转米

    A_point_yx = get_random_point(A_mask)
    B_point_yx = get_random_point(B_mask)

    if A_point_yx is None or B_point_yx is None:
        return None, None

    A_depth = image_depth[A_point_yx[0] // 2, A_point_yx[1] // 2]
    B_depth = image_depth[B_point_yx[0] // 2, B_point_yx[1] // 2]

    img_shape = A_rle["size"]
    A_coord_str = f"({A_point_yx[1]/img_shape[1]:.3f}, {A_point_yx[0]/img_shape[0]:.3f})"
    B_coord_str = f"({B_point_yx[1]/img_shape[1]:.3f}, {B_point_yx[0]/img_shape[0]:.3f})"

    is_farther = A_depth > B_depth

    question_template = random.choice(template_questions)
    answer_template = random.choice(true_responses if is_farther else false_responses)

    question = question_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)
    answer = answer_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)

    return question, answer

# point choice ------------------------------------------------

def point_close_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = point_close_choice_questions
    template_responses = point_close_choice_responses

    A_rle = A["rle"]
    B_rle = B["rle"]
    A_mask = rle_2_mask(A_rle)
    B_mask = rle_2_mask(B_rle)
    image_depth = imageio.v2.imread(wide_depth_path).astype(np.float32) / 1000.0  # 毫米转米

    A_point_yx = get_random_point(A_mask)
    B_point_yx = get_random_point(B_mask)

    if A_point_yx is None or B_point_yx is None:
        return None, None

    A_depth = image_depth[A_point_yx[0] // 2, A_point_yx[1] // 2]
    B_depth = image_depth[B_point_yx[0] // 2, B_point_yx[1] // 2]

    img_shape = A_rle["size"]
    A_coord_str = f"({A_point_yx[1]/img_shape[1]:.3f}, {A_point_yx[0]/img_shape[0]:.3f})"
    B_coord_str = f"({B_point_yx[1]/img_shape[1]:.3f}, {B_point_yx[0]/img_shape[0]:.3f})"

    closer_coord = A_coord_str if A_depth < B_depth else B_coord_str

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = question_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)
    answer = answer_template.replace("[X]", closer_coord)

    return question, answer

def point_far_choice(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = point_far_choice_questions
    template_responses = point_far_choice_responses

    A_rle = A["rle"]
    B_rle = B["rle"]
    A_mask = rle_2_mask(A_rle)
    B_mask = rle_2_mask(B_rle)
    image_depth = imageio.v2.imread(wide_depth_path).astype(np.float32) / 1000.0  # 毫米转米

    A_point_yx = get_random_point(A_mask)
    B_point_yx = get_random_point(B_mask)

    if A_point_yx is None or B_point_yx is None:
        return None, None

    A_depth = image_depth[A_point_yx[0] // 2, A_point_yx[1] // 2]
    B_depth = image_depth[B_point_yx[0] // 2, B_point_yx[1] // 2]

    img_shape = A_rle["size"]
    A_coord_str = f"({A_point_yx[1]/img_shape[1]:.3f}, {A_point_yx[0]/img_shape[0]:.3f})"
    B_coord_str = f"({B_point_yx[1]/img_shape[1]:.3f}, {B_point_yx[0]/img_shape[0]:.3f})"

    farther_coord = A_coord_str if A_depth > B_depth else B_coord_str

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = question_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)
    answer = answer_template.replace("[X]", farther_coord)

    return question, answer

# depth
def obj_depth_data(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = obj_depth_questions
    template_responses = obj_depth_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    A_pcd = A["pointcloud"]
    A_points = np.array(A_pcd["points"])

    # 提取z坐标列（基于numpy的向量化操作[1,6](@ref)）
    z_coords = A_points[:, 2]

    # 获取最小z值及其索引（优化算法[7](@ref)）
    min_z = np.min(z_coords)  # 性能优于纯Python循环
    human_readable_depth = human_like_distance(min_z)

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", human_readable_depth)

    return question, answer

def point_depth_data(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = point_depth_questions
    template_responses = point_depth_responses

    A_rle = A["rle"]

    image_depth = imageio.v2.imread(wide_depth_path).astype(np.float32) / 1000.0  # 毫米转米

    A_mask = rle_2_mask(A_rle)
    A_point_yx = get_random_point(A_mask)

    if A_point_yx is None:
        return None

    A_depth = image_depth[A_point_yx[0] // 2, A_point_yx[1] // 2]

    human_readable_depth = human_like_distance(A_depth)

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    img_shape = A_rle["size"]

    # 构建坐标描述符
    A_coord_str = f"({A_point_yx[1]/img_shape[1]:.3f}, {A_point_yx[0]/img_shape[0]:.3f})"

    question = question_template.replace("[A]", A_coord_str)
    answer = answer_template.replace("[A]", A_coord_str).replace("[X]", human_readable_depth)

    return question, answer


# obj 2 point -----------------------------------------------------------------------

def fine_grain_object_2_point(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = fine_grain_object_2_point_questions
    template_responses = fine_grain_object_2_point_responses

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
    A_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", A_coord_str)

    return question, answer

# point 2 obj --------------------------------------

def point_2_fine_grain_object(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = point_2_caption_questions
    template_responses = point_2_caption_responses

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

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = question_template.replace("[X]", A_coord_str)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", A_coord_str)

    return question, answer

# distence -----------------------------------

def object_distence_data(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = distance_questions
    template_responses = distance_responses

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

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)
    answer = answer.replace("[X]", distance)

    return question, answer

def object_width_data(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = width_questions
    template_responses = width_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    width_A = A["scale"][0]

    human_readable_width = human_like_distance(width_A)

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", human_readable_width)

    return question, answer

def object_height_data(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = height_questions
    template_responses = height_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    height_A = A["scale"][1]

    human_readable_height = human_like_distance(height_A)

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[X]", human_readable_height)

    return question, answer

# face ----------------------------------------------------------------
def how_horizontal_face_object(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = how_horizontal_face_object_questions
    template_responses = how_horizontal_face_object_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    A_pos = np.array(A["position"])

    # 4. 计算角度
    horizontal_angle_deg = np.degrees(np.arctan2(A_pos[0], A_pos[2]))
    if horizontal_angle_deg > 0:
        horizontal_rotate = "right"
    else:
        horizontal_rotate = "left"

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[R]", horizontal_rotate)
    answer = answer.replace("[X]", f"{abs(horizontal_angle_deg):.3f}")

    return question, answer


def how_vertical_face_object(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = how_vertical_face_object_questions
    template_responses = how_vertical_face_object_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    A_pos = np.array(A["position"])

    # 4. 计算角度
    vertical_angle_deg = np.degrees(np.arctan2(A_pos[1], A_pos[2]))
    if vertical_angle_deg > 0:
        vertical_rotate = "down"
    else:
        vertical_rotate = "up"

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = answer.replace("[R]", vertical_rotate)
    answer = answer.replace("[X]", f"{abs(vertical_angle_deg):.3f}")

    return question, answer


def is_facing_object(A, B, C, gt_depth_path, wide_depth_path, detections):
    # A正对B
    template_questions = facing_object_questions
    true_responses = facing_object_true_responses
    false_responses = facing_object_false_responses

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

    question_template = random.choice(template_questions)
    answer_template = random.choice(true_responses if is_face else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

# face away from 背对 ----------------------------------------------------------------
def is_facing_away_from_object(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = facing_away_object_questions
    true_responses = facing_away_object_true_responses
    false_responses = facing_away_object_false_responses

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

    question_template = random.choice(template_questions)
    answer_template = random.choice(true_responses if is_back else false_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer


# angle -----------------------------------------------------------------
def angle_of_objects(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = angle_of_objects_questions
    template_responses = angle_of_objects_responses

    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()  

    R_a = np.array(A['R'])
    R_b = np.array(B['R'])
    front_a = normalize(R_a[:, 0])  # 假设正面是 X 轴
    front_b = normalize(R_b[:, 0])

    angle_of_degrees = angle_between_vectors(front_a, front_b)
    
    # 处理角度值：如果是0则直接用"0"，否则保留三位有效数字
    angle_str = "0" if angle_of_degrees == 0 else f"{angle_of_degrees:.3g}"

    question_template = random.choice(template_questions)
    answer_template = random.choice(template_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", answer_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)
    answer = answer.replace("[X]", angle_str)

    return question, answer

# choice of relation

def choice_left_right(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = choice_left_right_questions
    left_responses = choice_left_responses
    right_responses = choice_right_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pos = A["position"]
    B_pos = B["position"]

    is_left =  A_pos[0] < B_pos[0]

    question_template = random.choice(template_questions)
    response_template = random.choice(left_responses if is_left else right_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def choice_front_behind(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = choice_front_behind_questions
    front_responses = choice_front_responses
    behind_responses = choice_behind_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    is_front =  A_min_z < B_min_z

    question_template = random.choice(template_questions)
    response_template = random.choice(front_responses if is_front else behind_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def image_choice_above_below(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = image_choice_above_below_questions
    above_responses = image_choice_above_responses
    below_responses = image_choice_below_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_pos = A["position"]
    B_pos = B["position"]

    is_above = A_pos[1] < B_pos[1]

    question_template = random.choice(template_questions)
    response_template = random.choice(above_responses if is_above else below_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def world_choice_above_below(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = world_choice_above_below_questions
    above_responses = world_choice_above_responses
    below_responses = world_choice_below_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    # 1. 读取旋转矩阵（gravity 对齐矩阵）
    T_gravity_path = wide_depth_path.replace("depth.png", "T_gravity.json")
    with open(T_gravity_path, "r") as f:
        R = json.load(f)
    R = np.array(R, dtype=np.float64)

    # ✅ 注意：R 是 camera → world，对行向量直接右乘 R
    A_pos = np.array(A["position"], dtype=np.float64)
    B_pos = np.array(B["position"], dtype=np.float64)

    A_world = A_pos @ R
    B_world = B_pos @ R

    is_above = A_world[1] < B_world[1]

    question_template = random.choice(template_questions)
    response_template = random.choice(above_responses if is_above else below_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def choice_wide_thin(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = choice_wide_thin_questions
    wide_responses = choice_wide_responses
    thin_responses = choice_thin_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_width = A["scale"][0]
    B_width = B["scale"][0]

    is_wide = A_width > B_width

    question_template = random.choice(template_questions)
    response_template = random.choice(wide_responses if is_wide else thin_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def choice_tall_short(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = choice_tall_short_questions
    tall_responses = choice_tall_responses
    short_responses = choice_short_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_height = A["scale"][1]
    B_height = B["scale"][1]

    is_tall = A_height > B_height

    question_template = random.choice(template_questions)
    response_template = random.choice(tall_responses if is_tall else short_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def choice_big_small(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = choice_big_small_questions
    big_responses = choice_big_responses
    small_responses = choice_small_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    volume_A = np.prod(A["scale"])
    volume_B = np.prod(B["scale"])

    is_big = volume_A > volume_B

    question_template = random.choice(template_questions)
    response_template = random.choice(big_responses if is_big else small_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer

def choice_inside_outside(A, B, C, gt_depth_path, wide_depth_path, detections):
    # A 在B的里面还是外面
    template_questions = choice_inside_outside_questions
    inside_responses = choice_inside_responses
    outside_responses = choice_outside_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    # 提取空间信息
    A_pos = np.array(A["position"])
    A_scale = np.array(A["scale"])
    A_R = np.array(A["R"])

    B_pos = np.array(B["position"])
    B_scale = np.array(B["scale"])
    B_R = np.array(B["R"])

    # Step 1: 从 A 的单位立方体中采样点，并变换到世界坐标系
    sample_pts_local = sample_points_in_unit_bbox(n=1000)
    A_pts_world = transform_points(sample_pts_local, A_scale, A_R, A_pos)

    # Step 2: 将 A 的点变换到 B 的局部坐标系中
    A_pts_in_B_local = inverse_transform_points(A_pts_world, B_scale, B_R, B_pos)

    # Step 3: 判断 A 的点有多少在 B 的单位立方体内
    inside_flags = np.all(np.abs(A_pts_in_B_local) <= 0.5, axis=1)
    inside_ratio = np.sum(inside_flags) / len(inside_flags)

    is_inside = inside_ratio >= 0.3

    question_template = random.choice(template_questions)
    response_template = random.choice(inside_responses if is_inside else outside_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    answer = smart_insert(A_desc, A_dense, "[A]", response_template)
    answer = smart_insert(B_desc, B_dense, "[B]", answer)

    return question, answer


def choice_point_close_far(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = choice_point_close_far_questions
    closer_responses = choice_point_close_responses
    farther_responses = choice_point_far_responses

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

    question_template = random.choice(template_questions)
    response_template = random.choice(closer_responses if is_closer else farther_responses)

    question = question_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)
    answer = response_template.replace("[A]", A_coord_str).replace("[B]", B_coord_str)

    return question, answer

# choice obj closer to achor
def close_anchor(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = close_anchor_questions
    tamplate_responses = close_anchor_responses

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

    question_template = random.choice(template_questions)
    response_template = random.choice(tamplate_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    question = smart_insert(C_desc, C_dense, "[C]", question)
    answer = smart_insert(closer_obj_desc, closer_obj_dense, "[X]", response_template)
    answer = smart_insert(C_desc, C_dense, "[C]", answer)

    return question, answer
# --------------------------------------------------------------------------------------------------------------
# choice obj closer to achor
def far_anchor(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = far_anchor_questions
    tamplate_responses = far_anchor_responses

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

    further_obj_desc = A_desc if A_C_distance > B_C_distance else B_desc
    further_obj_dense = A_dense if A_C_distance > B_C_distance else B_dense

    question_template = random.choice(template_questions)
    response_template = random.choice(tamplate_responses)

    question = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = smart_insert(B_desc, B_dense, "[B]", question)
    question = smart_insert(C_desc, C_dense, "[C]", question)
    answer = smart_insert(further_obj_desc, further_obj_dense, "[X]", response_template)
    answer = smart_insert(C_desc, C_dense, "[C]", answer)

    return question, answer

def find_one_anchor_left_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_left_templates  = find_one_anchor_left_obj_questions
    single_target_left_templates  = find_one_anchor_single_left_obj_questions
    template_responses = find_one_anchor_left_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_pos = A["position"]
    B_pos = B["position"]

    A_is_left = A_pos[0] < B_pos[0]

    if A_is_left:
        obj_range = find_anchor_left_obj_range(B, A, detections)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_left_obj_range(A, B, detections)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_left_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_left_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer
    
def find_one_anchor_right_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_right_templates  = find_one_anchor_right_obj_questions
    single_target_right_templates  = find_one_anchor_single_right_obj_questions
    template_responses = find_one_anchor_right_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_pos = A["position"]
    B_pos = B["position"]

    A_is_right = A_pos[0] > B_pos[0]

    if A_is_right:
        obj_range = find_anchor_right_obj_range(B, A, detections)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_right_obj_range(A, B, detections)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_right_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_right_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer

def find_one_anchor_image_above_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_image_above_templates  = find_one_anchor_image_above_obj_questions
    single_target_image_above_templates  = find_one_anchor_single_image_above_obj_questions
    template_responses = find_one_anchor_image_above_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_pos = A["position"]
    B_pos = B["position"]

    A_is_above = A_pos[1] < B_pos[1]

    if A_is_above:
        obj_range = find_anchor_image_above_obj_range(B, A, detections)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_image_above_obj_range(A, B, detections)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_image_above_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_image_above_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer

def find_one_anchor_image_below_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_image_below_templates  = find_one_anchor_image_below_obj_questions
    single_target_image_below_templates  = find_one_anchor_single_image_below_obj_questions
    template_responses = find_one_anchor_image_below_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_pos = A["position"]
    B_pos = B["position"]

    A_is_below = A_pos[1] > B_pos[1]

    if A_is_below:
        obj_range = find_anchor_image_below_obj_range(B, A, detections)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_image_below_obj_range(A, B, detections)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_image_below_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_image_below_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer

def find_one_anchor_world_above_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_world_above_templates  = find_one_anchor_world_above_obj_questions
    single_target_world_above_templates  = find_one_anchor_single_world_above_obj_questions
    template_responses = find_one_anchor_world_above_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

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

    A_is_above = A_world[1] < B_world[1]

    if A_is_above:
        obj_range = find_anchor_world_above_obj_range(B, A, detections, R)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_world_above_obj_range(A, B, detections, R)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_world_above_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_world_above_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer

def find_one_anchor_world_below_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_world_below_templates  = find_one_anchor_world_below_obj_questions
    single_target_world_below_templates  = find_one_anchor_single_world_below_obj_questions
    template_responses = find_one_anchor_world_below_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

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

    A_is_below = A_world[1] > B_world[1]

    if A_is_below:
        obj_range = find_anchor_world_below_obj_range(B, A, detections, R)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_world_below_obj_range(A, B, detections, R)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_world_below_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_world_below_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer

def find_one_anchor_front_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_front_templates  = find_one_anchor_front_obj_questions
    single_target_front_templates  = find_one_anchor_single_front_obj_questions
    template_responses = find_one_anchor_front_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    A_is_front = A_min_z < B_min_z

    if A_is_front:
        obj_range = find_anchor_front_obj_range(B, A, detections)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_front_obj_range(A, B, detections)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_front_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_front_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer

def find_one_anchor_behind_obj(A, B, C, gt_depth_path, wide_depth_path, detections):
    multi_target_behind_templates  = find_one_anchor_behind_obj_questions
    single_target_behind_templates  = find_one_anchor_single_behind_obj_questions
    template_responses = find_one_anchor_behind_obj_responses

    # 随机选择描述文本
    A_desc = random.choice(A["spatial_caption"]).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()

    A_dense = A.get("dense_caption", A_desc).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    A_is_behind = A_min_z > B_min_z

    if A_is_behind:
        obj_range = find_anchor_behind_obj_range(B, A, detections)
        anchor_desc = B_desc
        anchor_dense = B_dense
        target_label = A_label
        target_rle = A["rle"]
    else:
        obj_range = find_anchor_behind_obj_range(A, B, detections)
        anchor_desc = A_desc
        anchor_dense = A_dense
        target_label = B_label
        target_rle = B["rle"]
    
    # 锚点左边没有目标
    if obj_range is None:
        print("No objects detected.")
        return None, None
    
    # 构造问题
    if obj_range == 0:
        template = random.choice(single_target_behind_templates)
        question = template.replace("[class_name]", target_label)
    else:
        template = random.choice(multi_target_behind_templates)
        range_str = ordinal(obj_range)
        question = template.replace("[class_name]", target_label)\
                           .replace("[range]", range_str)
        
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question)

    answer = random.choice(template_responses)

    target_mask = rle_2_mask(target_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(target_mask, connectivity=1)
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
    
    img_shape = target_rle["size"]

    target_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"
    answer = random.choice(template_responses).replace("[X]", target_coord_str)

    return question, answer

def find_obj_between_anchor(e1, middle, e2, direction, gt_depth_path, wide_depth_path, detections):
    if direction == 'x':
        template_questions = find_obj_between_anchor_x_questions
    elif direction == 'y':
        template_questions = find_obj_between_anchor_y_questions
    else:
        template_questions = find_obj_between_anchor_z_questions
    template_responses = find_obj_between_anchor_responses
    e1_desc = random.choice(e1["spatial_caption"]).lower()
    e2_desc = random.choice(e2["spatial_caption"]).lower()
    e1_dense = e1.get("dense_caption", e1_desc).lower()
    e2_dense = e2.get("dense_caption", e2_desc).lower()
    middle_label = middle["class_name"]
    middle_rle = middle["rle"]

    middle_mask = rle_2_mask(middle_rle)

    # ============= 关键：先进行最大连通区域筛选 ================
    labeled_mask = label(middle_mask, connectivity=1)
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
    
    img_shape = middle_rle["size"]

    middle_coord_str = f"[({selected_coord[1]/img_shape[1]:.3f}, {selected_coord[0]/img_shape[0]:.3f})]"

    question = random.choice(template_questions)
    question = smart_insert(e1_desc, e1_dense, "[anchor_1]", question)
    question = smart_insert(e2_desc, e2_dense, "[anchor_2]", question)
    question = question.replace("[class_name]", middle_label)
    answer = random.choice(template_responses).replace("[X]", middle_coord_str)
    return question, answer

class PromptGenerator:
    def evaluate_predicates_on_pairs(self, detections, gt_depth_path, wide_depth_path):
        """
            根据输入的 detections 数量，分别应用一元、二元、三元谓词函数生成 QA。
            返回格式为一个 results 列表，包含 (qa_result, object_index_1, object_index_2, ..., func_name, qa_type)
        """
        results = []

        # 一元谓词函数列表（单个物体）
        one_object_can = [
            obj_depth_data,
            point_depth_data,
            fine_grain_object_2_point,
            point_2_fine_grain_object,
            object_width_data,
            object_height_data,
            # how_face_object,
        ]

        # 二元谓词函数列表（物体对之间的关系）
        two_object_can = {
            "left_right_predicate": [
                left_predicate, right_predicate, left_choice, right_choice, choice_left_right
            ],
            "obj_front_behind_predicate": [
                front_predicate, behind_predicate, front_choice, behind_choice, choice_front_behind
            ],
            "point_close_far_predicate": [
                point_close_prediction, point_far_prediction, point_close_choice, point_far_choice, choice_point_close_far
            ],
            "image_above_below_predicate": [
                image_above_predicate, image_below_predicate, image_above_choice, image_below_choice, image_choice_above_below
            ],
            "world_above_below_predicate": [
                world_above_predicate, world_below_predicate, world_above_choice, world_below_choice, world_choice_above_below
            ],
            "wide_thin": [
                wide_predicate, thin_predicate, wide_choice, thin_choice, choice_wide_thin
            ],
            "tall_short": [
                tall_predicate, short_predicate, tall_choice, short_choice, choice_tall_short
            ],
            "big_small":[
                big_predicate, small_predicate, big_choice, small_choice, choice_big_small
            ],
            "inside_outside": [
                contain_predicate, outside_predicate, choice_inside_outside
            ],
            "touch_far": [
                touch_predicate, far_from_predicate
            ],
            "facing": [
                is_facing_object, is_facing_away_from_object,
            ],
            "angle" : [
                angle_of_objects
            ],
            "distence": [
                object_distence_data
            ],
            "anchor" : [
                find_one_anchor_left_obj, find_one_anchor_right_obj,
                find_one_anchor_image_above_obj, find_one_anchor_image_below_obj, find_one_anchor_world_above_obj, find_one_anchor_world_below_obj,
                find_one_anchor_front_obj, find_one_anchor_behind_obj
            ]
        }

        # 三元谓词函数列表（涉及三个物体的空间关系）
        three_object_can = [
            close_anchor,
            far_anchor
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
                selected_predicates_choices = random.sample(valid_prompt_variants, 6)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, '', '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

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
                selected_predicates_choices = random.sample(valid_prompt_variants, 6)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, '', '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:2]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = two_object_can
                # 遍历每个类别，每类采样 1 个
                selected_predicates_choices = [
                    random.choice(func_list)
                    for func_list in valid_prompt_variants.values()
                    if len(func_list) > 0
                ]

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'two_object_qa'))

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
                selected_predicates_choices = random.sample(valid_prompt_variants, 2)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, '', '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:7]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = two_object_can
                # 从所有类别中随机选取 4 类
                all_categories = list(valid_prompt_variants.keys())
                random.shuffle(all_categories)
                selected_categories = all_categories[:4]
                # 每类中随机选一个函数
                for category in selected_categories:
                    func_list = valid_prompt_variants[category]
                    if not func_list:
                        continue  # 如果该类为空，跳过
                    prompt_func = random.choice(func_list)

                    qa = prompt_func(A, B, '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'two_object_qa'))

            # 三元谓词：从有序组合中选取
            three_obj_all_combinations = list(permutations(range(len(detections)), 3))
            random.shuffle(three_obj_all_combinations)
            three_obj_selected_combinations = three_obj_all_combinations[:8]
            three_object_pairs = [(detections[i], detections[j], detections[k], i, j, k) for i, j ,k in three_obj_selected_combinations]

            for A, B, C, A_index, B_index, C_index in three_object_pairs:
                valid_prompt_variants = three_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 1)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, C, gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, B_index, C_index, prompt_func.__name__, 'three_object_qa'))

            # 无序三元谓词，从无序组合中选取
            three_obj_all_combinations_for_multi_anchor = list(combinations(range(len(detections)), 3))
            random.shuffle(three_obj_all_combinations_for_multi_anchor)
            three_object_pairs_for_multi_anchor = [(detections[i], detections[j], detections[k], i, j, k) for i, j ,k in three_obj_all_combinations_for_multi_anchor]
            count = 0
            for A, B, C, A_index, B_index, C_index in three_object_pairs_for_multi_anchor:
                direction = find_max_variance_direction(A, B, C)
                sorted_objs = sort_objects_by_direction([A, B, C], direction)
                e1, middle, e2 = sorted_objs
                # 获取对应 index
                obj_to_index = {
                    id(A): A_index,
                    id(B): B_index,
                    id(C): C_index
                }
                e1_index     = obj_to_index[id(e1)]
                middle_index = obj_to_index[id(middle)]
                e2_index     = obj_to_index[id(e2)]
                if not check_ambiguity(middle, e1, e2, detections, direction):
                    qa = find_obj_between_anchor(e1, middle, e2, direction, gt_depth_path, wide_depth_path, detections)
                    results.append((qa, e1_index, middle_index, e2_index, 'find_obj_between_anchor', 'three_object_qa'))
                    count += 1
                    if count >= 4:
                        break
            return results