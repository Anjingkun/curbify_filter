import imageio
import cv2
import numpy as np
from PIL import Image

wide_depth_path = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20/42444499/2458914221666/wide/depth_normalized.png"

image_depth = cv2.imread(wide_depth_path)

import ipdb; ipdb.set_trace()
# # 读取深度图像
# image_depth = imageio.v2.imread(wide_depth_path).astype(np.float32) / 1000.0  # 毫米转米

# # 对这个image_depth变成相对深度然后保存
# # 计算有效深度值（非零值）的最小值和最大值
# valid_depth = image_depth[image_depth > 0]
# if len(valid_depth) > 0:
#     min_depth = np.min(valid_depth)
#     max_depth = np.max(valid_depth)
    
#     # 归一化到0-1范围
#     normalized_depth = np.zeros_like(image_depth)
#     mask = image_depth > 0
#     normalized_depth[mask] = (image_depth[mask] - min_depth) / (max_depth - min_depth)
    
#     # 转换为可视化图像（0-255范围）
#     depth_vis = (normalized_depth * 255).astype(np.uint8)
    
#     # 应用伪彩色映射以便更好地可视化
#     depth_colormap = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
    
#     # 保存结果
#     output_path = wide_depth_path.replace("depth_resized.png", "depth_normalized_2.png")
#     cv2.imwrite(output_path, depth_vis)
    
#     # 保存彩色版本
#     output_color_path = wide_depth_path.replace("depth_resized.png", "depth_colormap_2.png")
#     cv2.imwrite(output_color_path, depth_colormap)
    
#     print(f"原始深度范围: {min_depth:.2f}m - {max_depth:.2f}m")
#     print(f"归一化深度图已保存至: {output_path}")
#     print(f"彩色深度图已保存至: {output_color_path}")
# else:
#     print("深度图中没有有效值")



