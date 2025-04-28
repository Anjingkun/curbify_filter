# 验证 gt depth中是否存在none
import cv2
import numpy as np
import os

def check_depth_image(depth_path):
    if not os.path.exists(depth_path):
        print(f"❌ 文件不存在: {depth_path}")
        return

    # 以原始深度格式读取（保持float或16位）
    depth = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)

    if depth is None:
        print("❌ 无法读取图像，可能格式不支持或路径错误")
        return

    print(f"✅ 图像读取成功，shape: {depth.shape}, dtype: {depth.dtype}")

    # 转为 float32 以便检查 NaN 和 inf
    depth = depth.astype(np.float32)

    nan_mask = np.isnan(depth)
    inf_mask = np.isinf(depth)
    zero_mask = depth == 0
    neg_mask = depth < 0

    total_pixels = depth.size

    print(f"总像素数: {total_pixels}")
    print(f"NaN 像素数: {np.sum(nan_mask)}")
    print(f"Inf 像素数: {np.sum(inf_mask)}")
    print(f"Zero 像素数: {np.sum(zero_mask)}")
    print(f"Negative 像素数: {np.sum(neg_mask)}")

    if np.any(nan_mask | inf_mask | neg_mask):
        print("⚠️ 警告：深度图中存在非法值！")
    else:
        print("✅ 深度图中没有发现 NaN / Inf / 负值")

# 用法示例
depth_image_path = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20/42444499/2458914221666/wide/depth.png"
check_depth_image(depth_image_path)