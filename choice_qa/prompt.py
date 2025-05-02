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
def left_predicate(A, B, C, gt_depth_path, wide_depth_path):
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
    
    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_left 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_left:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_left 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_left:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def right_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_right 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_right:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_right 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_right:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def image_above_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_above 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_above:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_above 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_above:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def image_below_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_below 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_below:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_below 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_below:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer


def world_above_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_above 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_above:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_above 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_above:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def world_below_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_below 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_below:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_below 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_below:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def front_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_front 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_front:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_front 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_front:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def behind_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_behind 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_behind:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_behind 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_behind:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def wide_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_wider 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_wider:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_wider 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_wider:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def thin_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_thinner 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_thinner:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_thinner 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_thinner:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def tall_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_taller 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_taller:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_taller 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_taller:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def short_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_shorter 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_shorter:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_shorter 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_shorter:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def big_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_bigger 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_bigger:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_bigger 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_bigger:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def small_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_smaller 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_smaller:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_behind 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_smaller:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def touch_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_touching 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_touching:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_touching 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_touching:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def far_from_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_far 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_far:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_far 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_far:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def contain_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_contain 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_contain:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_contain 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_contain:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def outside_predicate(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_outside 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_outside:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_outside 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_outside:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer


# face ----------------------------------------------------------------

def how_horizontal_face_object(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = how_horizontal_face_object_questions

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    A_pos = np.array(A["position"])

    # 计算水平旋转角度
    horizontal_angle_deg = np.degrees(np.arctan2(A_pos[0], A_pos[2]))
    if horizontal_angle_deg > 0:
        horizontal_rotate = "right"
    else:
        horizontal_rotate = "left"

    # 随机打乱 left/right 的顺序
    options = ["left", "right"]
    random.shuffle(options)

    # 生成选项字符串
    option_str = f"(A) {options[0]}, (B) {options[1]}"

    # 选择模板并替换
    question_template = random.choice(template_questions)
    question_filled = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = question_filled.replace("[option]", option_str)

    # 判断正确答案是哪个选项
    if options[0] == horizontal_rotate:
        answer = "(A)"
    else:
        answer = "(B)"

    return question, answer

def how_vertical_face_object(A, B, C, gt_depth_path, wide_depth_path, detections):
    template_questions = how_vertical_face_object_questions

    # 获取目标描述
    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    # 获取目标位置
    A_pos = np.array(A["position"])

    # 计算垂直旋转角度（pitch）：y轴相对 z轴方向的角度
    vertical_angle_deg = np.degrees(np.arctan2(A_pos[1], A_pos[2]))
    if vertical_angle_deg > 0:
        vertical_rotate = "down"
    else:
        vertical_rotate = "up"

    # 随机选项顺序
    options = ["up", "down"]
    random.shuffle(options)

    # 构建选项字符串
    option_str = f"(A) {options[0]}, (B) {options[1]}"

    # 随机选择模板并替换
    question_template = random.choice(template_questions)
    question_filled = smart_insert(A_desc, A_dense, "[A]", question_template)
    question = question_filled.replace("[option]", option_str)

    # 判断正确答案
    if options[0] == vertical_rotate:
        answer = "(A)"
    else:
        answer = "(B)"

    return question, answer

def is_facing_object(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_face 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_face:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_face 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_face:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

# face away from 背对 ----------------------------------------------------------------
def is_facing_away_from_object(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) yes (B) no"
        # 如果 is_back 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_back:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) no (B) yes"
        # 如果 is_back 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_back:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

# choice of relation

def choice_left_right(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) left (B) right"
        # 如果 is_left 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_left:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) right (B) left"
        # 如果 is_left 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_left:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def choice_front_behind(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) front (B) behind"
        # 如果 is_front 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_front:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) behind (B) front"
        # 如果 is_front 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_front:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def image_choice_above_below(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) above (B) below"
        # 如果 is_above 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_above:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) below (B) above"
        # 如果 is_above 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_above:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def world_choice_above_below(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) above (B) below"
        # 如果 is_above 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_above:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) below (B) above"
        # 如果 is_above 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_above:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def choice_wide_thin(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) wide (B) thin"
        # 如果 is_wide 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_wide:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) thin (B) wide"
        # 如果 is_wide 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_wide:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def choice_tall_short(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) tall (B) short"
        # 如果 is_tall 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_tall:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) short (B) tall"
        # 如果 is_tall 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_tall:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def choice_big_small(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) big (B) small"
        # 如果 is_big 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_big:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) small (B) big"
        # 如果 is_big 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_big:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

def choice_inside_outside(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) inside (B) outside"
        # 如果 is_inside 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_inside:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) outside (B) inside"
        # 如果 is_inside 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_inside:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer


def choice_point_close_far(A, B, C, gt_depth_path, wide_depth_path):
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

    # 随机化 yes/no 对应选项 (A) 或 (B)
    # 如果 random_order = True => 问题后缀 "(A) yes (B) no"
    # 如果 random_order = False => 问题后缀 "(A) no (B) yes"
    random_order = random.choice([True, False])

    if random_order:
        # (A) yes (B) no
        question += " (A) closer (B) farther"
        # 如果 is_closer 为 True，正确答案是 yes => "(A)"
        # 否则正确答案是 no => "(B)"
        if is_closer:
            correct_letter = "(A)"
        else:
            correct_letter = "(B)"
    else:
        # (A) no (B) yes
        question += " (A) farther (B) closer"
        # 如果 is_closer 为 True，正确答案是 yes => "(B)"
        # 否则正确答案是 no => "(A)"
        if is_closer:
            correct_letter = "(B)"
        else:
            correct_letter = "(A)"

    answer = f"{correct_letter} {answer}"

    return question, answer

# multi choice
def close_anchor_multi_choice(objects):
    """
    根据输入的物体列表生成一个多选题：
      - 随机选择一个物体为锚点（anchor）
      - 其余物体作为参考选项，计算锚点到各参考物体的点云距离
      - 锚点距离最近的参考物体作为正确答案
  
    每个物体应为一个字典，包含如下字段：
      - "spatial_caption": [str, ...]  # 至少包含一个描述文本
      - "dense_caption": str (可选)   # 如果没有，则使用 spatial_caption 里的随机一个
      - "pointcloud": dict，包含 "points" 和 "color" 字段
  
    参数:
      objects: 物体字典列表（3~5个物体）
      close_anchor_questions: 题目模板列表，每个模板包含占位符 [A]
  
    返回:
      question: 最终生成的题干（包含锚点描述和所有选项）
      correct_answer: 正确答案的选项字符串（例如 "(B) 某物体描述"）
    """
    if len(objects) < 3:
        raise ValueError("至少需要三个物体来生成多选题！")

    # 1. 随机选择一个锚点物体，并把其余物体作为参考选项
    anchor = random.choice(objects)
    reference_objs = [obj for obj in objects if obj is not anchor]
    random.shuffle(reference_objs)
    reference_objs = reference_objs[:5]

    # 获取锚点描述文本：优先使用 spatial_caption 随机选择，一个备用的 dense_caption
    anchor_desc = random.choice(anchor["spatial_caption"]).lower()
    anchor_dense = anchor.get("dense_caption", anchor_desc).lower()

    # 2. 将锚点点云数据转换成 Open3D 的点云对象
    anchor_pcd_data = anchor["pointcloud"]
    anchor_o3d_pcd = o3d.geometry.PointCloud()
    anchor_o3d_pcd.points = o3d.utility.Vector3dVector(anchor_pcd_data["points"])
    anchor_o3d_pcd.colors = o3d.utility.Vector3dVector(anchor_pcd_data["color"])

    distances = []
    # 3. 对每个参考物体计算锚点与其的点云距离
    for obj in reference_objs:
        pcd_data = obj["pointcloud"]
        candidate_o3d_pcd = o3d.geometry.PointCloud()
        candidate_o3d_pcd.points = o3d.utility.Vector3dVector(pcd_data["points"])
        candidate_o3d_pcd.colors = o3d.utility.Vector3dVector(pcd_data["color"])

        # 计算距离（假设 calculate_distances_between_point_clouds 已定义）
        dist = calculate_distances_between_point_clouds(anchor_o3d_pcd, candidate_o3d_pcd, human_readable=False)
        distances.append(dist)

    # 4. 找出距离最小的参考物体为正确答案
    correct_idx = distances.index(min(distances))

    # 5. 构造多选题选项，使用预定的标签列表（根据参考物体总数可以适当扩充）
    option_labels = ["(A)", "(B)", "(C)", "(D)", "(E)"]
    options_str_list = []
    for i, obj in enumerate(reference_objs):
        candidate_desc = random.choice(obj["spatial_caption"]).lower()
        options_str_list.append(f"{option_labels[i]} {candidate_desc}")
    all_options_str = "\n".join(options_str_list)

    # 构造题干：这里假设题目模板中有 "[A]" 占位符用于放入锚点物体描述
    question_template = random.choice(anchor_distance_nearest_multi_choice_questions)
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question_template).replace("[options]", all_options_str)

    # 返回题干以及正确选项字符串（例如 "(B) 某参考物体的描述"）
    correct_answer = options_str_list[correct_idx]
    return question, correct_answer


def far_anchor_multi_choice(objects):
    """
    根据输入的物体列表生成一个多选题：
      - 随机选择一个物体为锚点（anchor）
      - 其余物体作为参考选项，计算锚点到各参考物体的点云距离
      - 锚点距离最远的参考物体作为正确答案
  
    每个物体应为一个字典，包含如下字段：
      - "spatial_caption": [str, ...]  # 至少包含一个描述文本
      - "dense_caption": str (可选)   # 如果没有，则使用 spatial_caption 里的随机一个
      - "pointcloud": dict，包含 "points" 和 "color" 字段
  
    参数:
      objects: 物体字典列表（3~5个物体）
      far_anchor_questions: 题目模板列表，每个模板包含占位符 [anchor] 与 [options]
  
    返回:
      question: 最终生成的题干（包含锚点描述和所有选项）
      correct_answer: 正确答案的选项字符串（例如 "(B) 某物体描述"）
    """
    import random
    import open3d as o3d  # 确保已安装 open3d 库

    if len(objects) < 3:
        raise ValueError("至少需要三个物体来生成多选题！")

    # 1. 随机选择一个锚点物体，并把其余物体作为参考选项
    anchor = random.choice(objects)
    reference_objs = [obj for obj in objects if obj is not anchor]
    random.shuffle(reference_objs)
    reference_objs = reference_objs[:5]

    # 获取锚点描述文本：优先使用 spatial_caption 随机选择，一个备用的 dense_caption
    anchor_desc = random.choice(anchor["spatial_caption"]).lower()
    anchor_dense = anchor.get("dense_caption", anchor_desc).lower()

    # 2. 将锚点点云数据转换成 Open3D 的点云对象
    anchor_pcd_data = anchor["pointcloud"]
    anchor_o3d_pcd = o3d.geometry.PointCloud()
    anchor_o3d_pcd.points = o3d.utility.Vector3dVector(anchor_pcd_data["points"])
    anchor_o3d_pcd.colors = o3d.utility.Vector3dVector(anchor_pcd_data["color"])

    distances = []
    # 3. 对每个参考物体计算锚点与其的点云距离
    for obj in reference_objs:

        pcd_data = obj["pointcloud"]
        candidate_o3d_pcd = o3d.geometry.PointCloud()
        candidate_o3d_pcd.points = o3d.utility.Vector3dVector(pcd_data["points"])
        candidate_o3d_pcd.colors = o3d.utility.Vector3dVector(pcd_data["color"])

        # 计算距离（假设 calculate_distances_between_point_clouds 已定义）
        dist = calculate_distances_between_point_clouds(anchor_o3d_pcd, candidate_o3d_pcd, human_readable=False)
        distances.append(dist)

    # 4. 找出距离最大的参考物体作为正确答案
    correct_idx = distances.index(max(distances))

    # 5. 构造多选题选项，使用预定的标签列表（根据参考物体总数可以适当扩充）
    option_labels = ["(A)", "(B)", "(C)", "(D)", "(E)"]
    options_str_list = []
    for i, obj in enumerate(reference_objs):
        candidate_desc = random.choice(obj["spatial_caption"]).lower()
        options_str_list.append(f"{option_labels[i]} {candidate_desc}")
    all_options_str = "\n".join(options_str_list)

    # 构造题干：假设题目模板中有 "[anchor]" 占位符用于放入锚点物体描述，以及 "[options]" 用于放入选项
    question_template = random.choice(anchor_distance_farthest_multi_choice_questions)
    question = smart_insert(anchor_desc, anchor_dense, "[anchor]", question_template).replace("[options]", all_options_str)

    # 返回题干以及正确选项字符串（例如 "(B) 某参考物体的描述"）
    correct_answer = options_str_list[correct_idx]
    return question, correct_answer



class PromptGenerator:
    def evaluate_predicates_on_pairs(self, detections, gt_depth_path, wide_depth_path):
        """
            根据输入的 detections 数量，分别应用一元、二元、三元谓词函数生成 QA。
            返回格式为一个 results 列表，包含 (qa_result, object_index_1, object_index_2, ..., func_name, qa_type)
        """
        results = []

        one_object_choice_prompts = [
            how_horizontal_face_object,
            how_vertical_face_object
        ]

        # 至少两个物体
        yes_or_no_choice_prompts = [
            left_predicate,
            right_predicate,
            image_above_predicate,
            image_below_predicate,
            world_above_predicate,
            world_below_predicate,
            touch_predicate,
            far_from_predicate,
            front_predicate,
            behind_predicate,
            wide_predicate,
            thin_predicate,
            tall_predicate,
            short_predicate,
            big_predicate,
            small_predicate,
            contain_predicate,
            outside_predicate,
            is_facing_object,
            is_facing_away_from_object,
        ]

        # 至少两个物体
        double_choice_prompts = [
            choice_left_right,
            image_choice_above_below,
            world_choice_above_below,
            choice_front_behind,
            choice_wide_thin,
            choice_tall_short,
            choice_big_small,
            choice_inside_outside,
            choice_point_close_far,
        ]

        # 至少三个物体
        multi_choice_prompts = [
            close_anchor_multi_choice,
            far_anchor_multi_choice,
        ]

        if len(detections) == 0:
            return results

        # --------------------------
        # 处理单个物体的情况
        # --------------------------
        elif len(detections) == 1:
            # 一元谓词：从有序组合中选取
            one_obj_all_combinations = list(permutations(range(len(detections)), 1))
            random.shuffle(one_obj_all_combinations)
            one_obj_selected_combinations = one_obj_all_combinations[:1]
            one_obj_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_obj_object_pairs:
                valid_prompt_variants = one_object_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 2)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, '', '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

        # --------------------------
        # 处理两个物体的情况
        # --------------------------

        elif len(detections) == 2:

            # 一元谓词：从有序组合中选取
            one_obj_all_combinations = list(permutations(range(len(detections)), 1))
            random.shuffle(one_obj_all_combinations)
            one_obj_selected_combinations = one_obj_all_combinations[:2]
            one_obj_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_obj_object_pairs:
                valid_prompt_variants = one_object_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 1)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, '', '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:3]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = yes_or_no_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 6)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, '', gt_depth_path, wide_depth_path)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'yes_or_no_choice_prompts'))


            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:3]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = double_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 4)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, '', gt_depth_path, wide_depth_path)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'double_choice_prompts'))

        if len(detections) >= 3:
            
            # 一元谓词：从有序组合中选取
            one_obj_all_combinations = list(permutations(range(len(detections)), 1))
            random.shuffle(one_obj_all_combinations)
            one_obj_selected_combinations = one_obj_all_combinations[:2]
            one_obj_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_obj_object_pairs:
                valid_prompt_variants = one_object_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 1)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, '', '', gt_depth_path, wide_depth_path, detections)
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:3]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = yes_or_no_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 6)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, '', gt_depth_path, wide_depth_path)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'yes_or_no_choice_prompts'))


            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(permutations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:3]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = double_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 4)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, '', gt_depth_path, wide_depth_path)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'double_choice_prompts'))

            for _ in range(2):
                valid_prompt_variants = multi_choice_prompts
                selected_predicates_choices = random.sample(valid_prompt_variants, 1)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(detections)
                    results.append((qa, '', '', '', prompt_func.__name__, 'multi_choice_prompts'))

        return results


