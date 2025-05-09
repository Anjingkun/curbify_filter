import os
import json
from collections import defaultdict
import multiprocessing
from tqdm import tqdm

# --- Configuration for file types/sources ---
FILTER_STEP_20_JSON_FILENAMES = [
    "choice_qa.json",
    "template_qa_only_point.json",
    "template_qa.json",
    "visual_choice.json",
    "vacant_qa.json"
]

# --- Worker function for file DISCOVERY phase ---
def discover_files_in_video_dir_task(task_args):
    video_dir_path, json_filenames_to_check = task_args
    found_files_in_this_video_dir = []
    try:
        for frame_id_dir in os.listdir(video_dir_path):
            frame_path = os.path.join(video_dir_path, frame_id_dir)
            if not os.path.isdir(frame_path):
                continue
            for json_filename in json_filenames_to_check:
                file_path = os.path.join(frame_path, json_filename)
                if os.path.exists(file_path):
                    found_files_in_this_video_dir.append((file_path, json_filename))
    except Exception:
        pass 
    return found_files_in_this_video_dir

# --- Updated discover_files function ---
def discover_files(filter_step_20_base_path):
    all_files_to_process_with_tags = []
    if not os.path.exists(filter_step_20_base_path):
        print(f"Path not found, skipping discovery: {filter_step_20_base_path}")
        return all_files_to_process_with_tags

    print(f"Starting file discovery in: {filter_step_20_base_path}...")
    video_id_dirs = []
    for item_name in os.listdir(filter_step_20_base_path):
        item_path = os.path.join(filter_step_20_base_path, item_name)
        if os.path.isdir(item_path):
            video_id_dirs.append(item_path)

    if not video_id_dirs:
        print("No video directories found.")
        return all_files_to_process_with_tags

    discovery_tasks = [(video_dir_path, FILTER_STEP_20_JSON_FILENAMES) for video_dir_path in video_id_dirs]
    num_discovery_processes = os.cpu_count() if os.cpu_count() else 1
    num_discovery_processes = min(num_discovery_processes, len(discovery_tasks))
    if num_discovery_processes == 0 and len(discovery_tasks) > 0:
        num_discovery_processes = 1
    
    if discovery_tasks:
        print(f"Scanning {len(discovery_tasks)} video directories with {num_discovery_processes} processes...")
        with multiprocessing.Pool(processes=num_discovery_processes) as pool:
            results_iterator = pool.imap_unordered(discover_files_in_video_dir_task, discovery_tasks)
            for list_of_found_files in tqdm(results_iterator, total=len(discovery_tasks), desc="Discovering files"):
                all_files_to_process_with_tags.extend(list_of_found_files)
    
    print(f"Total files discovered for processing: {len(all_files_to_process_with_tags)}")
    return all_files_to_process_with_tags

# --- Worker function for file PROCESSING phase ---
def process_single_file(file_path, file_type_tag):
    local_qa_function_counts = defaultdict(int)
    granular_counts_for_this_file_type = defaultdict(int)
    items_in_this_file = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        qa_pairs = data.get("qa_pairs", [])
        items_in_this_file = len(qa_pairs)
        granular_counts_for_this_file_type[file_type_tag] = items_in_this_file
        for qa_item in qa_pairs:
            if qa_item is None: continue
            qa_func = qa_item.get("qa_function")
            if qa_func:
                local_qa_function_counts[qa_func] += 1
    except json.JSONDecodeError:
        pass
    except Exception:
        pass
    return local_qa_function_counts, granular_counts_for_this_file_type, items_in_this_file

# Helper function to unpack arguments for starmap-like behavior with imap for PROCESSING
def starmap_process_single_file_wrapper(args_tuple):
    return process_single_file(*args_tuple)

# --- Main execution ---
def main():
    # Updated data structure for qa_function counts
    agg_qa_function_by_filetype_counts = defaultdict(lambda: defaultdict(int))
    
    agg_granular_qa_counts = defaultdict(int) 
    agg_total_qa_items = 0

    filter_step_20_base_path = "/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20"

    files_to_process = discover_files(filter_step_20_base_path)

    if not files_to_process:
        print("No files found to process. Exiting.")
        return

    num_processing_processes = os.cpu_count() if os.cpu_count() else 1
    num_processing_processes = min(num_processing_processes, len(files_to_process))
    if num_processing_processes == 0 and len(files_to_process) > 0:
        num_processing_processes = 1
    
    if files_to_process:
        print(f"\nStarting processing of {len(files_to_process)} files with {num_processing_processes} processes...")
        with multiprocessing.Pool(processes=num_processing_processes) as pool:
            results_iterator = pool.imap_unordered(starmap_process_single_file_wrapper, files_to_process)
            
            for res_qa_func_counts_this_file, res_granular_map_this_file, res_total_items_this_file in tqdm(results_iterator, total=len(files_to_process), desc="Processing files"):
                
                # Get the file_type_tag for the current file's results
                current_file_type_tag = None
                if res_granular_map_this_file: # Should contain one key: the file_type_tag
                    current_file_type_tag = list(res_granular_map_this_file.keys())[0]

                if current_file_type_tag:
                    for qa_f, count_in_file in res_qa_func_counts_this_file.items():
                        agg_qa_function_by_filetype_counts[qa_f][current_file_type_tag] += count_in_file
                
                # Aggregate granular counts (total items per file type)
                for tag, count in res_granular_map_this_file.items():
                    agg_granular_qa_counts[tag] += count
                
                agg_total_qa_items += res_total_items_this_file
        print("All file processing finished.")
    else:
        print("No files were queued for processing.")

    # --- Print Results ---
    print("\n--- Aggregated Statistics (filter_step_20 only) ---")

    print("\nTotal QA Items per JSON File Type:")
    if agg_granular_qa_counts:
        for file_type, count in sorted(agg_granular_qa_counts.items()):
            print(f"  {file_type}: {count} QA items")
    else:
        print("  No QA items found for the specified JSON file types.")

    print("\nCategory: qa_function Counts (broken down by JSON file type):")
    if agg_qa_function_by_filetype_counts:
        for qa_func, filetype_counts in sorted(agg_qa_function_by_filetype_counts.items()):
            print(f"\nqa_function: '{qa_func}'")
            total_for_this_qafunc = 0
            for file_type, count in sorted(filetype_counts.items()):
                print(f"  - {file_type}: {count}")
                total_for_this_qafunc += count
            print(f"  (Total for '{qa_func}': {total_for_this_qafunc})")
    else:
        print("  No qa_function data found.")
        
    print(f"\nOverall Total QA items processed from these files: {agg_total_qa_items}")

if __name__ == "__main__":
    multiprocessing.freeze_support() 
    main()