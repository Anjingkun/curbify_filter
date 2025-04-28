#!/usr/bin/env python3
import os
from pathlib import Path
import imageio
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# —— 根据需要修改
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

def find_all_frame_dirs(root_path: str) -> list[str]:
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")
    # video_id/frame_id 形式的目录
    dirs = [p for p in root.glob("*/*") if p.is_dir()]
    print(f"🔍 Found {len(dirs)} frame folders under {root}")
    return [str(p) for p in dirs]

def process_frame(frame_dir: str) -> None:
    try:
        wide_dir = Path(frame_dir) / "wide"
        depth_path = wide_dir / "depth_resized.png"
        if not depth_path.exists():
            print(f"❌ {depth_path} does not exist. Skipping.")
            return

        # 1) 读取
        img = imageio.v2.imread(depth_path)
        # 2) 如果是彩色图，先转灰度
        if img.ndim == 3:
            # 简单加权转换
            img = (0.2989 * img[...,0] + 0.5870 * img[...,1] + 0.1140 * img[...,2]).astype(np.float32)
        else:
            img = img.astype(np.float32)

        # 3) 根据读入的位深度决定是否转米
        #    常见：uint16 存的是毫米 -> 除 1000 得到米
        if img.dtype == np.float32 and img.max() > 1000:
            # 读出的 float32 可能也是 mm
            depth_m = img / 1000.0
        elif img.dtype == np.uint16 or img.max() > 255:
            depth_m = img / 1000.0
        else:
            # 已经是 [0,255]，先归一到 [0,1]
            depth_m = img / 255.0

        # 4) 归一化到 [0,1]
        d_min, d_max = float(depth_m.min()), float(depth_m.max())
        if abs(d_max - d_min) < 1e-8:
            norm = np.zeros_like(depth_m, dtype=np.uint8)
        else:
            norm = ( (d_max - depth_m) / (d_max - d_min) * 255.0 ).clip(0,255).astype(np.uint8)

        # 5) 拓展到 3 通道
        depth_rgb = np.repeat(norm[..., np.newaxis], 3, axis=-1)

        # 6) 保存
        out_path = wide_dir / "depth_normalized.png"
        imageio.v2.imwrite(str(out_path), depth_rgb)

    except Exception as e:
        print(f"⚠️ Error processing {frame_dir}: {e}")

if __name__ == "__main__":
    frames = find_all_frame_dirs(ROOT_DIR)
    with Pool(cpu_count()) as pool:
        list(tqdm(pool.imap(process_frame, frames), total=len(frames)))
    print("🎉 Batch processing completed!")