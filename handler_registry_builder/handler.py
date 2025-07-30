import os
import time
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


class RegistryBuilder:
    def __init__(self, api_key):
        self.gemini_llm = LlmGemini(api_key = api_key)
        

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

    def _build_prompt(self, handler_type: str, domain: str) -> str:
        if handler_type == "base_llm":
            model_list = [getattr(models, name) for name in models.__all__]
            return self.prompt_map[handler_type].format(domain=domain, model_list=model_list)
        else:
            return (
                f"You are designing tools for the selected domain. "
                f"Follow the prompt template below to generate the tools: {self.prompt_map[handler_type]}"
            )

    def build_registry(self, handler_type: str, version: str):
        if handler_type not in self.prompt_map:
            raise ValueError(f"[❌] Invalid handler type: {handler_type}")

        print(f"[🔧] Building registry for handler_type: {handler_type}")

        usecases = self.usecase_map[handler_type]
        all_outputs = []

        for domain in usecases:
            print("44444444444444444444")
            prompt = self._build_prompt(handler_type, domain)
            print("55555555555555555555555", handler_type)
            print(f"{handler_type}: [🧠] Calling Gemini")
            print("66666666666666666666666", handler_type)

            start_time = time.time()
            output = self.gemini_llm.call_gemini(prompt)
            end_time = time.time()
            all_outputs.append(output)
            print(f"{handler_type}: [✅] Done with domain:{end_time - start_time:.2f}s")

        save_path = f"./handler_registry_builder/handler_registries/{version}"
        save_handlers(handler_type, all_outputs, save_dir=save_path)
        print(f"{handler_type}:[💾] Saved handler registry in: {save_path}/{handler_type}")


