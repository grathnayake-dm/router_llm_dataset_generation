import sys
import os
import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from google.api_core.retry import Retry, if_exception_type
from google.api_core.exceptions import GoogleAPIError, ResourceExhausted
from typing import List, Dict, Any

from contextual_fields_builder.prompts.rag import RAG_PROMPT
from contextual_fields_builder.prompts.base_llm import BASE_LLM_PROMPT
from contextual_fields_builder.prompts.mcp_tool import MCP_TOOL_PROMPT
from contextual_fields_builder.prompts.worker_agent import WORKER_AGENT_PROMPT

PROMPT_MAP = {
    "rag": RAG_PROMPT,
    "base_llm": BASE_LLM_PROMPT,
    "mcp_tool": MCP_TOOL_PROMPT,
    "worker_agent": WORKER_AGENT_PROMPT,
}

class ContextualFieldsBuilder:
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
        self.input_path = Path(f"./static_fields_builder/static_output/{version}/{handler_type}.jsonl")
        self.output_dir = Path(f"./contextual_fields_builder/contextual_output/{version}")
        self.prompt = PROMPT_MAP[handler_type]
        self.api_key = api_key
        self.batch_size = batch_size
        self.model_id = model_id
        self.start_line = start_line
        self.end_line = end_line
        self.handler_type = handler_type

        input_stem = self.input_path.stem
        self.output_folder = self.output_dir / input_stem
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.metadata_folder = self.output_folder / "metadata"
        self.batchwise_folder = self.metadata_folder / f"batch_{self.start_line}"
        self.batchwise_folder.mkdir(parents=True, exist_ok=True)
        self.temp_dir = self.batchwise_folder / "temp_batches"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.error_dir = self.batchwise_folder / "errors_batch_logs"
        self.error_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_path = self.batchwise_folder / "checkpoint.json"
        self.out_path = self.output_folder / self.input_path.name

        self.client = genai.Client(api_key=api_key)
        self.wait_time = 60

        self.retry = Retry(
            predicate=if_exception_type(
                ResourceExhausted,
                GoogleAPIError,
                ConnectionError,
                TimeoutError
            ),
            initial=2.0,
            maximum=120.0,
            multiplier=2.0,
            timeout=600.0,
            on_error=self._log_retry_error
        )

    def _log_retry_error(self, exception: Exception) -> None:
        print(f"[RETRY] Retryable error: {getattr(exception, 'error_details', str(exception))}")

    def load_input_range(self, start_line: int, end_line: int | None) -> List[Dict[str, Any]]:
        selected = []
        with self.input_path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f):
                if line_num < start_line:
                    continue
                if end_line is not None and line_num >= end_line:
                    break
                line = line.strip()
                if line:
                    try:
                        selected.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"[WARN] Invalid JSON at line {line_num + 1}: {e}")
        print(f"[INFO] Loaded {len(selected)} JSON objects from line {start_line} to {end_line}.")
        return selected

    def load_checkpoint(self) -> set:
        if self.checkpoint_path.exists():
            with self.checkpoint_path.open("r") as f:
                return set(json.load(f))
        return set()

    def save_checkpoint(self, processed_batches: set) -> None:
        with self.checkpoint_path.open("w") as f:
            json.dump(sorted(list(processed_batches)), f)

    def wrap_with_prompt(self, obj: Dict[str, Any], index: int) -> Dict[str, Any]:
        return {
            "key": f"request_{index}",
            "request": {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"""Below is the input data the model must operate on:INPUT_JSON:
{json.dumps(obj, indent=2)}Instructions to review and refine above INPUT_JSON:
{self.prompt}
"""
                            }
                        ]
                    }
                ]
            }
        }

    def upload_and_run_batch(self, batch_data: List[Dict[str, Any]], batch_index: str) -> str:
        batch_filename = f"batch_request_{batch_index}.jsonl"
        temp_path = self.temp_dir / batch_filename

        with temp_path.open("w", encoding="utf-8") as f:
            for j, obj in enumerate(batch_data, start=1):
                f.write(json.dumps(self.wrap_with_prompt(obj, j)) + "\n")

        print(f"[Uploading] {batch_filename}")

        @self.retry
        def upload_file():
            return self.client.files.upload(
                file=str(temp_path),
                config=types.UploadFileConfig(display_name=batch_filename, mime_type='jsonl')
            )

        try:
            uploaded_file = upload_file()
        except Exception as e:
            raise RuntimeError(f"Failed to upload {batch_filename} after retries: {e}") from e

        @self.retry
        def create_batch():
            return self.client.batches.create(
                model=self.model_id,
                src=uploaded_file.name,
                config={"display_name": f"job_for_{batch_filename}"}
            )

        try:
            job = create_batch()
            return job.name
        except Exception as e:
            raise RuntimeError(f"Failed to create batch {batch_filename} after retries: {e}") from e

    def poll_until_done(self, job_name: str) -> Any:
        print(f"[Polling] Job: {job_name}")

        @self.retry
        def get_batch():
            return self.client.batches.get(name=job_name)

        while True:
            try:
                job = get_batch()
                state = job.state.name
                if state in ("JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"):
                    if state == "JOB_STATE_FAILED" and hasattr(job, 'error'):
                        if job.error.code == 429:
                            raise ResourceExhausted(f"Quota exceeded for job {job_name}: {job.error.message}")
                        raise RuntimeError(f"Job {job_name} failed: {job.error}")
                    return job
                print(f"[WAIT] State: {state}. Sleeping {self.wait_time} seconds.")
                time.sleep(self.wait_time)
            except Exception as e:
                raise RuntimeError(f"Failed to poll job {job_name} after retries: {e}") from e

    def save_results(self, job: Any, batch_index: str) -> bool:
        if job.state.name != "JOB_STATE_SUCCEEDED":
            print(f"[ERROR] Job failed: {job.error}")
            return False

        @self.retry
        def download_result():
            return self.client.files.download(file=job.dest.file_name)

        try:
            result_bytes = download_result()
        except Exception as e:
            print(f"[ERROR] Failed to download results for batch {batch_index}: {e}")
            return False

        result_text = result_bytes.decode("utf-8")
        parsed_outputs = []
        error_lines = []

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
                    data = json.loads(text_block)
                    parsed_outputs.extend(data if isinstance(data, list) else [data])
            except Exception as e:
                error_lines.append({
                    "line_num": line_num,
                    "error": str(e),
                    "raw_line": line
                })

        def safe_json_dump(obj):
            try:
                return json.dumps(obj, ensure_ascii=False)
            except Exception as e:
                print(f"[WARN] Failed to encode JSON: {e}")
                return "{}"

        with self.out_path.open("a", encoding="utf-8") as f:
            for obj in parsed_outputs:
                f.write(safe_json_dump(obj) + "\n")

        if error_lines:
            error_path = self.error_dir / f"errors_batch_{batch_index}.log"
            with error_path.open("a", encoding="utf-8") as ef:
                for err in error_lines:
                    ef.write(f"Line {err['line_num']}: {err['error']}\nRaw line: {err['raw_line']}\n\n")
            print(f"[!] Saved {len(error_lines)} parse errors to {error_path}")

        print(f"[✓] Appended batch {batch_index} results to {self.out_path}")
        return True

    def run(self, start_line: int = 0, end_line: int | None = None) -> None:
        
        print(f"Start building contextual section of {self.handler_type}")
        
        t1 = time.time()
        inputs = self.load_input_range(start_line, end_line)
        total = len(inputs)
        num_batches = (total + self.batch_size - 1) // self.batch_size
        print(f"[INFO] Processing {num_batches} batches...")

        processed_batches = self.load_checkpoint()

        for i in range(num_batches):
            batch_num = f"{start_line}_{i + 1}"
            if batch_num in processed_batches:
                print(f"[✓] Skipping already processed batch {batch_num}")
                continue

            print(f"\n[Batch {batch_num}]")
            batch_data = inputs[i * self.batch_size: (i + 1) * self.batch_size]

            try:
                job_name = self.upload_and_run_batch(batch_data, batch_num)
                job = self.poll_until_done(job_name)
                if self.save_results(job, batch_num):
                    processed_batches.add(batch_num)
                    self.save_checkpoint(processed_batches)
                    print(f"Completed building contextual section of {self.handler_type}")
                else:
                    print(f"[WARN] Batch {batch_num} had no valid outputs")
            except ResourceExhausted as e:
                print(f"[ERROR] Quota exceeded: {e}. Retrying after wait...")
                time.sleep(self.wait_time)
                try:
                    job_name = self.upload_and_run_batch(batch_data, batch_num)
                    job = self.poll_until_done(job_name)
                    if self.save_results(job, batch_num):
                        processed_batches.add(batch_num)
                        self.save_checkpoint(processed_batches)
                        print(f"Completed building contextual section of {self.handler_type}")
                    else:
                        print(f"[WARN] Batch {batch_num} had no valid outputs after retry")
                except Exception as retry_e:
                    print(f"[ERROR] Retry failed: {retry_e}")
                    self.save_checkpoint(processed_batches)
                    raise
            except Exception as e:
                print(f"[ERROR] Unexpected failure: {e}")
                self.save_checkpoint(processed_batches)
                raise

        print(f"\n[✓] Total time taken: {time.time() - t1:.2f} seconds")
