import os
import random
import json
import numpy as np
from pathlib import Path
from scipy.spatial.transform import Rotation as R
from PIL import Image  # 用于读取深度图判断拍摄方向
import multiprocessing as mp

import tqdm

# 模板问答列表
# 模板，其中 [option] 为占位符
left_right_rotate_question_templates = [
    "How did the camera likely rotate when shooting the video? [option]",
    "How did the camera likely rotate when shooting the video? [option]",
    "Which way did the camera rotate in the video? [option]",
    "Which way did the camera rotate in the video? [option]",
    "Did the camera rotate left or right? [option]",
    "Did the camera rotate left or right? [option]",
]

up_down_rotate_question_templates = [
    "How did the camera likely rotate when shooting the video? [option]",
    "How did the camera likely rotate when shooting the video? [option]",
    "Which way did the camera rotate in the video? [option]",
    "Which way did the camera rotate in the video? [option]",
    "Did the camera rotate upward or downward? [option]",
    "Did the camera rotate upward or downward? [option]",
]

def generate_lr_question(yaw):
    """
    根据 yaw 值生成左右旋转题目。
    
    当 yaw < 0 时认为方向是 rotated left；
    当 yaw > 0 时认为方向是 rotated right。
    
    随机选取一个模板，并随机决定选项顺序。
    输出的 question 会替换模板中的 [option] 为：
      (A) rotated left (B) rotated right
      或者
      (A) rotated right (B) rotated left
      
    同时答案会以类似 "(A) rotated left" 的格式返回。
    """
    # 随机选择一个模板
    template = random.choice(left_right_rotate_question_templates)
    # 随机决定选项顺序
    order = random.choice(["lr", "rl"])
    if order == "lr":
        options_text = "(A) rotated left (B) rotated right"
        if yaw < 0:
            answer = "(A)"
        else:
            answer = "(B)"
    else:
        options_text = "(A) rotated right (B) rotated left"
        if yaw > 0:
            answer = "(A)"
        else:
            answer = "(B)"
    # 替换模板中的占位符
    question = template.replace("[option]", options_text)
    return question, answer

def generate_ud_question(pitch):
    """
    根据 pitch 值生成上下旋转题目。
    
    当 pitch > 0 时认为方向是 rotated upward；
    当 pitch < 0 时认为方向是 rotated downward。
    
    随机选取一个模板，并随机决定选项顺序。
    输出的 question 会替换模板中的 [option] 为：
      (A) rotated upward (B) rotated downward
      或者
      (A) rotated downward (B) rotated upward
      
    同时答案会以类似 "(A) rotated upward" 的格式返回。
    """
    template = random.choice(up_down_rotate_question_templates)
    order = random.choice(["ud", "du"])
    if order == "ud":
        options_text = "(A) rotated upward (B) rotated downward"
        if pitch > 0:
            answer = "(A)"
        else:
            answer = "(B)"
    else:
        options_text = "(A) rotated downward (B) rotated upward"
        if pitch < 0:
            answer = "(A)"
        else:
            answer = "(B)"
    question = template.replace("[option]", options_text)
    return question, answer

def load_rt(rt_json_path):
    """加载单帧的 RT 矩阵（4x4），RT.json 存储格式为 JSON 格式"""
    with open(rt_json_path, "r") as f:
        rt_data = json.load(f)
    return np.array(rt_data, dtype=np.float64)

def analyze_frame_pair(rt_path1, rt_path2):
    """
    对两个帧的 RT 矩阵计算相对变换，
    返回：(pitch, yaw, roll, overall_rot_angle, translation_diff)
    
    其中：
      - pitch, yaw, roll：在第一帧坐标系中分解的欧拉角（单位：°）
      - overall_rot_angle：通过视线向量计算得到的整体旋转角（单位：°）
      - translation_diff：两个 RT 中平移部分的欧几里得距离（单位：m）
    """
    RT1 = load_rt(rt_path1)
    RT2 = load_rt(rt_path2)
    
    # 求相对变换： T_relative = inv(RT1) * RT2
    T_relative = np.linalg.inv(RT1) @ RT2
    R_rel = T_relative[:3, :3]
    
    # 利用 SciPy 将旋转部分转换为 Euler 角（依次为 x (pitch), y (yaw), z (roll)）
    euler_angles = R.from_matrix(R_rel).as_euler('xyz', degrees=True)
    pitch, yaw, roll = euler_angles

    # 计算“相机视线”之间的夹角作为旋转衡量
    # 将相机坐标系下的光轴 [0, 0, 1] 变换到世界坐标系
    view1 = RT1[:3, :3] @ np.array([0, 0, 1])
    view2 = RT2[:3, :3] @ np.array([0, 0, 1])
    view1 = view1 / np.linalg.norm(view1)
    view2 = view2 / np.linalg.norm(view2)
    dot = np.dot(view1, view2)
    dot = np.clip(dot, -1.0, 1.0)
    view_angle = np.arccos(dot)
    overall_rot_angle = np.degrees(view_angle)

    # 计算两个帧在世界坐标下的相机位置差（平移变化）
    pos1 = RT1[:3, 3]
    pos2 = RT2[:3, 3]
    translation_diff = np.linalg.norm(pos2 - pos1)
    
    return pitch, yaw, roll, overall_rot_angle, translation_diff

def determine_orientation(frame_folder):
    """
    通过读取帧文件夹下的 depth.png 判断拍摄方向。
    如果图像宽 >= 高，则认为是横拍；否则为竖拍。
    """
    depth_img_path = frame_folder / "depth.png"
    if depth_img_path.exists():
        try:
            with Image.open(depth_img_path) as img:
                width, height = img.size  # PIL 返回 (width, height)
            return "horizontal" if width >= height else "vertical"
        except Exception as e:
            print(f"读取 {depth_img_path} 失败，错误信息: {e}. 默认使用 horizontal")
            return "horizontal"
    else:
        print(f"{depth_img_path} 不存在，默认使用 horizontal")
        return "horizontal"

def resize_image(source_path, dest_path, target_size, interpolation=Image.LANCZOS):
    """
    将指定图像 resize 到目标尺寸，并保存到目标路径中。

    参数:
        source_path (str 或 Path): 源图像文件路径。
        dest_path (str 或 Path): 保存 resized 图像的目标路径。
        target_size (tuple): 目标尺寸，格式为 (width, height)。
        interpolation (int): 插值方法，默认使用 Image.LANCZOS。对于 depth 图像建议使用 Image.NEAREST。

    返回:
        bool: 成功返回 True，否则返回 False。
    """
    source = Path(source_path)
    dest = Path(dest_path)
    
    try:
        with Image.open(source) as img:
            resized_img = img.resize(target_size, interpolation)
            resized_img.save(dest)
    except Exception as e:
        print(f"Error processing '{source}': {e}")
        return False
    return True

def process_video_folder(video_folder_path, 
                         default_hor_fov=73.0, default_ver_fov=54.0, diag_fov=84.0, 
                         sampling_gap_min=5, sampling_gap_max=15, sample_step=20,
                         trans_thresh=0.618, fov_scale=0.618):
    """
    对单个视频文件夹进行处理：
      1. 视频文件夹下存在一个子文件夹（非 world.gt）表示帧所在的文件夹，
         如果只有 "world.gt" 则直接跳过。
      2. 对帧文件夹进行字典排序，然后以随机间隔采样帧。
      3. 对于采样得到的每一对帧，计算相对旋转情况（pitch, yaw, roll, 整体旋转角、平移差）。
      4. 如果任一旋转角超过相机视角的 fov_scale 倍（水平、垂直、整体）或平移差超过指定值，
         则认为这对帧的内容关联性较低，舍弃该帧对；否则生成 QA 对。
         
    针对不同拍摄方向（横拍或竖拍），调整水平和垂直的视角阈值：
      - 横拍：水平视角 = default_hor_fov, 垂直视角 = default_ver_fov
      - 竖拍：水平视角 = default_ver_fov, 垂直视角 = default_hor_fov
      
    返回的 QA 对保存在一个列表中，每个元素为一个字典，格式如下：
        {
            "frame1": <第一个帧的 image.png 路径>,
            "frame2": <第二个帧的 image.png 路径>,
            "question": <模板问答>,
            "answer": <答案>,
            "question_type": <"horizontal rotate" 或 "vertical rotate">
        }
    """
    qa_pairs_in_folder = []

    # 查找视频帧所在的子文件夹（跳过 world.gt 文件夹）
    subfolders = [d for d in video_folder_path.iterdir() if d.is_dir() and d.name != "world.gt"]
    if not subfolders:
        print(f"跳过 {video_folder_path}，没有有效的帧文件夹。")
        return qa_pairs_in_folder

    # 通常只有一个视频ID文件夹
    video_frames_dir = subfolders[0]

    # 得到所有帧文件夹，假设名称以 .gt 结尾，按字典序排序
    frame_folders = sorted(
        [d for d in video_frames_dir.iterdir() 
         if d.is_dir() and d.name.endswith('.gt') and d.name != "world.gt"],
        key=lambda x: x.name
    )
    if len(frame_folders) < 2:
        print(f"{video_frames_dir} 中帧文件夹数量不足，跳过。")
        return qa_pairs_in_folder

    # 判断当前视频拍摄方向
    orientation = determine_orientation(frame_folders[0])
    if orientation == "vertical":
        effective_hor_fov = default_ver_fov
        effective_ver_fov = default_hor_fov
    else:
        effective_hor_fov = default_hor_fov
        effective_ver_fov = default_ver_fov

    # print(f"处理视频文件夹: {video_folder_path.name}  (拍摄方向: {orientation})")
    # print(f"帧数量: {len(frame_folders)}")
    # print(f"有效水平FOV: {effective_hor_fov}°, 有效垂直FOV: {effective_ver_fov}°, 对角线FOV: {diag_fov}°")

    # 阈值设定：旋转角度按相机视角的 fov_scale 倍计算
    hor_thresh = fov_scale * effective_hor_fov   # 左右旋转阈值
    ver_thresh = fov_scale * effective_ver_fov       # 上下旋转阈值
    diag_thresh = fov_scale * diag_fov              # 整体旋转阈值

    index = 0
    pair_idx = 0
    # 采样：每次先随机间隔 gap 帧，再额外跳过 sample_step 帧
    while index < len(frame_folders) - 1:
        gap = random.randint(sampling_gap_min, sampling_gap_max)
        next_index = index + gap
        if next_index >= len(frame_folders):
            break

        # 获取两帧对应的 RT.json 文件
        rt_path1 = frame_folders[index] / "RT.json"
        rt_path2 = frame_folders[next_index] / "RT.json"

        if not (rt_path1.exists() and rt_path2.exists()):
            print(f"帧 {frame_folders[index].name} 或 {frame_folders[next_index].name} 中没有 RT.json，跳过这对。")
            index = next_index
            continue

        pitch, yaw, roll, overall_angle, translation_diff = analyze_frame_pair(rt_path1, rt_path2)
        pair_idx += 1
        # print(f"\n帧对 {pair_idx}: {frame_folders[index].name}  ->  {frame_folders[next_index].name}")
        # print(f"  计算结果: yaw={yaw:.2f}°, pitch={pitch:.2f}°, overall旋转={overall_angle:.2f}°, 平移差={translation_diff:.2f} m")

        # 判断是否超过阈值，若超过则舍弃
        invalid = (abs(yaw) > hor_thresh or 
                   abs(pitch) > ver_thresh or 
                   overall_angle > diag_thresh or 
                   translation_diff > trans_thresh)
        if invalid:
            # print("  → 该帧对不满足关联条件（超出阈值），舍弃。")
            index = next_index
            continue
        else:
            # 构造 .wide 目录下对应的文件路径（将 .gt 文件夹转换为 .wide 文件夹）
            frame1_wide_path = frame_folders[index].with_suffix(".wide")
            frame1_wide_image_path = str(frame1_wide_path / "image.png")
            frame1_wide_depth_path = str(frame1_wide_path / "depth.png")
            frame1_gt_depth_path = str(frame_folders[index] / "depth.png")
            
            frame2_wide_path = frame_folders[next_index].with_suffix(".wide")
            frame2_wide_image_path = str(frame2_wide_path / "image.png")
            frame2_wide_depth_path = str(frame2_wide_path / "depth.png")
            frame2_gt_depth_path = str(frame_folders[next_index] / "depth.png")

            # 获取目标尺寸：以 ground truth depth 图像的尺寸为准
            try:
                with Image.open(frame1_gt_depth_path) as gt_img:
                    target_size_frame1 = gt_img.size  # (width, height)
            except Exception as e:
                print(f"Error opening frame1 ground truth depth image {frame1_gt_depth_path}: {e}")
                index = next_index + sample_step
                continue  # 跳过本次循环

            try:
                with Image.open(frame2_gt_depth_path) as gt_img:
                    target_size_frame2 = gt_img.size  # (width, height)
            except Exception as e:
                print(f"Error opening frame2 ground truth depth image {frame2_gt_depth_path}: {e}")
                index = next_index + sample_step
                continue

            # 构造保存 resized 文件的目标路径
            frame1_wide_resized_image_path = str(frame1_wide_path / "image_resized.png")
            frame1_wide_resized_depth_path = str(frame1_wide_path / "depth_resized.png")
            frame2_wide_resized_image_path = str(frame2_wide_path / "image_resized.png")
            frame2_wide_resized_depth_path = str(frame2_wide_path / "depth_resized.png")

            resize_image(frame1_wide_image_path, frame1_wide_resized_image_path, target_size_frame1, interpolation=Image.LANCZOS)
            resize_image(frame2_wide_image_path, frame2_wide_resized_image_path, target_size_frame2, interpolation=Image.LANCZOS)
            resize_image(frame1_wide_depth_path, frame1_wide_resized_depth_path, target_size_frame1, interpolation=Image.NEAREST)
            resize_image(frame2_wide_depth_path, frame2_wide_resized_depth_path, target_size_frame2, interpolation=Image.NEAREST)

            # 当 yaw 绝对角度大于 6.18° 时生成左右问答
            if abs(yaw) > 6.18:
                question_horizontal, answer_horizontal = generate_lr_question(yaw)
                qa_dict = {
                    "frame1_image": frame1_wide_resized_image_path,
                    "frame2_image": frame2_wide_resized_image_path,
                    "frame1_depth": frame1_wide_resized_depth_path,
                    "frame2_depth": frame2_wide_resized_depth_path,
                    "question": question_horizontal,
                    "answer": answer_horizontal,
                    "question_type": "horizontal rotate"
                }
                qa_pairs_in_folder.append(qa_dict)
            
            # 当 pitch 绝对角度大于 6.18° 时生成上下问答
            if abs(pitch) > 6.18:
                question_vertical , answer_vertical = generate_ud_question(pitch)
                qa_dict = {
                    "frame1_image": frame1_wide_resized_image_path,
                    "frame2_image": frame2_wide_resized_image_path,
                    "frame1_depth": frame1_wide_resized_depth_path,
                    "frame2_depth": frame2_wide_resized_depth_path,
                    "question": question_vertical,
                    "answer": answer_vertical,
                    "question_type": "vertical rotate"
                }
                qa_pairs_in_folder.append(qa_dict)

            index = next_index + sample_step  # 按采样策略跳过更多帧

    return qa_pairs_in_folder

# 工作进程函数：从任务队列中取视频文件夹进行处理，将处理结果放到结果队列中
def worker(task_queue, result_queue):
    while True:
        video_folder = task_queue.get()
        if video_folder is None:  # 收到哨兵任务，退出
            break
        qa_pairs = process_video_folder(video_folder)
        result_queue.put(qa_pairs)

def main():
    # 数据根目录，请根据实际情况修改路径
    train_root = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/train")
    # 输出文件路径（全部结果保存在同一个文件中，采用 JSON 格式）
    output_file = Path("/home_sfs/zhouenshen/dataset/3D/cubifyanything/multi_view_qa.json")
    # 清空输出文件（若已存在）
    with open(output_file, "w", encoding="utf-8") as f:
        pass

    video_folders = [d for d in train_root.iterdir() if d.is_dir()]
    num_tasks = len(video_folders)
    if num_tasks == 0:
        print("没有找到视频文件夹。")
        return

    task_queue = mp.Queue()
    result_queue = mp.Queue()

    # 将视频文件夹任务放入任务队列
    for folder in video_folders:
        task_queue.put(folder)
    # 添加哨兵任务，每个工作进程收到哨兵后退出
    num_workers = mp.cpu_count()
    for _ in range(num_workers):
        task_queue.put(None)

    # 创建工作进程
    processes = []
    for _ in range(num_workers):
        p = mp.Process(target=worker, args=(task_queue, result_queue))
        p.start()
        processes.append(p)

    flush_threshold = 10  # 每从结果队列中累计得到 10 次任务结果后保存一次
    results = []
    results_received = 0

    # 初始化进度条，总任务数为 num_tasks
    pbar = tqdm.tqdm(total=num_tasks, desc="Collecting QA results")


    # 主进程从结果队列中收集任务结果（知道收到的任务数等于总任务数）
    for _ in range(num_tasks):
        qa_pairs = result_queue.get()  # 每个任务结果是一个 QA 对列表
        results.extend(qa_pairs)
        results_received += 1
        pbar.update(1)

        # 当累计达到 flush_threshold，则写入文件
        if results_received % flush_threshold == 0:
            with open(output_file, "w", encoding="utf-8") as f_out:
                json.dump(results, f_out, indent=4)

    pbar.close()

    # 将所有结果写入文件
    if results:
        with open(output_file, "w", encoding="utf-8") as f_out:
            json.dump(results, f_out, indent=4)

    # 等待所有工作进程结束
    for p in processes:
        p.join()

    print(f"共生成 {len(results)}个QA 对并已保存到 {output_file}")

if __name__ == "__main__":
    random.seed(42)
    main()