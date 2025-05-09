import os
import json
from collections import defaultdict
import multiprocessing
from tqdm import tqdm

# 这是一个通用的标签，因为我们是对llm_qa下所有文件内容做聚合统计
LLM_QA_FILE_TAG = "llm_qa_file_content" 

# Worker function to process a single LLM QA JSON file
def process_llm_qa_file(file_path, file_tag_placeholder): # file_tag_placeholder 在此场景下主要用于保持接口一致性
    """
    Processes a single JSON file from the llm_qa set.
    Returns:
        - local_question_type_counts: dict of question_type counts from this file.
        - items_processed_in_file: total llm_prompts + conversations items in this file.
    """
    local_question_type_counts = defaultdict(int)
    items_processed_in_file = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Process conversations
        conversations = data.get("conversations", [])
        items_processed_in_file += len(conversations)
        for conv in conversations:
            if conv is None: 
                continue
            # 假设 'conversations' 条目也包含 'question_type' 和 'function_name'
            # 根据您之前提供的结构，这里也应该有 question_type
            q_type = conv.get("function_name") 
            if q_type:
                local_question_type_counts[q_type] += 1
                
    except json.JSONDecodeError:
        # print(f"Worker: Error decoding JSON in {file_path}") 
        # 在使用tqdm时，worker进程中的print可能会打乱进度条，建议使用日志或保持静默
        pass 
    except Exception as e:
        # print(f"Worker: Error processing file {file_path}: {e}")
        pass

    return (
        local_question_type_counts,
        items_processed_in_file
    )

def discover_llm_qa_files(llm_qa_base_path):
    files_to_process_with_tags = [] # List of (file_path, tag)

    if not os.path.exists(llm_qa_base_path):
        print(f"Path not found, skipping discovery: {llm_qa_base_path}")
        return files_to_process_with_tags

    print(f"Discovering files in: {llm_qa_base_path}...")
    discovered_count = 0
    # 遍历 0-7 这些分组文件夹
    for group_dir_name in os.listdir(llm_qa_base_path): 
        group_path = os.path.join(llm_qa_base_path, group_dir_name)
        if not os.path.isdir(group_path):
            continue
        # 遍历视频文件夹
        for video_id_dir_name in os.listdir(group_path):
            video_path = os.path.join(group_path, video_id_dir_name)
            if not os.path.isdir(video_path):
                continue
            # 遍历json文件
            for json_filename in os.listdir(video_path):
                if json_filename.endswith(".json"):
                    file_path = os.path.join(video_path, json_filename)
                    # 所有来自 llm_qa 的文件使用同一个标签
                    files_to_process_with_tags.append((file_path, LLM_QA_FILE_TAG))
                    discovered_count +=1
    
    print(f"Total LLM QA JSON files discovered for processing: {discovered_count}")
    return files_to_process_with_tags

# Helper function to unpack arguments for starmap-like behavior with imap
def starmap_worker_wrapper(args_tuple):
    # This now calls the llm_qa specific worker
    return process_llm_qa_file(*args_tuple) 

def main():
    agg_question_type_counts = defaultdict(int)
    agg_total_qa_items = 0 # 总的 "llm_prompts" 和 "conversations" 条目数

    llm_qa_base_path = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/llm_qa"

    # 仅发现 llm_qa 下的文件
    files_to_process = discover_llm_qa_files(llm_qa_base_path)

    if not files_to_process:
        print("No LLM QA files found to process. Exiting.")
        return

    num_processes = os.cpu_count() if os.cpu_count() else 1
    num_processes = min(num_processes, len(files_to_process))
    if num_processes == 0 and len(files_to_process) > 0: # 保证至少有1个进程（如果文件存在）
        num_processes = 1
    
    if files_to_process:
        print(f"\nStarting processing of {len(files_to_process)} LLM QA files with {num_processes} processes...")
        with multiprocessing.Pool(processes=num_processes) as pool:
            # 使用 imap_unordered 以便在结果可用时立即处理，并配合tqdm显示进度
            results_iterator = pool.imap_unordered(starmap_worker_wrapper, files_to_process)
            
            # 用 tqdm 包装迭代器以显示进度条
            for local_q_type_counts, items_from_file in tqdm(results_iterator, total=len(files_to_process), desc="Processing LLM QA files"):
                for q_type, count in local_q_type_counts.items():
                    agg_question_type_counts[q_type] += count
                agg_total_qa_items += items_from_file
        print("All file processing finished.")
    else:
        print("No LLM QA files were queued for processing.")

    # --- 打印结果 ---
    print("\n--- Aggregated Statistics (llm_qa only) ---")

    print("\nCategory: question_type Counts:")
    if agg_question_type_counts:
        for q_type, count in sorted(agg_question_type_counts.items()):
            print(f"  {q_type}: {count}")
    else:
        print("  No question_type data found.")
        
    print(f"\nOverall Total items (llm_prompts + conversations) processed from llm_qa files: {agg_total_qa_items}")

if __name__ == "__main__":
    # 这对于某些操作系统（如Windows）上的多处理正常工作很重要
    multiprocessing.freeze_support() 
    main()