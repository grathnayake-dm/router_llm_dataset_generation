import os
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai
import time
import click
import threading
import logging
from pathlib import Path

from handler_registry_builder.handler import RegistryBuilder
from static_fields_builder.static_fields import StaticFieldsBuilder
from contextual_fields_builder.contextual_fileds import ContextualFieldsBuilder
from data_validation.data_validation import DataValidator
from add_handlers.add_handlers import HandlerRegistryExtender
from utils.utils import save_handlers, load_registries, save_static_jsonl_files, merge_files

# Configure logging to output to both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

API_KEYS = {
    "rag": "AIzaSyAy3O2OIn-p0i8Gwctbud3o9mR2jEHkgQA",
    "base_llm": "AIzaSyCDIJ0SzNC3SqJDylSwNdUwWK9OXsom6_c",
    "worker_agent": "AIzaSyDeH_wnfSqW_EG9rXl0farmmIZaiswl6oM",
    "mcp_tool": "AIzaSyDeH_wnfSqW_EG9rXl0farmmIZaiswl6oM",
}

def run_pipeline(handler_type: str, version: str, api_key: str):
    try:
        logging.info(f"🚀 Starting pipeline for {handler_type}")

#         # Step 1: Registry
#         logging.info(f"[{handler_type}] 🔧 Step 1: Registry")
#         try:
#             builder = RegistryBuilder(api_key=api_key)
#             builder.build_registry(handler_type, version)
#         except Exception as e:
#             logging.error(f"[{handler_type}] ❌ Registry step failed: {e}")
#             return
#         time.sleep(30)

#         # Step 2: Static Fields
#         logging.info(f"[{handler_type}] 📦 Step 2: Static Fields")
#         try:
#             base_dir = Path(f"handler_registry_builder/handler_registries/{version}/{handler_type}")
#             entries = load_registries(base_dir=base_dir, handler_type=handler_type)
#             for item in entries:
#                 entry = item['entry']
#                 static_builder = StaticFieldsBuilder(entry, handler_type)
#                 results = static_builder.build_structured_entries()
#                 save_static_jsonl_files(handler_type, results, save_dir=f"./static_fields_builder/static_output/{version}")
#         except Exception as e:
#             logging.error(f"[{handler_type}] ❌ Static fields step failed: {e}")
#             return
#         time.sleep(30)

        # Step 3: Contextual Fields
        logging.info(f"[{handler_type}] 🧠 Step 3: Contextual Fields")
        try:
            context_builder = ContextualFieldsBuilder(
                api_key=api_key,
                version=version,
                handler_type=handler_type,
                batch_size=200,
                start_line=0,
                end_line=None
            )
            context_builder.run()
        except Exception as e:
            logging.error(f"[{handler_type}] ❌ Contextual fields step failed: {e}")
            return
        time.sleep(30)
        
        # Step 4: Validation
        logging.info(f"[{handler_type}] ✅ Step 4 : Validation")
        try:
            data_validator = DataValidator(
                api_key=api_key,
                version=version,
                handler_type=handler_type,
                batch_size=200,
                start_line=0,
                end_line=None
            )
            data_validator.run()
        except Exception as e:
            logging.error(f"[{handler_type}] ❌ Validation step failed: {e}")
            return
        time.sleep(30)
        
        # Step 5: Append Handlers
        logging.info(f"[{handler_type}] 📚 Step 5: Append Handlers")
        try:
            extender = HandlerRegistryExtender(version=version, handler_type=handler_type)
            extender.extend_single_jsonl()
        except Exception as e:
            logging.error(f"[{handler_type}] ❌ Append handlers step failed: {e}")
            return
        
        # Step 6: Merge Data
        logging.info(f"[{handler_type}] 📚 Step 6: Merge Data")
        try:
            logging.info(f"[{handler_type}] 🔗 Merging data after pipeline...")
            merge_files(version=version)
        except Exception as merge_err:
            logging.error(f"[{handler_type}] ❌ Merge failed: {merge_err}")
            return

        logging.info(f"[{handler_type}] 🎉 Pipeline completed successfully!")

    except Exception as top_level_error:
        logging.critical(f"[{handler_type}] 🔥 Pipeline crashed: {top_level_error}")

@click.command()
@click.option('--version', required=True, help='Version label (e.g., 5)')
def main(version):
    # "rag", "worker_agent", "base_llm", "mcp_tool"
    handler_types = ["rag", "worker_agent", "base_llm",]
    threads = []

    for handler in handler_types:
        api_key = API_KEYS.get(handler)
        t = threading.Thread(target=run_pipeline,
                             args=(handler, version, api_key))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
        print(f"✅ Completed thread: {thread.name}")

if __name__ == "__main__":
    main()
