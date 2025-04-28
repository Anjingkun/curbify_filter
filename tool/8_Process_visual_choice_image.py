import shutil
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# 请替换为你实际的根目录路径
ROOT_DIR = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

def find_all_frame_dirs(root_path: str) -> list[str]:
    """
    自动扫描 root_path 下所有形如 video_id/frame_id 的帧目录
    """
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")
    
    # glob("*/*") 匹配的是两层文件夹，即 video_id/frame_id
    candidate_dirs = [p.resolve() for p in root.glob("*/*") if p.is_dir()]
    print(f"🔍 Found {len(candidate_dirs)} frame folders under {root}")
    return [str(p) for p in candidate_dirs]

def process_frame_dir(frame_dir: str, dest_dir: Path):
    """
    对每个帧文件夹，复制并重命名 image_with_bbox 和 image_with_points 下的图片
    """
    frame_path = Path(frame_dir)
    # video_id 为该帧目录的上一级文件夹名称
    video_id = frame_path.parent.name  
    # frame_id 为该帧目录的名称
    frame_id = frame_path.name         

    # 需处理的子文件夹名称
    subfolders = ["image_with_bbox", "image_with_points"]

    for subfolder in subfolders:
        folder = frame_path / subfolder
        if not folder.exists() or not folder.is_dir():
            print(f"Warning: 文件夹 {folder} 不存在或不是文件夹。")
            continue
        
        # 遍历文件夹下所有 png 图片，按照数字顺序（假设图片名为 0.png、1.png...）
        for file in sorted(folder.glob("*.png"), key=lambda x: int(x.stem) if x.stem.isdigit() else x.stem):
            # 构造新的文件名，例如 "video1_frame10_image_with_bbox_0.png"
            new_filename = f"{video_id}_{frame_id}_{subfolder}_{file.stem}.png"
            dest_file = dest_dir / new_filename
            try:
                shutil.copy2(file, dest_file)
            except Exception as e:
                print(f"Error copying {file} to {dest_file}: {e}")

def main():
    # 扫描所有帧目录
    frame_dirs = find_all_frame_dirs(ROOT_DIR)
    
    # 构建输出目录：与 ROOT_DIR 平级下的 visual_choice_images 文件夹
    dest_dir = Path(ROOT_DIR).parent / "visual_choice_qa_images_v2"
    dest_dir.mkdir(parents=True, exist_ok=True)
    print(f"Destination directory is: {dest_dir}")
    
    # 【选项 A】顺序方式处理，使用 tqdm 显示进度条
    # for frame_dir in tqdm(frame_dirs, desc="Processing frames"):
    #     process_frame_dir(frame_dir, dest_dir)
    
    # 【选项 B】使用多进程加速（当帧目录较多时可以启用）
    # 注意：多进程复制 IO 密集型任务收益不一定显著，可视实际情况启用
    with Pool(cpu_count()) as pool:
        pool.starmap(process_frame_dir, [(frame_dir, dest_dir) for frame_dir in frame_dirs])
    
    print("✅ 所有图片已成功复制并重命名。")

if __name__ == "__main__":
    main()