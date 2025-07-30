import os
import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from .prompts.base_llm import BASE_LLM_PROMPT
from data_validation.prompts.rag import RAG_PROMPT
from data_validation.prompts.worker_agent import WORKER_AGENT_PROMPT
from data_validation.prompts.mcp_tool import MCP_TOOL_PROMPT

PROMPT_MAP = {
    "base_llm": BASE_LLM_PROMPT,
    "rag": RAG_PROMPT,
    "worker_agent": WORKER_AGENT_PROMPT,
    "mcp_tool": MCP_TOOL_PROMPT,
}


class DataValidator:
    def __init__(
    self,
    api_key: str,
    version: str,
    handler_type: str,
    batch_size: int = 300,
    start_line: int = 0,
    end_line: int = None,
    model_id: str = "gemini-2.5-pro",
):
        self.api_key = api_key
        self.version = version
        self.handler_type = handler_type
        self.batch_size = batch_size
        self.start_line = start_line
        self.end_line = end_line
        self.model_id = model_id
        # Define input path directly
        self.input_path = Path(f"./contextual_fields_builder/contextual_output/{version}/{handler_type}/{handler_type}.jsonl")
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        self.input_filename = self.input_path.name

        base_output_dir = Path(f"./data_validation/validated_output/{version}")
        base_output_dir.mkdir(parents=True, exist_ok=True)

        self.merged_valid_refined_path = base_output_dir / self.input_filename
        self.merged_valid_refined_path.parent.mkdir(parents=True, exist_ok=True)

        self.base_output_dir = base_output_dir / "metadata" / self.input_filename.replace(".jsonl", "").replace(".json", "")
        self.base_output_dir.mkdir(parents=True, exist_ok=True)

        self.raw_output_dir = self.base_output_dir / "raw_output"
        self.raw_output_dir.mkdir(exist_ok=True)

        self.valid_dir = self.base_output_dir / "valid"
        self.valid_dir.mkdir(exist_ok=True)

        self.refined_dir = self.base_output_dir / "refined"
        self.refined_dir.mkdir(exist_ok=True)

        self.invalid_dir = self.base_output_dir / "invalid"
        self.invalid_dir.mkdir(exist_ok=True)

        self.unknown_dir = self.base_output_dir / "unknown"
        self.unknown_dir.mkdir(exist_ok=True)

        self.temp_dir = self.base_output_dir / "temp_batches"
        self.temp_dir.mkdir(exist_ok=True)

        self.checkpoint_path = self.base_output_dir / "checkpoint.json"

        # Prompt
        self.prompt = PROMPT_MAP[handler_type]

        # Gemini client
        self.client = genai.Client(api_key=api_key)
        self.wait_time = 30  # seconds


    def load_input_range(self, start_line, end_line):
        selected = []
        print(f"[DEBUG] Opening input file: {self.input_path}")
        with self.input_path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f):
                if line_num < start_line:
                    if line_num % 1000 == 0:
                        print(f"[DEBUG] Skipping line {line_num} (before start_line)")
                    continue
                if end_line is not None and line_num >= end_line:
                    print(f"[DEBUG] Reached end_line at line {line_num}. Stopping read.")
                    break

                line = line.strip()
                if not line:
                    print(f"[DEBUG] Skipping empty line at {line_num}")
                    continue

                try:
                    obj = json.loads(line)
                    selected.append(obj)
                    if len(selected) % 100 == 0:
                        print(f"[DEBUG] Loaded {len(selected)} objects so far (up to line {line_num})")
                except json.JSONDecodeError as e:
                    print(f"[WARN] Invalid JSON at line {line_num + 1}: {e}")
                    print(f"[WARN] Offending line: {line}")

        print(f"[INFO] Loaded total {len(selected)} JSON objects from line {start_line} to {end_line}")
        return selected

    def load_checkpoint(self):
        if self.checkpoint_path.exists():
            with self.checkpoint_path.open("r") as f:
                return set(json.load(f))
        return set()

    def save_checkpoint(self, processed_batches):
        with self.checkpoint_path.open("w") as f:
            json.dump(sorted(list(processed_batches)), f)

    def wrap_with_prompt(self, obj, index):
        return {
            "key": f"request_{index}",
            "request": {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"""Below is the input data the model must operate on:

INPUT_JSON:
{json.dumps(obj, indent=2)}

Instructions to review and refine above INPUT_JSON :
{self.prompt}
"""
                            }
                        ]
                    }
                ]
            }
        }

    def upload_and_run_batch(self, batch_data, batch_index):
        batch_filename = f"batch_request_{batch_index}.jsonl"
        temp_path = self.temp_dir / batch_filename

        with temp_path.open("w", encoding="utf-8") as f:
            for j, obj in enumerate(batch_data, start=1):
                f.write(json.dumps(self.wrap_with_prompt(obj, j)) + "\n")

        print(f"[Uploading] {batch_filename}")
        uploaded_file = self.client.files.upload(
            file=str(temp_path),
            config=types.UploadFileConfig(display_name=batch_filename, mime_type='jsonl')
        )

        job = self.client.batches.create(
            model=self.model_id,
            src=uploaded_file.name,
            config={"display_name": f"job_for_{batch_filename}"}
        )
        return job.name

    def poll_until_done(self, job_name):
        print(f"[Polling] Job: {job_name}")
        while True:
            job = self.client.batches.get(name=job_name)
            state = job.state.name
            if state in ("JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"):
                return job
            print(f"[WAIT] State: {state}. Sleeping {self.wait_time} seconds.")
            time.sleep(self.wait_time)

    def save_results(self, job, batch_index):
        if job.state.name != "JOB_STATE_SUCCEEDED":
            print(f"[ERROR] Job failed: {job.error}")
            return

        result_file = job.dest.file_name
        result_bytes = self.client.files.download(file=result_file)
        result_text = result_bytes.decode("utf-8")

        parsed_outputs = []
        for line_num, line in enumerate(result_text.strip().splitlines(), start=1):
            try:
                parsed = json.loads(line)
                candidates = parsed.get("response", {}).get("candidates", [])
                for candidate in candidates:
                    text_block = candidate.get("content", {}).get("parts", [])[0].get("text", "")
                    if text_block.startswith("```"):
                        lines = text_block.splitlines()
                        if lines[0].strip().startswith("```json") or lines[0].strip() == "```":
                            lines = lines[1:]
                        if lines and lines[-1].strip() == "```":
                            lines = lines[:-1]
                        text_block = "\n".join(lines)
                    parsed_outputs.append(json.loads(text_block))
            except Exception as e:
                print(f"[WARN] Error parsing output line {line_num}: {e}")

        raw_out_path = self.raw_output_dir / f"output_{batch_index}.jsonl"
        with raw_out_path.open("a", encoding="utf-8") as f:
            for obj in parsed_outputs:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")

        categorized = {
            "VALID": [],
            "REFINED": [],
            "INVALID": [],
            "UNKNOWN": []
        }

        for line_num, obj in enumerate(parsed_outputs, start=1):
            status = obj.get("status", "UNKNOWN").upper()
            data = obj.get("data", {})
            if status in categorized:
                categorized[status].append(data)
            else:
                categorized["UNKNOWN"].append({"line": line_num, "data": data})

        def append_jsonl(filepath, data_list):
            with filepath.open("a", encoding="utf-8") as f:
                for item in data_list:
                    try:
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
                    except Exception as e:
                        print(f"[WARN] Failed to write JSON in {filepath}: {e}")

        append_jsonl(self.valid_dir / f"valid_{batch_index}.jsonl", categorized["VALID"])
        append_jsonl(self.refined_dir / f"refined_{batch_index}.jsonl", categorized["REFINED"])
        append_jsonl(self.invalid_dir / f"invalid_{batch_index}.jsonl", categorized["INVALID"])
        append_jsonl(self.unknown_dir / f"unknown_{batch_index}.jsonl", categorized["UNKNOWN"])

        with self.merged_valid_refined_path.open("a", encoding="utf-8") as f:
            for entry in categorized["VALID"] + categorized["REFINED"]:
                try:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                except Exception as e:
                    print(f"[WARN] Failed to write merged valid/refined JSON: {e}")

        print(f"[✓] Saved batch {batch_index} results.")

    def run(self):
        t1 = time.time()
        inputs = self.load_input_range(self.start_line, self.end_line)
        total = len(inputs)
        num_batches = (total + self.batch_size - 1) // self.batch_size
        print(f"[INFO] Processing {num_batches} batches...")

        processed_batches = self.load_checkpoint()

        for i in range(num_batches):
            batch_num = f"{self.start_line}_{i + 1}"
            if batch_num in processed_batches:
                print(f"[✓] Skipping already processed batch {batch_num}")
                continue

            print(f"\n[Batch {batch_num}]")
            batch_data = inputs[i * self.batch_size : (i + 1) * self.batch_size]

            try:
                job_name = self.upload_and_run_batch(batch_data, batch_num)
                job = self.poll_until_done(job_name)
                self.save_results(job, batch_num)

                processed_batches.add(batch_num)
                self.save_checkpoint(processed_batches)

            except Exception as e:
                print(f"[❌] Batch {batch_num} failed: {e}")
                print("[⚠️] Saving checkpoint and exiting...")
                self.save_checkpoint(processed_batches)
                return

        print(f"\n[✓] Total time taken: {time.time() - t1:.2f} seconds")