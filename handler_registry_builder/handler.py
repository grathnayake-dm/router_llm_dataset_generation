import os
import time
import concurrent.futures

from .gemini import LlmGemini
from .prompts.rag import RAG_PROMPT
from .prompts.base_llm import LLM_PROMPT
from .prompts.mcp_tool import MCP_TOOL_PROMPT
from .prompts.worker_agent import WOKER_AGENT_PROMPT

from .prompts.domains.rag import usecases as rag_usecases
from .prompts.domains.mcp_tool import usecases as mcp_usecases
from .prompts.domains.base_llm import usecases as llm_usecases
from .prompts.domains.worker_agent import usecases as worker_agent_usecases

from .prompts.domains.base_llm import models
from utils.utils import save_handlers
from string import Template


class RegistryBuilder:
    def __init__(self, api_key):
        self.gemini_llm = LlmGemini(api_key=api_key)

        self.prompt_map = {
            "base_llm": LLM_PROMPT,
            "mcp_tool": MCP_TOOL_PROMPT,
            "rag": RAG_PROMPT,
            "worker_agent": WOKER_AGENT_PROMPT
        }

        self.usecase_map = {
            "base_llm": [getattr(llm_usecases, name) for name in llm_usecases.__all__],
            "mcp_tool": [getattr(mcp_usecases, name) for name in mcp_usecases.__all__],
            "rag": [getattr(rag_usecases, name) for name in rag_usecases.__all__],
            "worker_agent": [getattr(worker_agent_usecases, name) for name in worker_agent_usecases.__all__]
        }

    def _build_prompt(self, handler_type: str, domain: str, hander_count_per_domain : str) -> str:
        if handler_type == "base_llm":
            model_list = [getattr(models, name) for name in models.__all__]
            return self.prompt_map[handler_type].substitute(domain=domain, model_list=model_list, count = hander_count_per_domain)
        else:
            return self.prompt_map[handler_type].substitute( domain=domain,count = hander_count_per_domain
)

    def build_registry(self, handler_type: str, version: str, hander_count_per_domain: str):
        if handler_type not in self.prompt_map:
            raise ValueError(f"{handler_type}: [❌] Invalid handler type: {handler_type}")

        print(f"[🔧] Building registry for handler_type: {handler_type}")
        usecases = self.usecase_map[handler_type]
        all_outputs = []

        def process_domain(domain):
            try:
                prompt = self._build_prompt(handler_type, domain, hander_count_per_domain)
                print(f"{handler_type}: [🧠] Calling Gemini for domain")
                start_time = time.time()
                output = self.gemini_llm.call_gemini(prompt)
                end_time = time.time()
                print(f"{handler_type}: [✅] Done with domain in {end_time - start_time:.2f}s")
                return output
            except Exception as e:
                print(f"{handler_type}:  [❌] Error processing domain: {e}")
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(usecases))) as executor:
            futures = [executor.submit(process_domain, domain) for domain in usecases]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    all_outputs.append(result)

        save_path = f"./handler_registry_builder/handler_registries/{version}"
        save_handlers(handler_type, all_outputs, save_dir=save_path)
        print(f"{handler_type}: [💾] Saved handler registry in: {save_path}/{handler_type}")
