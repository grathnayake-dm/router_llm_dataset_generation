import os
import json
import random
from pathlib import Path
from copy import deepcopy

HANDLER_TYPE_MAP = {
    "mcp_tool": "mcp_tools",
    "worker_agent": "worker_agents",
    "base_llm": "llm_handlers",
    "rag": "rag_handlers"
}

class HandlerRegistryExtender:
    def __init__(self, handler_type,  version):
        self.input_file_path = Path(f"./data_validation/validated_output/{version}/{handler_type}.jsonl")   
        self.output_dir = Path(f"./add_handlers/output/{version}")
        self.source = Path(f"./handler_registry_builder/handler_registries/{version}")
        self.available_handlers = self._load_available_handlers()

    def _load_available_handlers(self):
        print("[🔍] Starting to load available handlers...")

        handler_sources = {key: [] for key in HANDLER_TYPE_MAP.values()}
        print(f"[🗂️] Initialized handler_sources with keys: {list(handler_sources.keys())}")

        for folder_name, registry_key in HANDLER_TYPE_MAP.items():
            folder_path = self.source / folder_name
            print(f"\n[📁] Checking folder for handler type '{registry_key}': {folder_path}")

            if not folder_path.is_dir():
                print(f"[❌] Request cannot proceed further: Missing folder in handler registry: {folder_path}")
                raise FileNotFoundError(f"❌ Input file does not exist: {input_path}")

            for filename in os.listdir(folder_path):
                if filename.endswith(".jsonl"):
                    file_path = folder_path / filename
                    print(f"[📄] Reading file: {file_path}")

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            for idx, line in enumerate(f, 1):
                                line = line.strip()
                                if not line:
                                    print(f"[⚠️] Skipping empty line {idx} in {filename}")
                                    continue
                                try:
                                    item = json.loads(line)
                                    if item not in handler_sources[registry_key]:
                                        handler_sources[registry_key].append(item)
                                except json.JSONDecodeError as e:
                                    print(f"[❌] JSON decode error at line {idx} in {filename}: {e}")
                    except Exception as e:
                        print(f"[🔥] Failed reading {file_path}: {e}")

        print("\n[✅] Handler loading complete.")
        for key, items in handler_sources.items():
            print(f"[📦] {key}: Loaded {len(items)} handlers.")

        return handler_sources

    def _extend_and_shuffle_handler_lists(self, registry: dict):
        for handler_key, available_items in self.available_handlers.items():
            existing_items = registry.get(handler_key, [])
            serialized_existing = set(json.dumps(i, sort_keys=True) for i in existing_items)

            new_candidates = [i for i in available_items if json.dumps(i, sort_keys=True) not in serialized_existing]

            has_default = any(h.get("is_workspace_default") for h in existing_items) if handler_key == "llm_handlers" else False

            random.shuffle(new_candidates)
            selected_new = []
            for candidate in new_candidates:
                if handler_key == "llm_handlers" and candidate.get("is_workspace_default"):
                    if has_default:
                        continue
                    has_default = True
                selected_new.append(candidate)
                if len(selected_new) >= random.randint(6, 10):
                    break

            combined = existing_items + selected_new
            random.shuffle(combined)
            registry[handler_key] = combined

    def extend_single_jsonl(self):
        print(f"{self.handler_type}:  ▶️ Step 3: Starting adding handlers to registry")
        input_path = self.input_file_path
        if not input_path.is_file():
            raise FileNotFoundError(f"❌ Input file does not exist: {input_path}")
    

        out_path = self.output_dir / input_path.name
        out_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[→] Processing input file: {input_path}")

        with open(input_path, "r", encoding="utf-8") as in_file, \
             open(out_path, "w", encoding="utf-8") as out_file:  # overwrite mode

            for line_num, line in enumerate(in_file, 1):
                if not line.strip():
                    continue
                try:
                    parsed = json.loads(line)
                    entries = parsed if isinstance(parsed, list) else [parsed]
                except Exception as e:
                    print(f"[!] Skipping bad JSON at line {line_num} in {input_path}: {e}")
                    continue

                for entry in entries:
                    if not isinstance(entry, dict) or "input" not in entry:
                        continue

                    new_entry = deepcopy(entry)
                    input_block = new_entry["input"]
                    registry_data = input_block.get("handler_registry", {})

                    if isinstance(registry_data, list) and registry_data:
                        registry = registry_data[0]
                    elif isinstance(registry_data, dict):
                        registry = registry_data
                    else:
                        continue

                    self._extend_and_shuffle_handler_lists(registry)
                    input_block["handler_registry"] = registry
                    new_entry["input"] = input_block

                    out_file.write(json.dumps(new_entry, ensure_ascii=False) + "\n")
                    print(f"[✔] Extended entry id: {input_block.get('id', 'unknown')}")

        print(f"[✅] Output saved to: {out_path}")

