import argparse
import time
import warnings

import glob
from pathlib import Path
import os
import tqdm
import multiprocessing
import random
import json
def find_all_frame_dirs(root_path: str, num_workers: int = None) -> list[str]:
    """
    多进程查找所有包含目标 JSON 的帧目录。
    假设结构为 root/video_id/frame_id。
    """
    root = Path(root_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root_path}")

    # 查找所有两级目录：video_id/frame_id
    candidate_frame_dirs = [
        str(p.resolve()) for p in root.glob("*/*")
        if p.is_dir()
    ]

    print(f"🔍 Found {len(candidate_frame_dirs)} frame folders.")
    return candidate_frame_dirs

# Suppressing all warnings
warnings.filterwarnings("ignore")

def is_json_invalid(json_file):
    try:
        with open(json_file, "r") as f:
            json.load(f)
        return json_file, True  # 有效
    except Exception:
        return json_file, False   # 损坏

def delete_invalid_jsons(folder_path, num_workers=8):
    print(f"正在扫描目录：{folder_path}\n")
    folder_path = Path(folder_path)

    # 获取所有子文件夹下的 JSON（递归查找 *.json）
    all_json_files = sorted(folder_path.glob("*/*.json"), key=lambda f: f.stat().st_ctime, reverse=True)

    print(f"发现 {len(all_json_files)} 个 JSON 文件，开始校验...\n")

    with multiprocessing.Pool(num_workers) as pool:
        results = list(tqdm.tqdm(pool.imap_unordered(is_json_invalid, all_json_files), total=len(all_json_files)))

    # 统计结果
    valid_files = [f for f, valid in results if valid]
    invalid_files = [f for f, valid in results if not valid]

    print(f"\n总文件数: {len(all_json_files)}")
    print(f"有效 JSON: {len(valid_files)}")
    print(f"\n共找到 {len(invalid_files)} 个损坏 JSON 文件，开始删除...\n")

    for f in invalid_files:
        try:
            f.unlink()
            print(f"Deleted: {f}")
        except Exception as e:
            print(f"Failed to delete {f}: {e}")

def process_facts(task_queue, result_queue, device, model_path, base_port, this_machine_llm_qa_dir):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
    import re
    from sglang import function, system, gen, set_default_backend, RuntimeEndpoint
    from sglang.utils import (
        execute_shell_command,
        wait_for_server,
    )
    response_regex = r"\{" + r'    "Question": "[\w\d\s<>?,.!]{1,512}",' + r'    "Answer": "[\w\d\s<>?,.!]{1,512}"' + r"\}"
    @function
    def rephrase_qa(s, question_1):
        s += system(
            r"""
                    You are a helpful assistant tasked with generating spatial reasoning-based questions and answers from provided descriptions of scenes.

                    Rules:
                    1. **We have three types of input information**:
                    - **[Scene]**: A general description of the entire image, which provides context for the objects and their surroundings.  
                        **Example:**  
                        ```
                        [Scene]: The image shows a tranquil lakeside with a small wooden dock on the right and calm, reflective water in the center. The sky is overcast.
                        ```
                    - **[Objects]**: A list containing one or more object labels separated by "|".  
                        **Example:**  
                        ```
                        [Objects]: teal glossy water at lower center | green bamboo dock at lower right.
                        ```
                    - **[Objects Description]**: Provides spatial or comparative details between those objects. And it may also obtain information about the spatial ordering of objects (e.g., "which is the first water from the left", "the third  bamboo from the bottom").
                        **Example:**  
                        ```
                        [Objects Description]: teal glossy water at lower center is taller than green bamboo dock at lower right.
                        [Objects Description]: teal glossy water at lower center, which is the first water from the left, is taller than green bamboo dock at lower right, the third bamboo from the bottom.
                        ```

                    2. **When crafting a Question**:
                    - **Always use the provided [Scene] description as context** to ensure the question aligns with the overall image.  
                    - **Mention all object labels from [Objects]** in the question.  
                    - **You'd better to use the information about the spatial ordering of objects in the `[Objects Description]`**.
                    - **Do not modify or paraphrase the object labels**; they must appear **exactly** as given in `[Objects]`.
                    - **Do not assume or invent additional scene details** beyond what is provided in `[Scene]`.  
                    - **Do not reveal the specific details in [Objects Description]** (like which object is taller, shorter, wider, etc.).
                    - Always generate questions related to the description using the object labels from [Objects].  
                    - Each object label in `[Objects]` **must appear exactly once** in the Question.  
                    - The question should read from **an observer's perspective**.
                    - The description should always be used to answer and not leak into the question. 

                    3. **When crafting an Answer**:
                    - **Mention at least one object label from [Objects]** in the answer.  
                    - Use the `[Objects Description]` to provide a correct answer.  
                    - Ensure the answer is concise, factual, and directly related to the provided `[Scene]` and `[Objects]`.  
                    - You may restate or summarize the relevant details from `[Objects Description]`, but do not introduce new assumptions.  


                    Here's several examples:

                    [Scene]: The image depicts a modern living room with a large window allowing warm sunlight to enter. The room has a wooden floor, a patterned rug in the center, and a coffee table with a few magazines neatly stacked on it. A yellow leather sofa is positioned centrally, facing the television mounted on the opposite wall. To the left of the sofa, a black metal chair with a cushioned seat is placed beside a tall bookshelf filled with an assortment of books and decorative items. The furniture arrangement leaves an open pathway between the sofa and the chair.
                    [Objects]: yellow leather sofa at lower center | black metal chair on the left. 
                    [Objects Description]: The distance between yellow leather sofa at lower center, which is the first sofa from the bottom, and black metal chair on the left, which is the second chair from the left, is 1.5 meters.
                    "Question": You are a cleaning robot that is 1 meter wide. Now you are standing in a living room and see the image; you want to move from here to the door that leads to the backyard. Do you think you can go through the path between the yellow leather sofa at lower center , which is the first sofa from the bottom, and the black metal chair on the left, which is the second chair from the left? 
                    "Answer": The path between the yellow leather sofa at lower center and the black metal chair on the left is 1.5 meters, so yes, the robot can go through the path between the yellow leather sofa at lower center and the black metal chair on the left since it is wider than the robot's width.

                    [Scene]: The image showcases a modern kitchen with a wooden countertop that extends across the space, separating the cooking area from the dining area. On the left side of the countertop, a fruit bowl holds a variety of fresh produce. A red fresh apple is placed on the left side of the bowl, while a bright fresh orange sits neatly on the right side. Behind the fruit bowl, a glass pitcher filled with orange juice and a stack of white ceramic plates are visible. Natural light streams in from a large window above the sink, reflecting off the stainless steel appliances and giving the space a bright, clean feel.
                    [Objects]: red fresh apple on the left | fresh orange on the right. 
                    [Objects Description]: red fresh apple on the left is positioned on the left side of fresh orange on the right, the second orange from the right.
                    "Question": You see two fruits, a red fresh apple on the left and a fresh orange on the right, the second orange from the right. Which one is more on the left side? 
                    "Answer": The red fresh apple on the left is more on the left.

                    [Scene]: The image features a neatly arranged bedroom with soft pastel tones. The floor is covered with a plush beige carpet, and a small nightstand sits beside a pink wooden bed in the middle of the room. The bed has a neatly folded blanket at the foot, and a few decorative pillows are arranged against the headboard. To the right of the bed, a white wooden desk is positioned against the wall, with a small desk lamp and an open notebook resting on its surface. A window with semi-transparent curtains allows natural daylight to cast a soft glow over the room.
                    [Objects]: white wooden desk on the right | pink wooden bed in the middle. 
                    [Objects Description]: white wooden desk on the right, arranged as the first desk from the front to the back, is further to the viewer than pink wooden bed in the middle.
                    "Question": You are exploring a bedroom and walking towards the white wooden desk on the right, arranged as the first desk from the front to the back, and the pink wooden bed in the middle. Which one will you reach first? 
                    "Answer": You will reach the pink wooden bed in the middle first because it is closer to you than the white wooden desk on the right, arranged as the first desk from the front to the back, which is further away.

                    [Scene]: The image captures a quiet reading nook within a library. Rows of wooden bookshelves filled with books of various sizes and colors stretch across the background. A wooden table with a green reading lamp sits in the center, accompanied by a few cushioned chairs. On the upper right shelf, a brown book stands slightly out of alignment with the others. Nearby, a librarian’s cart with neatly stacked books waits to be reshelved. Soft lighting from hanging lamps and large windows creates a peaceful atmosphere, inviting readers to immerse themselves in their books.
                    [Objects]: brown book at upper right. 
                    [Objects Description]: brown book at upper right, placed as the second book from the right, is 50 cm in width.
                    "Question": You are a librarian currently standing in front of a 40 cm width bookshelf, and you see the brown book at upper right, placed as the second book from the right, and you want to place it on the shelf. Can you determine if the brown book at upper right will fit on the shelf?
                    "Answer":  The brown book at upper right, placed as the second book from the right, is 50 cm in width, so the shelf is not wide enough to hold a book of that size. Please find a larger shelf.

                    Now its your turn!

    """
        )
        s += question_1
        s += gen("json_output", max_tokens=1024, regex=response_regex)
    def extract_point(s):
        match = re.search(r"\(([^)]+)\)", s)
        return match.group(1).strip() if match else s.strip()
    def process_prompt(llm_prompt, image_caption, rephrase_qa, max_retries=3):
        prompt = llm_prompt["instruction"]
        object_A_name = llm_prompt["object_A_name"]
        object_B_name = llm_prompt["object_B_name"]
        object_C_name = llm_prompt["object_C_name"]
        question_type = llm_prompt["question_type"]
        instruction = f"[Scene]: {image_caption}. {prompt.replace('[Description]', '[Objects Description]')}"
        for attempt in range(max_retries):
            try:
                llama_response = rephrase_qa.run(instruction, temperature=0.2)
                response_string = llama_response["json_output"]

                # Clean and parse the response
                cleaned_string = response_string.strip()
                cleaned_string = "".join(char for char in cleaned_string if ord(char) >= 32 or char == "\n")
                cleaned_string = re.sub(r"\s+", " ", cleaned_string)
                cleaned_string = cleaned_string.replace("'", '"')
                json_response = json.loads(cleaned_string)

                question, answer = json_response["Question"], json_response["Answer"]

                # Cleanup question/answer
                question = question[2:] if question and question[:2] == ". " else question
                answer = answer[2:] if answer and answer[:2] == ". " else answer

                # Validate region tags
                if question_type == "one_object_fact":
                    if "point" in object_A_name.lower():
                        prompt_tags = {extract_point(object_A_name.lower())}
                    else:
                        prompt_tags = {object_A_name.lower()}
                elif question_type == "two_object_fact":
                    if "point" in object_A_name.lower() and "point" in object_B_name.lower():
                        prompt_tags = {extract_point(object_A_name.lower()), extract_point(object_B_name.lower())}
                    else:
                        prompt_tags = {object_A_name.lower(), object_B_name.lower()}
                else:
                    if "point" in object_A_name.lower() and "point" in object_B_name.lower() and "point" in object_C_name.lower():
                        prompt_tags = {extract_point(object_A_name.lower()), extract_point(object_B_name.lower()), extract_point(object_C_name.lower())}
                    else:
                        prompt_tags = {object_A_name.lower(), object_B_name.lower(), object_C_name.lower()}
                question_tags = set() 
                answer_tags = set()
                for item in prompt_tags:
                    if item in question.lower():
                        question_tags.add(item)
                    if item in answer.lower():
                        answer_tags.add(item)

                # Check if all validations pass
                if prompt_tags == question_tags:
                    if answer_tags.issubset(prompt_tags):
                        if all(question.lower().count(tag) == 1 for tag in prompt_tags):
                            if question_type == "two_object_fact":
                                if "point" in object_A_name.lower() and "point" in object_B_name.lower():
                                    A_point_num = extract_point(object_A_name.lower())
                                    B_point_num = extract_point(object_B_name.lower())
                                    # 判断是否已经有括号包裹
                                    if f"({A_point_num})" not in question:
                                        question = question.replace(A_point_num, f"({A_point_num})")
                                    if f"({B_point_num})" not in question:
                                        question = question.replace(B_point_num, f"({B_point_num})")
                                    if f"({A_point_num})" not in answer:
                                        answer = answer.replace(A_point_num, f"({A_point_num})")
                                    if f"({B_point_num})" not in answer:
                                        answer = answer.replace(B_point_num, f"({B_point_num})")
                            elif question_type == "one_object_fact":
                                if "point" in object_A_name.lower():
                                    A_point_num = extract_point(object_A_name.lower())
                                    # 判断是否已经有括号包裹
                                    if f"({A_point_num})" not in question:
                                        question = question.replace(A_point_num, f"({A_point_num})")
                                    if f"({A_point_num})" not in answer:
                                        answer = answer.replace(A_point_num, f"({A_point_num})")
                            # print(f"Prompt: {prompt}")
                            # print(f"Question: {question}")
                            # print(f"Answer: {answer}")
                            # print("---------------")
                            return True, question, answer
                        else:
                            print(f"Attempt {attempt + 1}: skipping because object name appeared >1 times in question")
                    else:
                        print(f"Attempt {attempt + 1}: skipping because object name miss-matched in answer")
                else:
                    print(f"Attempt {attempt + 1}: skipping because object name miss-matched in question")

            except Exception as e:
                print(f"Attempt {attempt + 1} failed with error: {str(e)}")

        print(f"Failed to get valid output after {max_retries} attempts")
        return False, None, None
    server_process = execute_shell_command(
        f"python -m sglang.launch_server --model-path {model_path}  --port {base_port+device} --host 0.0.0.0 --tp 1"
    )
    wait_for_server(f"http://localhost:{base_port+device}")
    set_default_backend(RuntimeEndpoint(f"http://localhost:{base_port+device}"))
    while not task_queue.empty():
        frame_path = task_queue.get()
        scene_id = frame_path.split("/")[-2]
        os.makedirs(f"{this_machine_llm_qa_dir}/{scene_id}", exist_ok=True)
        frame_id = frame_path.split("/")[-1]
        frame_facts_path = Path(frame_path) / "fact.json"
        # Read llm_prompts json
        with open(frame_facts_path, "r") as f:
            image_facts = json.load(f)
        llm_prompts = image_facts["llm_prompts"]
        image_path = image_facts["image_path"]
        image_caption = image_facts["image_caption"]
        conversations = []
        # 修改点：随机选择最多3个提示
        num_to_select = min(15, len(llm_prompts))
        selected_prompts = random.sample(llm_prompts, num_to_select) if llm_prompts else []
        for llm_prompt in selected_prompts:
            success, question, answer = process_prompt(llm_prompt, image_caption, rephrase_qa)
            if success:
                conversation = llm_prompt.copy()
                conversation["question"] = question
                conversation["answer"] = answer
                conversations.append(conversation)
        image_facts["conversations"] = conversations
        with open(f"{this_machine_llm_qa_dir}/{scene_id}/{frame_id}.json", "w") as f:
            json.dump(image_facts, f, indent=4)
        result_queue.put(frame_id)



def main(args):
    devices = list(args.devices)
    model_path = args.model_path
    os.makedirs(args.llm_qa_dir, exist_ok=True)
    machine_id = int(args.machine_id)
    machine_count = 8
    this_machine_llm_qa_dir = f"{args.llm_qa_dir}/{machine_id}"
    os.makedirs(this_machine_llm_qa_dir, exist_ok=True)
    frame_dirs = find_all_frame_dirs(args.scene_dir)
    sorted_frame_dirs = sorted(frame_dirs)
    # 根据machine_count和machine_id分割图像列表
    total_frames = len(sorted_frame_dirs)
    chunk_size = total_frames // machine_count
    remainder = total_frames % machine_count

    if machine_id < remainder:
        start_idx = machine_id * (chunk_size + 1)
        end_idx = start_idx + (chunk_size + 1)
    else:
        start_idx = remainder * (chunk_size + 1) + (machine_id - remainder) * chunk_size
        end_idx = start_idx + chunk_size

    assigned_frame_list = sorted_frame_dirs[start_idx:end_idx]
    print(f"Machine {machine_id} totally needs to process {len(assigned_frame_list)} frames (total: {total_frames})")
    multiprocessing.set_start_method('spawn')
    delete_invalid_jsons(this_machine_llm_qa_dir)
    
    this_machine_has_process_frames_dic = {
        f.stem: True
        for f in Path(this_machine_llm_qa_dir).rglob("*.json")
    }
    should_process_frames_list = []
    for frame_path in assigned_frame_list:
        frame_id = os.path.basename(frame_path)
        if frame_id not in this_machine_has_process_frames_dic:
            should_process_frames_list.append(frame_path)
    print(f"this machine has processed images {len(this_machine_has_process_frames_dic)}, should process images {len(should_process_frames_list)}")
    
    task_queue = multiprocessing.Manager().Queue(maxsize=len(should_process_frames_list))
    result_queue = multiprocessing.Manager().Queue(maxsize=len(should_process_frames_list))
    for frames_path in should_process_frames_list:
        task_queue.put(frames_path)
    processes = []
    for device in devices:
        p = multiprocessing.Process(target=process_facts, args=(task_queue, result_queue, device, model_path, args.port, this_machine_llm_qa_dir))
        processes.append(p)
        p.start()
    # Initialize tqdm progress bar
    progress_bar = tqdm.tqdm(total=len(should_process_frames_list))

    while len(this_machine_has_process_frames_dic) != len(assigned_frame_list):
        while not result_queue.empty():
            item = result_queue.get()
            this_machine_has_process_frames_dic[item] = True
            # Update progress bar
            progress_bar.update(1)
        time.sleep(1)

    for p in processes:
        p.join()

    # Ensure the progress bar closes properly
    progress_bar.close()


def parse_args():
    """Command-line argument parser."""
    parser = argparse.ArgumentParser(description="Generate 3D SceneGraph for an image.")
    parser.add_argument("--config", default="configs/v2.py", help="Annotation config file path.")
    parser.add_argument("--port", default=3000, help="Port for Sglang")
    parser.add_argument(
        "--scene_dir",
        default="/home_sfs/zhouenshen/dataset/3D/cubifyanything/filter_step_20",
        help="Path to llm prompt json.",
    )
    parser.add_argument(
        "--llm_qa_dir",
        default="/home_sfs/zhouenshen/dataset/3D/cubifyanything/llm_qa",
        help="Path to llm qa json.",
    )
    parser.add_argument(
        "--machine_id", help="one of 0,1,2,3,4, and should be int",
    )
    parser.add_argument(
        "--model_path", default="/home/vlm/pretrain_model/QwQ-32B"
    )
    parser.add_argument(
        "--devices", default=[0,1,2,3,4,5,6,7]
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    args.timestamp = timestamp
    main(args)
