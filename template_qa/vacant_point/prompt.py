from itertools import combinations, permutations
from prompt_template import *
from prompt_utils import *
import copy

def left_vacant(A, B, all_objects, R_gravity, depth_map, K):
    question_templates = left_vacant_template_questions
    answer_templates = left_vacant_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    for obj in all_objects:
        corners = np.array(obj["corners"])
        obj["corners"] = transform_points_with_rotation(R_gravity, corners)

    labeled_obj_id = A["id"]
    target_obj = next(obj for obj in all_objects if obj["id"] == labeled_obj_id)

    # Step 4: Find platform
    platform_obj = find_platform_for_target(target_obj, all_objects, height_thresh=0.05, overlap_thresh=0.7)

    if platform_obj is None:
        return None

    obstacles = find_objects_on_platform(target_obj, platform_obj, all_objects)

    placeable_poly = compute_placeable_area(platform_obj, obstacles)

    if placeable_poly is None or placeable_poly.is_empty:
        return None

    target_bottom_y = bbox_bottom_surface_y(target_obj["corners"])

    platform_top_y = bbox_top_surface_y(platform_obj["corners"])

    y_height = max(target_bottom_y, platform_top_y)

    fan_points = sample_placeable_points_in_fan(
            placeable_poly, target_obj,
            direction="left",
            base_radius=0.3,
            fan_angle_deg=90,
            num_rays=90,
            num_samples_per_ray=100
        )
    
    if len(fan_points) < 2000:
        return None

    # 1. 构造 3D 点
    pts_3d = construct_3d_points(fan_points, y_height)

    # 2. 转换回相机坐标系
    pts_cam = transform_to_camera_coords(R_gravity, pts_3d)
    
    # 3. 投影到图像
    pts_img = project_to_image(pts_cam, K)

    # 过滤遮挡点
    visible_pts_img, visible_pts_cam = filter_visible_points_by_depth(pts_img, pts_cam, depth_map,depth_threshold=0.025)

    if len(visible_pts_img) < 2000:
        return None
    representative_point = select_representative_point(visible_pts_img, visible_pts_cam, depth_map, depth_threshold=0.025)
    img_shape = A["rle"]["size"]
    left_coord_str = f"[({representative_point[0] * 2 / img_shape[1]:.3f}, {representative_point[1] * 2 / img_shape[0]:.3f})]"

    question = random.choice(question_templates)
    answer = random.choice(answer_templates)
    question = smart_insert(A_desc, A_dense, "[A]", question)
    answer = answer.replace("[X]", left_coord_str)

    return question, answer

def right_vacant(A, B, all_objects, R_gravity, depth_map, K):
    question_templates = right_vacant_template_questions
    answer_templates = right_vacant_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    for obj in all_objects:
        corners = np.array(obj["corners"])
        obj["corners"] = transform_points_with_rotation(R_gravity, corners)

    labeled_obj_id = A["id"]
    target_obj = next(obj for obj in all_objects if obj["id"] == labeled_obj_id)

    # Step 4: Find platform
    platform_obj = find_platform_for_target(target_obj, all_objects, height_thresh=0.05, overlap_thresh=0.7)

    if platform_obj is None:
        return None

    obstacles = find_objects_on_platform(target_obj, platform_obj, all_objects)

    placeable_poly = compute_placeable_area(platform_obj, obstacles)

    if placeable_poly is None or placeable_poly.is_empty:
        return None

    target_bottom_y = bbox_bottom_surface_y(target_obj["corners"])

    platform_top_y = bbox_top_surface_y(platform_obj["corners"])

    y_height = max(target_bottom_y, platform_top_y)

    fan_points = sample_placeable_points_in_fan(
            placeable_poly, target_obj,
            direction="right",
            base_radius=0.3,
            fan_angle_deg=90,
            num_rays=90,
            num_samples_per_ray=100
        )
    
    if len(fan_points) < 2000:
        return None
    
    # 1. 构造 3D 点
    pts_3d = construct_3d_points(fan_points, y_height)

    # 2. 转换回相机坐标系
    pts_cam = transform_to_camera_coords(R_gravity, pts_3d)
    
    # 3. 投影到图像
    pts_img = project_to_image(pts_cam, K)

    # 过滤遮挡点
    visible_pts_img, visible_pts_cam = filter_visible_points_by_depth(pts_img, pts_cam, depth_map,depth_threshold=0.025)

    if len(visible_pts_img) < 2000:
        return None
    representative_point = select_representative_point(visible_pts_img, visible_pts_cam, depth_map, depth_threshold=0.025)
    img_shape = A["rle"]["size"]
    right_coord_str = f"[({representative_point[0] * 2 / img_shape[1]:.3f}, {representative_point[1] * 2 / img_shape[0]:.3f})]"

    question = random.choice(question_templates)
    answer = random.choice(answer_templates)
    question = smart_insert(A_desc, A_dense, "[A]", question)
    answer = answer.replace("[X]", right_coord_str)

    return question, answer

def front_vacant(A, B, all_objects, R_gravity, depth_map, K):
    question_templates = front_vacant_template_questions
    answer_templates = front_vacant_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    for obj in all_objects:
        corners = np.array(obj["corners"])
        obj["corners"] = transform_points_with_rotation(R_gravity, corners)

    labeled_obj_id = A["id"]
    target_obj = next(obj for obj in all_objects if obj["id"] == labeled_obj_id)

    # Step 4: Find platform
    platform_obj = find_platform_for_target(target_obj, all_objects, height_thresh=0.05, overlap_thresh=0.7)

    if platform_obj is None:
        return None

    obstacles = find_objects_on_platform(target_obj, platform_obj, all_objects)

    placeable_poly = compute_placeable_area(platform_obj, obstacles)

    if placeable_poly is None or placeable_poly.is_empty:
        return None

    target_bottom_y = bbox_bottom_surface_y(target_obj["corners"])

    platform_top_y = bbox_top_surface_y(platform_obj["corners"])

    y_height = max(target_bottom_y, platform_top_y)

    fan_points = sample_placeable_points_in_fan(
            placeable_poly, target_obj,
            direction="front",
            base_radius=0.3,
            fan_angle_deg=90,
            num_rays=90,
            num_samples_per_ray=100
        )

    if len(fan_points) < 2000:
        return None
    
    # 1. 构造 3D 点
    pts_3d = construct_3d_points(fan_points, y_height)

    # 2. 转换回相机坐标系
    pts_cam = transform_to_camera_coords(R_gravity, pts_3d)
    
    # 3. 投影到图像
    pts_img = project_to_image(pts_cam, K)

    # 过滤遮挡点
    visible_pts_img, visible_pts_cam = filter_visible_points_by_depth(pts_img, pts_cam, depth_map,depth_threshold=0.025)

    if len(visible_pts_img) < 2000:
        return None
    representative_point = select_representative_point(visible_pts_img, visible_pts_cam, depth_map, depth_threshold=0.025)
    img_shape = A["rle"]["size"]
    front_coord_str = f"[({representative_point[0] * 2 / img_shape[1]:.3f}, {representative_point[1] * 2 / img_shape[0]:.3f})]"

    question = random.choice(question_templates)
    answer = random.choice(answer_templates)
    question = smart_insert(A_desc, A_dense, "[A]", question)
    answer = answer.replace("[X]", front_coord_str)

    return question, answer

def behind_vacant(A, B, all_objects, R_gravity, depth_map, K):
    question_templates = behind_vacant_template_questions
    answer_templates = behind_vacant_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    for obj in all_objects:
        corners = np.array(obj["corners"])
        obj["corners"] = transform_points_with_rotation(R_gravity, corners)

    labeled_obj_id = A["id"]
    target_obj = next(obj for obj in all_objects if obj["id"] == labeled_obj_id)

    # Step 4: Find platform
    platform_obj = find_platform_for_target(target_obj, all_objects, height_thresh=0.05, overlap_thresh=0.7)

    if platform_obj is None:
        return None

    obstacles = find_objects_on_platform(target_obj, platform_obj, all_objects)

    placeable_poly = compute_placeable_area(platform_obj, obstacles)

    if placeable_poly is None or placeable_poly.is_empty:
        return None

    target_bottom_y = bbox_bottom_surface_y(target_obj["corners"])

    platform_top_y = bbox_top_surface_y(platform_obj["corners"])

    y_height = max(target_bottom_y, platform_top_y)

    fan_points = sample_placeable_points_in_fan(
            placeable_poly, target_obj,
            direction="back",
            base_radius=0.3,
            fan_angle_deg=90,
            num_rays=90,
            num_samples_per_ray=100
        )
    
    if len(fan_points) < 2000:
        return None
    
    # 1. 构造 3D 点
    pts_3d = construct_3d_points(fan_points, y_height)

    # 2. 转换回相机坐标系
    pts_cam = transform_to_camera_coords(R_gravity, pts_3d)
    
    # 3. 投影到图像
    pts_img = project_to_image(pts_cam, K)

    # 过滤遮挡点
    visible_pts_img, visible_pts_cam = filter_visible_points_by_depth(pts_img, pts_cam, depth_map,depth_threshold=0.025)

    if len(visible_pts_img) < 2000:
        return None
    representative_point = select_representative_point(visible_pts_img, visible_pts_cam, depth_map, depth_threshold=0.025)
    img_shape = A["rle"]["size"]
    behind_coord_str = f"[({representative_point[0] * 2 / img_shape[1]:.3f}, {representative_point[1] * 2 / img_shape[0]:.3f})]"

    question = random.choice(question_templates)
    answer = random.choice(answer_templates)
    question = smart_insert(A_desc, A_dense, "[A]", question)
    answer = answer.replace("[X]", behind_coord_str)

    return question, answer

def above_vacant(A, B, all_objects, R_gravity, depth_map, K):
    question_templates = above_vacant_template_questions
    answer_templates = above_vacant_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    for obj in all_objects:
        corners = np.array(obj["corners"])
        obj["corners"] = transform_points_with_rotation(R_gravity, corners)

    labeled_obj_id = A["id"]
    target_obj = next(obj for obj in all_objects if obj["id"] == labeled_obj_id)

    poly_area = Polygon(bbox_xz_polygon(target_obj["corners"])).area

    if poly_area < 0.06237 / 2: # A4纸面积的一半 
        return None

    top_y = bbox_top_surface_y(target_obj["corners"])

    # 在物体的 XZ 投影范围内采样点
    vertical_points = sample_points_in_bbox_xz(target_obj, num_points=300, scale_rate=0.75)

    # 构造 3D 点
    pts_3d = construct_3d_points(vertical_points, top_y)

    # 转换回相机坐标系
    pts_cam = transform_to_camera_coords(R_gravity, pts_3d)

    # 投影到图像
    pts_img = project_to_image(pts_cam, K)

    # 过滤遮挡点
    visible_pts_img, visible_pts_cam = filter_visible_points_by_depth(pts_img, pts_cam, depth_map, depth_threshold=0.025)

    if len(visible_pts_img) < 100:
        return None
    
    representative_point = select_representative_point(visible_pts_img, visible_pts_cam, depth_map, depth_threshold=0.025)

    img_shape = A["rle"]["size"]
    above_coord_str = f"[({representative_point[0] * 2 / img_shape[1]:.3f}, {representative_point[1] *2 / img_shape[0]:.3f})]"

    question = random.choice(question_templates)
    answer = random.choice(answer_templates)
    question = smart_insert(A_desc, A_dense, "[A]", question)
    answer = answer.replace("[X]", above_coord_str)

    return question, answer

def below_vacant(A, B, all_objects, R_gravity, depth_map, K):
    question_templates = below_vacant_template_questions
    answer_templates = below_vacant_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()

    for obj in all_objects:
        corners = np.array(obj["corners"])
        obj["corners"] = transform_points_with_rotation(R_gravity, corners)

    labeled_obj_id = A["id"]
    target_obj = next(obj for obj in all_objects if obj["id"] == labeled_obj_id)

    poly_area = Polygon(bbox_xz_polygon(target_obj["corners"])).area

    if poly_area < 0.06237 / 2: # A4纸的一半
        return None

    target_bottom_y = bbox_bottom_surface_y(target_obj["corners"])

    # 找到位于目标物体下方的平台
    platform_obj = find_platform_below_target(target_obj, all_objects, height_buffer=0.05, overlap_thresh=0.7)

    if platform_obj is None:
        return None

    # 找到平台上的物体
    obstacles = find_objects_on_platform_below_target(target_obj, platform_obj, all_objects)

    # 获得可放置物体的区域
    placeable_poly = compute_placeable_area(target_obj, obstacles)
    placeable_poly = Polygon(bbox_xz_polygon(platform_obj["corners"])).intersection(placeable_poly)
    if placeable_poly is None or placeable_poly.is_empty:
        return None

    # 在空闲区域的 XZ 投影范围内采样点
    vertical_points = sample_points_in_bbox_xz_below(target_obj, placeable_poly, num_points=300, scale_rate=0.75)

    if len(vertical_points) < 100:
        return None
    
    # 获得最低的高度
    y_height = max(target_bottom_y, bbox_top_surface_y(platform_obj["corners"]))

    # 构造 3D 点
    pts_3d = construct_3d_points(vertical_points, y_height)

    # 转换回相机坐标系
    pts_cam = transform_to_camera_coords(R_gravity, pts_3d)

    # 投影到图像
    pts_img = project_to_image(pts_cam, K)
    
    # 过滤遮挡点
    visible_pts_img, visible_pts_cam = filter_visible_points_by_depth(pts_img, pts_cam, depth_map, depth_threshold=0.025)

    if len(visible_pts_img) < 100:
        return None
    
    representative_point = select_representative_point(visible_pts_img, visible_pts_cam, depth_map, depth_threshold=0.025)

    img_shape = A["rle"]["size"]
    below_coord_str = f"[({representative_point[0] * 2 / img_shape[1]:.3f}, {representative_point[1] *2 / img_shape[0]:.3f})]"

    question = random.choice(question_templates)
    answer = random.choice(answer_templates)
    question = smart_insert(A_desc, A_dense, "[A]", question)
    answer = answer.replace("[X]", below_coord_str)

    return question, answer
    
def between_vacant(A, B, all_objects, R_gravity, depth_map, K):
    question_templates = between_vacant_template_questions
    answer_templates = between_vacant_template_answers

    A_desc = random.choice(A["spatial_caption"]).lower()
    A_dense = A.get("dense_caption", A_desc).lower()
    B_desc = random.choice(B["spatial_caption"]).lower()
    B_dense = B.get("dense_caption", B_desc).lower()

    for obj in all_objects:
        corners = np.array(obj["corners"])
        obj["corners"] = transform_points_with_rotation(R_gravity, corners)

    # Step 3: Extract target object
    target_obj_1 = next(obj for obj in all_objects if obj["id"] == A["id"])
    target_obj_2 = next(obj for obj in all_objects if obj["id"] == B["id"])

    # Step 4: Find platform
    platform_obj_1 = find_platform_for_target(target_obj_1, all_objects, height_thresh=0.05, overlap_thresh=0.7)
    platform_obj_2 = find_platform_for_target(target_obj_2, all_objects, height_thresh=0.05, overlap_thresh=0.7)
    if platform_obj_1 is None or platform_obj_2 is None:
        return None
    
    if platform_obj_1["id"] != platform_obj_2["id"]:
        return None
    platform_obj = platform_obj_1 # 共享平台

    obstacles = find_objects_on_two_target_platform(target_obj_1, target_obj_2, platform_obj, all_objects)

    between_area = get_between_area(target_obj_1, target_obj_2, platform_obj)

    if between_area.area < 0.06237 / 8: # A4纸的八分之一
        return None
    
    between_placeable_poly = compute_between_placeable_area(target_obj_1, target_obj_2, platform_obj, obstacles)

    if between_placeable_poly is None or between_placeable_poly.is_empty:
        return None

    between_points = sample_placeable_points_in_between_area(between_placeable_poly, target_obj_1, target_obj_2, platform_obj, num_samples=1000)

    if len(between_points) < 618:
        return None
    
    # 计算每个方向的中心点# 1. 构造 3D 点
    platform_top_y = bbox_top_surface_y(platform_obj["corners"])
    target_1_bottom_y = bbox_bottom_surface_y(target_obj_1["corners"])
    target_2_bottom_y = bbox_bottom_surface_y(target_obj_2["corners"])

    y_height = max(target_1_bottom_y, target_2_bottom_y, platform_top_y)

    pts_3d = construct_3d_points(between_points, y_height)

    # 2. 转换回相机坐标系
    pts_cam = transform_to_camera_coords(R_gravity, pts_3d)

    # 3. 投影到图像
    pts_img = project_to_image(pts_cam, K)

    # 过滤遮挡点
    visible_pts_img, visible_pts_cam = filter_visible_points_by_depth(pts_img, pts_cam, depth_map,depth_threshold=0.025)

    if len(visible_pts_img) < 618:
        return None
    
    representative_point = select_representative_point(visible_pts_img, visible_pts_cam, depth_map, depth_threshold=0.025)

    img_shape = A["rle"]["size"]
    between_coord_str = f"[({representative_point[0] * 2 / img_shape[1]:.3f}, {representative_point[1] *2 / img_shape[0]:.3f})]"

    question = random.choice(question_templates)
    answer = random.choice(answer_templates)

    question = smart_insert(A_desc, A_dense, "[A]", question)
    question = smart_insert(B_desc, B_dense, "[B]", question)

    answer = answer.replace("[X]", between_coord_str)


    return question, answer

class PromptGenerator:
    def evaluate_predicates_on_pairs(self, detections, instances_path, gt_depth_path, wide_depth_path, T_gravity_path, K_path):
        """
            根据输入的 detections 数量，分别应用一元、二元、三元谓词函数生成 QA。
            返回格式为一个 results 列表，包含 (qa_result, object_index_1, object_index_2, ..., func_name, qa_type)
        """
        results = []
        K = np.array(load_json(K_path))
        all_objects = load_json(instances_path)
        R_gravity = np.array(load_json(T_gravity_path))
        depth_map = np.array(cv2.imread(wide_depth_path, cv2.IMREAD_UNCHANGED), dtype=np.float32)
        depth_map = depth_map / 1000.0
        # 一元谓词函数列表（单个物体）
        one_object_can = [
            left_vacant,
            right_vacant,
            front_vacant,
            behind_vacant,
            above_vacant,
            below_vacant,
        ]

        two_object_can = [
            between_vacant
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
            one_obj_selected_combinations = one_obj_all_combinations
            one_obj_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_obj_object_pairs:
                valid_prompt_variants = one_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 6)

                for prompt_func in selected_predicates_choices:
                    all_objects_copy = copy.deepcopy(all_objects)
                    qa = prompt_func(A, '', all_objects_copy, R_gravity, depth_map, K)
                    if qa is None:
                        continue
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

            return results
        
        elif len(detections) >= 2:
            # 获取所有单物体组合（只有一个）
            one_obj_all_combinations = list(permutations(range(len(detections)), 1))
            random.shuffle(one_obj_all_combinations)
            one_obj_selected_combinations = one_obj_all_combinations
            one_obj_object_pairs = [(detections[i], i) for (i,) in one_obj_selected_combinations]

            for A, A_index in one_obj_object_pairs:
                valid_prompt_variants = one_object_can
                selected_predicates_choices = random.sample(valid_prompt_variants, 6)

                for prompt_func in selected_predicates_choices:
                    all_objects_copy = copy.deepcopy(all_objects)
                    qa = prompt_func(A, '', all_objects_copy, R_gravity, depth_map, K)
                    if qa is None:
                        continue
                    results.append((qa, A_index, '', '', prompt_func.__name__, 'one_object_qa'))

            # 二元谓词：从有序组合中选取
            two_obj_all_combinations = list(combinations(range(len(detections)), 2))
            random.shuffle(two_obj_all_combinations)
            two_obj_selected_combinations = two_obj_all_combinations
            two_object_pairs = [(detections[i], detections[j], i, j) for i, j in two_obj_selected_combinations]

            for A, B, A_index, B_index in two_object_pairs:
                valid_prompt_variants = two_object_can
                # 遍历每个类别，每类采样 1 个
                selected_predicates_choices = random.sample(valid_prompt_variants, 1)

                for prompt_func in selected_predicates_choices:
                    all_objects_copy = copy.deepcopy(all_objects)
                    qa = prompt_func(A, B, all_objects_copy, R_gravity, depth_map, K)
                    if qa is None:
                        continue
                    results.append((qa, A_index, B_index, '', prompt_func.__name__, 'two_object_qa'))

            return results