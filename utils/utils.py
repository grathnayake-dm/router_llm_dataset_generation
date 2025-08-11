import os
import json
import re
from typing import List, Dict, Any
from pathlib import Path 


# step 01 save handler regsistries

import os
import re
import json

def save_handlers(handler_type: str, all_outputs: list, save_dir="handlers"):
    output_folder = os.path.join(save_dir, handler_type)
    os.makedirs(output_folder, exist_ok=True)

    for i, raw_output in enumerate(all_outputs, start=1):
        file_name = f"{handler_type}_{i}.jsonl"
        file_path = os.path.join(output_folder, file_name)

        data = None
        if isinstance(raw_output, str):
            # Clean markdown json fences and unescape newlines
            cleaned = re.sub(r"```json|```", "", raw_output).strip()
            cleaned = cleaned.replace("\\n", "\n")

            try:
                data = json.loads(cleaned)
            except json.JSONDecodeError as e:
                print(f"[Warning] Skipping invalid JSON output {i}: {e}")
                # Skip invalid JSON silently (no error file)
                continue

        elif isinstance(raw_output, list):
            data = raw_output
        else:
            data = [raw_output]

        if data:
            with open(file_path, "w", encoding="utf-8") as f:  # "w" to overwrite if exists
                # If data is a list, write each item as a JSON line
                if isinstance(data, list):
                    for item in data:
                        json_line = json.dumps(item, ensure_ascii=False)
                        f.write(json_line + "\n")
                else:
                    # If data is a single object, write it as one line
                    json_line = json.dumps(data, ensure_ascii=False)
                    f.write(json_line + "\n")
            print(f"Saved: {file_path}")
        else:
            print(f"No valid data to save for output {i}, skipping file creation.")

            
            
# def save_handlers(handler_type: str, all_outputs: list, save_dir="handlers"):
#     output_folder = os.path.join(save_dir, handler_type)
#     os.makedirs(output_folder, exist_ok=True)

#     for i, raw_output in enumerate(all_outputs, start=1):
#         file_name = f"{handler_type}_{i}.jsonl"
#         file_path = os.path.join(output_folder, file_name)

#         data = None
#         if isinstance(raw_output, str):
#             cleaned = re.sub(r"```json|```", "", raw_output).strip()
#             cleaned = cleaned.replace("\\n", "\n")

#             try:
#                 data = json.loads(cleaned)
#             except json.JSONDecodeError as e:
#                 print(f"JSON decode error in output {i}: {e}")
#                 # Optional: save the invalid raw output to a separate file for debugging
#                 error_file = file_path + ".error"
#                 with open(error_file, "w", encoding="utf-8") as ef:
#                     ef.write(cleaned)
#                 # Skip writing the normal jsonl file
#                 continue
#         elif isinstance(raw_output, list):
#             data = raw_output
#         else:
#             data = [raw_output]
#         if data:
#             with open(file_path, "a", encoding="utf-8") as f:
#                 # Use "w" mode to overwrite any existing file, avoid append
#                 for item in data:
#                     json_line = json.dumps(item, ensure_ascii=False)
#                     f.write(json_line + "\n")
#             print(f"Saved: {file_path}")
#         else:
#             print(f"No valid data to save for output {i}, skipping file creation.")


# ----- Sep 02 : static field building
from pathlib import Path
from typing import List, Dict, Any
import json

def load_registries(base_dir, handler_type) -> List[Dict[str, Any]]:
    base_dir = Path(base_dir)
    all_entries = []

    print(f"[INFO] Scanning base directory: {base_dir}")
    for jsonl_file in base_dir.glob("*.jsonl"):
        if ".ipynb_checkpoints" in str(jsonl_file):
            continue 
            
        with open(jsonl_file, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    print(f"[⚠️] Skipping empty line {line_number} in {jsonl_file}")
                    continue
                try:
                    entry = json.loads(line)
                    all_entries.append({
                        "entry": entry,
                        "handler_type": handler_type
                    })
                    print(f"[✅] Parsed line {line_number} from {jsonl_file}")
                except json.JSONDecodeError as e:
                    print(f"[❌] Error parsing line {line_number} in {jsonl_file}: {e}")

    print(f"[✅] {handler_type}) -- > Total entries loaded: {len(all_entries)}")
    return all_entries


def save_static_jsonl_files(handler_type, data, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{handler_type}.jsonl")
    with open(save_path, 'a', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    # print(f"💾 Saved static fields to {save_path}")
    
    
# final stage

from pathlib import Path

from pathlib import Path

def merge_files(version: str):
    print(f" Starting merging JSONL")

    input_dir = Path(f"./add_handlers/output/{version}")
    batch_folder = Path(f"dataset/batches/{version}") 
    batch_folder.mkdir(parents=True, exist_ok=True)

    output_path = batch_folder / f"{version}.jsonl"

    final_dataset_dir = Path("dataset/final_dataset")
    final_dataset_dir.mkdir(parents=True, exist_ok=True)
    final_dataset_path = final_dataset_dir / "final_dataset.jsonl"

    with output_path.open("w", encoding="utf-8") as outfile, \
         final_dataset_path.open("a", encoding="utf-8") as finalfile:  # append mode

        for jsonl_file in sorted(input_dir.glob("*.jsonl")):
            if jsonl_file.name.startswith("batch__"):
                continue

            with jsonl_file.open("r", encoding="utf-8") as infile:
                for line in infile:
                    if line.strip():
                        clean_line = line.rstrip() + "\n"
                        outfile.write(clean_line)
                        finalfile.write(clean_line)

    print(f"✅ Merged JSONL written to: {output_path}")
    print(f"📌 Appended to final dataset: {final_dataset_path}")




