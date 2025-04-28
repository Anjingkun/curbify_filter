from visual_prompt_template import *
import random
from visual_utils import *
import numpy as np
import open3d as o3d
import imageio

def left_right_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = left_right_visual_choice_question

    A_dense = A.get("dense_caption").lower()
    B_dense = B.get("dense_caption").lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_pos = A["position"]
    B_pos = B["position"]

    is_left = A_pos[0] < B_pos[0]

    question = random.choice(template_questions)
    question = question.replace('[A]', A_label).replace('[B]', B_label)

    option_1_left = random.choice([True, False])
    if option_1_left:
        question = question.replace('[option 1]', 'left').replace('[option 2]', 'right')
        if is_left:
            answer = "(A)"
        else:
            answer = "(B)"
    else:
        question = question.replace('[option 1]', 'right').replace('[option 2]', 'left')
        if is_left:
            answer = "(B)"
        else:
            answer = "(A)"

    
    output_image_path = draw_one_bbox_on_image(image_path, A)

    return question, answer, output_image_path

def image_above_below_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = image_above_below_visual_choice_question

    A_dense = A.get("dense_caption").lower()
    B_dense = B.get("dense_caption").lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_pos = A["position"]
    B_pos = B["position"]

    is_above = A_pos[1] < B_pos[1]

    question = random.choice(template_questions)
    question = question.replace('[A]', A_label).replace('[B]', B_label)

    option_1_above = random.choice([True, False])
    if option_1_above:
        question = question.replace('[option 1]', 'above').replace('[option 2]', 'below')
        if is_above:
            answer = "(A)"
        else:
            answer = "(B)"
    else:
        question = question.replace('[option 1]', 'below').replace('[option 2]', 'above')
        if is_above:
            answer = "(B)"
        else:
            answer = "(A)"

    output_image_path = draw_one_bbox_on_image(image_path, A)
    
    return question, answer, output_image_path

def obj_close_camera_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = obj_close_visual_choice

    A_dense = A.get("dense_caption").lower()
    B_dense = B.get("dense_caption").lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    question = random.choice(template_questions)
    question = question.replace('[A]', A_label).replace('[B]', B_label)

    A_front = A_min_z < B_min_z

    if A_front:
        answer = "(A)"
    else:
        answer = "(B)"
    
    output_image_path = draw_two_bbox_on_image(image_path, A, B)

    return question, answer, output_image_path

def obj_far_camera_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = obj_far_visual_choice

    A_dense = A.get("dense_caption").lower()
    B_dense = B.get("dense_caption").lower()

    A_label = A["class_name"]
    B_label = B["class_name"]

    A_min_z = np.min(np.array(A["corners"])[:, 2])
    B_min_z = np.min(np.array(B["corners"])[:, 2])

    question = random.choice(template_questions)
    question = question.replace('[A]', A_label).replace('[B]', B_label)

    A_behind = A_min_z > B_min_z

    if A_behind:
        answer = "(A)"
    else:
        answer = "(B)"
    
    output_image_path = draw_two_bbox_on_image(image_path, A, B)

    return question, answer, output_image_path

def obj_close_anchor_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = obj_close_anchor_visual_choice_question

    A_dense = A.get("dense_caption").lower()
    B_dense = B.get("dense_caption").lower()
    C_dense = C.get("dense_caption").lower()

    A_label = A["class_name"]
    B_label = B["class_name"]
    C_label = C["class_name"]

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

    question = random.choice(template_questions)
    question = question.replace('[A]', A_label).replace('[B]', B_label).replace('[C]', C_label)

    A_close = A_C_distance < B_C_distance

    if A_close:
        answer = "(A)"
    else:
        answer = "(B)"
    
    output_image_path = draw_three_bbox_on_image(image_path, A, B, C)

    return question, answer, output_image_path

def obj_far_anchor_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = obj_far_anchor_visual_choice_question

    A_dense = A.get("dense_caption").lower()
    B_dense = B.get("dense_caption").lower()
    C_dense = C.get("dense_caption").lower()

    A_label = A["class_name"]
    B_label = B["class_name"]
    C_label = C["class_name"]

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

    question = random.choice(template_questions)
    question = question.replace('[A]', A_label).replace('[B]', B_label).replace('[C]', C_label)

    A_far = A_C_distance > B_C_distance

    if A_far:
        answer = "(A)"
    else:
        answer = "(B)"
    
    output_image_path = draw_three_bbox_on_image(image_path, A, B, C)

    return question, answer, output_image_path

def point_close_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = point_close_visual_choice_question

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

    A_close = A_depth < B_depth

    if A_close:
        answer = "(A)"
    else:
        answer = "(B)"
    question = random.choice(template_questions)
    output_image_path = draw_two_point_on_image(image_path, A_point_yx, B_point_yx)

    return question, answer, output_image_path

def point_far_visual_choice(A, B, C, image_path, gt_depth_path, wide_depth_path):
    template_questions = point_far_visual_choice_question

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

    A_far = A_depth > B_depth

    if A_far:
        answer = "(A)"
    else:
        answer = "(B)"
    question = random.choice(template_questions)
    output_image_path = draw_two_point_on_image(image_path, A_point_yx, B_point_yx)

    return question, answer, output_image_path


from itertools import combinations
from itertools import permutations
class VisualPromptGenerator:
    def evaluate_predicates_on_pairs(self, detections, image_path, gt_depth_path, wide_depth_path):
        results = []

        # 二元谓词函数列表

        two_object_can_left_right_above_below = [
            left_right_visual_choice, image_above_below_visual_choice,
        ]

        two_object_can_close_far_bbox = [
            obj_close_camera_visual_choice, obj_far_camera_visual_choice,
        ]

        two_object_can_close_far_point = [
            point_far_visual_choice, point_close_visual_choice
        ]

        # 三元谓词函数列表

        three_object_can = [
            obj_close_anchor_visual_choice,
            obj_far_anchor_visual_choice,
        ]

        # 无目标时，直接返回空列表
        if len(detections) < 2:
            return results

        # --------------------------
        # 处理两个物体的情况
        # --------------------------
        elif len(detections) == 2:
            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(combinations(range(len(detections)), 2))
            two_obj_selected_combinations = two_obj_all_combinations[:1]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = two_object_can_left_right_above_below + two_object_can_close_far_bbox + two_object_can_close_far_point

                selected_predicates_choices = random.sample(valid_prompt_variants, 6)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, '', image_path, gt_depth_path, wide_depth_path)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'two_object_visual_choice'))
            return results
        
        # --------------------------
        # 处理三个物体的情况
        # --------------------------
        elif len(detections) >= 3:
            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(combinations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations[:2]
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = two_object_can_close_far_bbox

                selected_predicates_choices = random.sample(valid_prompt_variants, 2)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, '', image_path, gt_depth_path, wide_depth_path)
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'two_object_visual_choice'))

            # 三元谓词：从有序组合中选取
            three_obj_all_permutations = list(permutations(range(len(detections)), 3))
            random.shuffle(three_obj_all_permutations)
            three_obj_selected_permutations = three_obj_all_permutations[:2]
            three_object_pairs = [(detections[i], detections[j], detections[k], i, j, k) for i, j, k in three_obj_selected_permutations]
            for A, B, C, A_index, B_index, C_index in three_object_pairs:
                valid_prompt_variants = three_object_can

                selected_predicates_choices = random.sample(valid_prompt_variants, 2)

                for prompt_func in selected_predicates_choices:
                    qa = prompt_func(A, B, C, image_path, gt_depth_path, wide_depth_path)
                    results.append((qa, A_index, B_index, C_index, prompt_func.__name__, 'three_object_visual_choice'))
            return results
            