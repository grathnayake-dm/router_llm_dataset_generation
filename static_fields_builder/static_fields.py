import uuid
import random
import itertools
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any

import os
import json
from typing import List, Dict


class StaticFieldsBuilder:

    def __init__(self, entry: List[Dict[str, Any]], handler_type: str):
        self.entry = entry
        self.handler_type = handler_type
        self.handler = {
            'mcp_tools': [],
            'worker_agents': [],
            'llm_handlers': [],
            'rag_handlers': []
        }

    def generate_id(self) -> str:
        return str(uuid.uuid4())
   
    def generate_confidence(self) -> float:
        return round(random.uniform(0.6, 0.99), 6)
    
    def generate_date_time(self) -> Tuple[str, str]:
        now = datetime.now()
        start_range = now - timedelta(days=730) 
        max_offset = int((now - start_range).total_seconds()) - 172800  # leave 2 days for timestamp window
        compiled_base = start_range + timedelta(seconds=random.randint(0, max_offset))
        timestamp = compiled_base + timedelta(seconds=random.randint(60, 172800))
        return compiled_base.isoformat(), timestamp.isoformat()
    
    def get_handler_registry(self, compiled_at: str) -> dict:
        if self.handler_type == "rag":
            self.handler['rag_handlers'].append(self.entry)
        elif self.handler_type == "base_llm":
            self.handler['llm_handlers'].append(self.entry)
        elif self.handler_type == "mcp_tool":
            self.handler['mcp_tools'].append(self.entry)
        elif self.handler_type == "worker_agent":
            self.handler['worker_agents'].append(self.entry)

        return {
            **self.handler, 
            "compiled_at": compiled_at,
            "user_id": str(uuid.uuid4()),
            "workspace_id": str(uuid.uuid4())
        }

    def get_copilot_id(self):     
        return self.entry.get("handler_payload")['copilot_id'] if self.handler_type == "rag" else None
    
    def get_servername(self):
        return self.entry.get("server_name") if self.handler_type == "mcp_tool" else None
    
    def get_toolname(self):
        return "" if self.handler_type == "mcp_tool" else None

    def get_workspace_preference_override(self) :
        if self.entry.get('is_workspace_default', {}) == True:
            return True
        else:
            return False

    def build_structured_entries(self,) -> List[dict]:
        print(f"{self.handler_type}: 📦 Step 2: Building static fields")
        results = []
        compiled_at, timestamp = self.generate_date_time()
        results.append(
            {
                "input": {
                    "id": str(uuid.uuid4()),
                    "timestamp": timestamp,
                    "query": "",
                    "conversation_summary": "",
                    "handler_registry": self.get_handler_registry(compiled_at),
                    "copilot_id": None,
                    "thread_id": str(uuid.uuid4())
                },
                "output": {
                    "select_handler_type": self.handler_type,
                    "handler_name": self.entry['name'],
                    "server_name": self.get_servername(),
                    "tool_name": self.get_toolname(),
                    "copilot_id": self.get_copilot_id(),
                    "missing_fields": [],
                    "optional_suggestions": [],
                    "suggested_payload": {},
                    "confidence": round(random.uniform(0.6, 0.99), 6),
                    "reasoning": "",
                    "chain_of_thought": [],
                    "workspace_preference_override": self.get_workspace_preference_override()
                }
            }
        )
        return results



