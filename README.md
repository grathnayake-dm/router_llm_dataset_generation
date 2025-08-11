---

# Router LLM Data Generation Pipeline

This project is designed to create high-quality training data for building a multi-conversational, multi-decision-making LLM, referred to as the Router LLM. The Router LLM is expected to intelligently route and respond to diverse user needs by selecting and interacting with four different types of handlers — including rag, base_llm, mcp_tool, and worker_agent.

To support this, the pipeline automates the entire data generation process required to train the model effectively. It includes:
    * Defining Handlers – outlining the logic and schema for each handler type
    * Generating Data – creating the initial structured data points and enriching them with context-specific fields to simulate realistic scenarios.
    * Validating Schema and Logic – ensuring data completeness, consistency, and alignment with handler expectations
    * Producing Refined, Structured Datasets – ready for downstream training and evaluation

These steps collectively produce the high-quality, task-specific datasets required to train and evaluate the Router LLM’s performance across diverse decision-making and tool-usage situations

---
## Training Data Point Structure
This JSON schema defines the structure for a training data point used in a router llm for the selection system. The system processes a user query, selects an appropriate handler from a handler registry, and generates a response with details about the selected tool, including, and reasoning for the selection.

```
{
  "input": {
    "id": "Uniquely identifies the input request",
    "timestamp": "Records when the request was made",
    "query": "Contains the user's request or question",
    "conversation_summary": "Summarizes prior conversation context",
    "handler_registry": {
      "mcp_tools": "Lists available mcp tools ",
      "worker_agents": "Lists available worker agent",
      "llm_handlers": "Lists available language model ",
      "rag_handlers": "Lists available retrieval-augmented generation handlers ",
      "compiled_at": "Records when the tool registry was last updated",
      "user_id": "Identifies the user making the request",
      "workspace_id": "Identifies the workspace or environment for the request"
    },
    "copilot_id": "Identifies an optional copilot instance (if applicable)",
    "thread_id": "Tracks the conversation thread for continuity"
  },
  "output": {
    "select_handler_type": "Specifies the type of tool selected",
    "handler_name": "Names the selected tool from the registry",
    "server_name": "Identifies the server hosting the selected toolif it is a mcp tool",
    "tool_name": "Provides a user-friendly name for the tool's purpose",
    "copilot_id": "Indicates copilot if it is a rag handler",
    "missing_fields": "Lists required input fields missing from the query",
    "optional_suggestions": "Suggests optional fields to enhance tool performance",
    "suggested_payload": "Indicated the avilable invocation parameters with its values",
    "confidence": "Scores the suitability of the selected tool (0.5 to 1.0)",
    "reasoning": "Explains why the tool was chosen",
    "chain_of_thought": "Details the step-by-step process for tool selection",
    "workspace_preference_override": "Indicates if workspace settings were overridden"
  }
}

```

## Project Structure

```.
├── main.py
├── handler_registry_builder/
    ├── prompts/
        ├── worker-agent  
        ├── mcp_tool
        ├── base_llm
        ├── rag
        ├── domains/   
            ├── worker-agent   
            ├── mcp_tool
            ├── base_llm
            ├── rag  

    ├── handler_registries/
        ├── batch_01
            ├── worker-agent  
            ├── mcp_tool
            ├── base_llm
            ├── rag
    ├── handler.py
    
├── static_fields_builder/
    ├── static_field.py
    ├── static_output
        ├── batch_01
            ├── worker-agent  
            ├── mcp_tool
            ├── base_llm
            ├── rag

├── contextual_fields_builder/
    ├──contextual_fileds.py 
    ├── prompts/
        ├── worker-agent/  
        ├── mcp_tool/
        ├── base_llm/
        ├── rag/
    ├── contextual_output/
        ├── batch_01
            ├── worker-agent/  
                ├── worker_agent.jsonl 
                ├── metadata/ 
                    ├── errors_batch_logs/
                    ├── temp_batches/                   
            ├── mcp_tool
                ├── mcp_tool.jsonl 
                ├── metadata/ 
                    ├── errors_batch_logs/
                    ├── temp_batches/                   
            ├── base_llm
                ├── base_llm.jsonl 
                ├── metadata/ 
                    ├── errors_batch_logs/
                    ├── temp_batches/                   
            ├── rag
                ├── rag.jsonl 
                ├── metadata/ 
                    ├── errors_batch_logs/
                        ├── errors_batch_0_1.log
                    ├── temp_batches/                   
                        ├── batch_request_01.jsonl    
├── data_validation/
    ├──data_validation.py 
    ├── prompts/
        ├── worker_agent.py    
        ├── mcp_tool.py  
        ├── base_llm.py  
        ├── rag.py  
    ├── validated_output/
        ├── batch_01
              ├── mcp_tool.jsonl  
              ├── base_llm.jsonl  
              ├── rag.jsonl  
              ├── worker_agent.jsonl  
              ├── metadata/ 
                ├── worker-agent/  
                    ├── refined /               
                    ├── invalid  /              
                    ├── valid  /               
                    ├── raw_output/
                    ├── temp_batches/                   
                    ├── checkpoint.json 
                ├── mcp_tool/
                    ├── refined /               
                    ├── invalid  /              
                    ├── valid  /               
                    ├── raw_output/
                    ├── temp_batches/                   
                    ├── checkpoint.json 
                
├── add_handlers/
    ├──add_handlers.py 
        ├── output/
            ├── batch_01    
                ├── mcp_tool.jsonl  
                ├── base_llm.jsonl  
                ├── rag.jsonl  
                ├── worker_agent.jsonl  
├── utils/
    ├── utils.py/
├── dataset/
    ├── batches/
        ├── batches_01/
            ├── batches_01.jsonl
    ├── final_dataset/
        ├── final_dataset.py
        
└── README.md
└── pipeline.log
└── requirement.txt
```


## 🚀 How It Works

The pipeline executes each handler type in a separate thread, allowing multiple handler types (e.g., rag, worker_agent, base_llm) to be processed concurrently. Within each thread, the full pipeline—from hander creation to data merging—is executed sequentially for that specific handler type, enabling parallel workflows while preserving step-wise order within each one.

### The pipeline consists of 5 steps for each handler type:

1. **Defining Handlers**
   This step initializes the rich set of handler definitions for each handler type (rag, base_llm, mcp_tool, worker_agent). These handlers are defined including metadata, capabilities, and invocation requirements based on domain-specific use cases, forming the foundation for subsequent data generation steps.

2. **Initial Schema Generation**
   This step creates the initial data structure (or skeleton) for each handler by initializing the basic schema. Initial schemas are generated, and possible fields are assigned specific values for each handler defined in the previous stage.

3. **Contextual Field Generation**
   This step enriches the initial data skeletons from Step 2 by generating dynamic, intelligent, context-specific fields such as queries, conversation summaries, chain-of-thought (CoT) reasoning, suggested payloads, and missing information sections using Gemini-based batch LLM processing. For each input, the pipeline generates four distinct and diverse versions of these contextual fields, providing multiple variations of the data point from a single input to improve robustness and diversity in training or evaluation.

4. **Validation**
   This step performs schema and logical validation on each entry—including both static and contextual fields—to ensure correctness, completeness, and adherence to the expected schema for each handler type. 
    - If the entry passes all checks without issues, it is marked as **VALID** with no corrections and includes the original data. 
    - If minor issues are found, the entry is **REFINED** by applying necessary corrections, which are recorded in the corrections field along with the updated data. 
    - If the entry fails validation and cannot be corrected automatically, it is labeled **INVALID**, with an explanation of why refinement was not possible, and the original data is preserved for review.

Example validation statuses look like:

* **VALID**: `{"status": "VALID", "corrections": "", "data": <original_data>}`
* **REFINED**: `{"status": "REFINED", "corrections": "Description of changes made", "data": <refined_data>}`
* **INVALID**: `{"status": "INVALID", "corrections": "Reason why it cannot be refined", "data": <original_data>}`

All results are logged for transparency and future analysis.

---
5. **Handler Appending**
  This step integrates the validated data entries with their corresponding handler definitions from Step 1, dynamically appending 6 to 10 handlers per handler registry. The result is a unified handler registry that serves as a centralized catalog for each handler type.
   
6. **Saving final data**
    Final data entries are saved batch-wise and appended to the final data .jsonl file.

---

## Supported Handler Types
* `rag`
* `base_llm`
* `worker_agent`
* `mcp_tool`

---

## 🛠️ Requirements

* Python 3.8+
* Google GenAI SDK (`google.generativeai`)
* `click`

* Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
---

## Usage

Run the full pipeline for all handler types with a given batch:
    ```bash
    python main.py --batch <batch_id> dataset_size <number of datapoints needed>
    ```

Example:
    ```bash
    python main.py --version batch_10 --dataset_size 12000
    ```
---

## Configuration

Update your API keys in main.py. Each handler type can be assigned a separate API key to support concurrent processing across multiple workflows:

```python
API_KEYS = {
    "rag": "<ADD_YOUR_API_KEY>",
    "base_llm": "<ADD_YOUR_API_KEY>",
    "worker_agent": "<ADD_YOUR_API_KEY>",
    "mcp_tool": "<ADD_YOUR_API_KEY>",
}

```
This setup enables parallel execution of the pipeline for different handler types, each using its own dedicated API key.

---

## 📤 Output Structure

Each stage of the pipeline generates outputs in a batch-wise directory structure, organized by handler type. For example, assuming the handler type is rag and the batch is batch_01, the outputs are stored in the following folders:

```.
├── handler_registry_builder/
│   └── handler_registries/batch_01/rag/          # Handler definitions
├── static_fields_builder/
│   └── static_output/batch_01/rag/               # Static field outputs
├── contextual_fields_builder/
│   └── contextual_output/batch_01/rag/           # Contextual field outputs and metadata
├── data_validation/
│   └── validated_output/batch_01/rag/            # Validated entries
├── add_handlers/
│   └── final_output/batch_01/rag/                # Merged handler entries
├── dataset/
│   ├── batches/batch_01/                         # Intermediate data batches
│   └── final_dataset/                            # Final compiled dataset

```

## Sample Data Point Generation Workflow (Handler Type: agent)
This example walks through how a single agent handler (e.g., Stitch) progresses through the pipeline — from the initial handler definition to a fully enriched and validated data entry. Each step below includes a description of what happens to this data point at that stage.

####  Step 1: Define the Handler 
In this step, the core attributes of the worker agent handler is  defined. This includes its name, description, endpoint, payload schema, and any workspace or system identifiers.

```
{
  "name": "Stitch",
  "description": "Intelligently maps the schema of a source dataset to a target schema, suggesting field-to-field connections. Requires the source and target dataset identifiers.",
  "http_endpoint": "https://schema-mapper.internal/api/v1/suggest/mapping",
  "payload_schema": {
    "type": "object",
    "properties": {
      "source_dataset_id": {
        "title": "Source Dataset ID",
        "type": "string"
      },
      "target_dataset_id": {
        "title": "Target Dataset ID",
        "type": "string"
      }
    },
    "required": ["source_dataset_id", "target_dataset_id"]
  },
  "workspace_id": "7b8c9d0e-1f2a-4b4c-5d6e-7f8a9b0c1d2e"
}

```

#### Step 02 :  Initialize the Data Point
This is the first version of the data point to be processed wraping the handler definition into a structured data point.

```
{
    "input": {
        "id": "753b8384-f93e-4151-b1d7-fff099fa26a8",
        "timestamp": "2023-12-11T06:51:34.767856",
        "query": "",
        "conversation_summary": "",
        "handler_registry": [
            {
                "mcp_tools": [ ],
                "worker_agents": [
                    {
                        "name": "Stitch",
                        "description": "Intelligently maps the schema of a source dataset to a target schema, suggesting field-to-field connections. Requires the source and target dataset identifiers.",
                        "http_endpoint": "https://schema-mapper.internal/api/v1/suggest/mapping",
                        "payload_schema": {
                            "type": "object",
                            "properties": {
                                "source_dataset_id": {
                                    "title": "Source Dataset ID",
                                    "type": "string"
                                },
                                "target_dataset_id": {
                                    "title": "Target Dataset ID",
                                    "type": "string"
                                }
                            },
                            "required": [
                                "source_dataset_id",
                                "target_dataset_id"
                            ]
                        },
                        "workspace_id": "7b8c9d0e-1f2a-4b4c-5d6e-7f8a9b0c1d2e"
                    }
                ],
                "llm_handlers": [],
                "rag_handlers": [],
                "compiled_at": "2023-12-09T17:18:42.767856",
                "user_id": "fa255dc9-da62-480b-ace9-0a747e4f2a29",
                "workspace_id": "36876599-3f6b-428f-9ae7-367fc0bb5409"
            }
        ],
        "copilot_id": null,
        "thread_id": "ce549e3b-4ce5-4819-9b3e-a5a802dd9aa0"
    },
    "output": {
        "select_handler_type": "worker_agent",
        "handler_name": "Stitch",
        "server_name": null,
        "tool_name": null,
        "copilot_id": null,
        "missing_fields": [],
        "optional_suggestions": [],
        "suggested_payload": {},
        "confidence": 0.728923,
        "reasoning": "",
        "chain_of_thought": [
            ],
        "workspace_preference_override": false
    }
}
```

#### Step 03: Enrich with Contextual Fields
Using LLMs, the pipeline generates rich, realistic contextual fields These simulate how a user might interact with the handler in practice and include elements like query, conversation_summary,reasoning, chain of thought,suggested_payload, missing_fields , optional_suggestions

```
{
    "input": {
        "id": "753b8384-f93e-4151-b1d7-fff099fa26a8",
        "timestamp": "2023-12-11T06:51:34.767856",
        "query": "I need to prepare a new data import. Can you suggest a schema mapping for our standard `prod_inventory_table`?",
        "conversation_summary": "User is preparing to integrate a new supplier's data feed. The target for this data is the main production inventory table (`prod_inventory_table`). They haven't specified the source dataset yet.",
        "handler_registry": [
            {
                "mcp_tools": [  ],
                "worker_agents": [
                    {
                        "name": "Stitch",
                        "description": "Intelligently maps the schema of a source dataset to a target schema, suggesting field-to-field connections. Requires the source and target dataset identifiers.",
                        "http_endpoint": "https://schema-mapper.internal/api/v1/suggest/mapping",
                        "payload_schema": {
                            "type": "object",
                            "properties": {
                                "source_dataset_id": {
                                    "title": "Source Dataset ID",
                                    "type": "string"
                                },
                                "target_dataset_id": {
                                    "title": "Target Dataset ID",
                                    "type": "string"
                                }
                            },
                            "required": [
                                "source_dataset_id",
                                "target_dataset_id"
                            ]
                        },
                        "workspace_id": "7b8c9d0e-1f2a-4b4c-5d6e-7f8a9b0c1d2e"
                    }
                 ],
                "llm_handlers": [],
                "rag_handlers": [],
                "compiled_at": "2023-12-09T17:18:42.767856",
                "user_id": "fa255dc9-da62-480b-ace9-0a747e4f2a29",
                "workspace_id": "36876599-3f6b-428f-9ae7-367fc0bb5409"
            }
        ],
        "copilot_id": null,
        "thread_id": "ce549e3b-4ce5-4819-9b3e-a5a802dd9aa0"
    },
    "output": {
        "select_handler_type": "worker_agent",
        "handler_name": "Stitch",
        "server_name": null,
        "tool_name": null,
        "copilot_id": null,
        "missing_fields": [
            "source_dataset_id"
        ],
        "optional_suggestions": [],
        "suggested_payload": {
            "source_dataset_id": "missing",
            "target_dataset_id": "prod_inventory_table",
            "summary": "User wants to get a schema mapping for the target dataset 'prod_inventory_table'."
        },
        "confidence": 0.728923,
        "reasoning": "The user intends to perform schema mapping, which correctly points to the `Stitch` worker agent. While the `target_dataset_id` is clearly identified, the required `source_dataset_id` is missing from both the query and the conversation history. The agent cannot be invoked without it.",
        "chain_of_thought": [
            "The user's request is to get a 'schema mapping' for the `prod_inventory_table`.",
            "This intent aligns with the `Stitch` worker agent, which suggests field-to-field connections between schemas.",
            "I examined the agent's schema requirements: `source_dataset_id` and `target_dataset_id` are both mandatory.",
            "The `target_dataset_id` ('prod_inventory_table') is explicitly mentioned in the query and reinforced in the summary.",
            "However, after reviewing both the query and the conversation summary, I found no mention of a `source_dataset_id`.",
            "Since a required parameter is missing, the agent cannot be executed.",
            "The system's confidence score of 0.728923 reflects a high certainty in the tool's relevance, but the inputs are incomplete."
        ],
        "workspace_preference_override": false
    }
}
```

### Step 04 : Validaton 
The enriched data point is validated to ensure that all required fields are present, data types and values are consistent, structured reasoning is logically sound, and the suggested payload aligns with the defined schema. If any issues are detected, the entry is flagged for refinement and updated with the necessary improvements.
In the example below, the data point passed all checks during the refinement process, so no modifications were needed. So it is marked as VALID without requiring any changes.

```
{"status": "VALID",
"corrections": "", 
"data": "
    "input": {
        "id": "753b8384-f93e-4151-b1d7-fff099fa26a8",
        "timestamp": "2023-12-11T06:51:34.767856",
        "query": "I need to prepare a new data import. Can you suggest a schema mapping for our standard `prod_inventory_table`?",
        "conversation_summary": "User is preparing to integrate a new supplier's data feed. The target for this data is the main production inventory table (`prod_inventory_table`). They haven't specified the source dataset yet.",
        "handler_registry": [
            {
                "mcp_tools": [  ],
                "worker_agents": [
                    {
                        "name": "Stitch",
                        "description": "Intelligently maps the schema of a source dataset to a target schema, suggesting field-to-field connections. Requires the source and target dataset identifiers.",
                        "http_endpoint": "https://schema-mapper.internal/api/v1/suggest/mapping",
                        "payload_schema": {
                            "type": "object",
                            "properties": {
                                "source_dataset_id": {
                                    "title": "Source Dataset ID",
                                    "type": "string"
                                },
                                "target_dataset_id": {
                                    "title": "Target Dataset ID",
                                    "type": "string"
                                }
                            },
                            "required": [
                                "source_dataset_id",
                                "target_dataset_id"
                            ]
                        },
                        "workspace_id": "7b8c9d0e-1f2a-4b4c-5d6e-7f8a9b0c1d2e"
                    }
                 ],
                "llm_handlers": [],
                "rag_handlers": [],
                "compiled_at": "2023-12-09T17:18:42.767856",
                "user_id": "fa255dc9-da62-480b-ace9-0a747e4f2a29",
                "workspace_id": "36876599-3f6b-428f-9ae7-367fc0bb5409"
            }
        ],
        "copilot_id": null,
        "thread_id": "ce549e3b-4ce5-4819-9b3e-a5a802dd9aa0"
    },
    "output": {
        "select_handler_type": "worker_agent",
        "handler_name": "Stitch",
        "server_name": null,
        "tool_name": null,
        "copilot_id": null,
        "missing_fields": [
            "source_dataset_id"
        ],
        "optional_suggestions": [],
        "suggested_payload": {
            "source_dataset_id": "missing",
            "target_dataset_id": "prod_inventory_table",
            "summary": "User wants to get a schema mapping for the target dataset 'prod_inventory_table'."
        },
        "confidence": 0.728923,
        "reasoning": "The user intends to perform schema mapping, which correctly points to the `Stitch` worker agent. While the `target_dataset_id` is clearly identified, the required `source_dataset_id` is missing from both the query and the conversation history. The agent cannot be invoked without it.",
        "chain_of_thought": [
            "The user's request is to get a 'schema mapping' for the `prod_inventory_table`.",
            "This intent aligns with the `Stitch` worker agent, which suggests field-to-field connections between schemas.",
            "I examined the agent's schema requirements: `source_dataset_id` and `target_dataset_id` are both mandatory.",
            "The `target_dataset_id` ('prod_inventory_table') is explicitly mentioned in the query and reinforced in the summary.",
            "However, after reviewing both the query and the conversation summary, I found no mention of a `source_dataset_id`.",
            "Since a required parameter is missing, the agent cannot be executed.",
            "The system's confidence score of 0.728923 reflects a high certainty in the tool's relevance, but the inputs are incomplete."
        ],
        "workspace_preference_override": false
    }
}
```
#### step 05 :  Building the final handler registry
The validated data is merged with the original handler definition to create a unified and complete handler registry entry.
```
{
    "input": {
        "id": "753b8384-f93e-4151-b1d7-fff099fa26a8",
        "timestamp": "2023-12-11T06:51:34.767856",
        "query": "I need to prepare a new data import. Can you suggest a schema mapping for our standard `prod_inventory_table`?",
        "conversation_summary": "User is preparing to integrate a new supplier's data feed. The target for this data is the main production inventory table (`prod_inventory_table`). They haven't specified the source dataset yet.",
        "handler_registry": [
            {
                "mcp_tools": [
                    {
                        "name": "fetch_employee_payslip_tool",
                        "server_name": "ErpPayrollMCP",
                        "description": "Retrieves a specific payslip for an employee for a given pay period. :param employee_id: The ID of the employee whose payslip is being requested. :param pay_period_id: The identifier for the specific pay period. :return: A structured object containing detailed payslip information including gross pay, deductions, and net pay. (Server: ErpPayrollMCP)",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "employee_id": {"title": "Employee ID","type": "string"},
                                "pay_period_id": {  "title": "Pay Period ID","type": "string"}
                            },
                            "required": ["employee_id", "pay_period_id"]
                        }
                    }
                    
                    }
                ],
                "worker_agents": [
                    {
                        "name": "Stitch",
                        "description": "Intelligently maps the schema of a source dataset to a target schema, suggesting field-to-field connections. Requires the source and target dataset identifiers.",
                        "http_endpoint": "https://schema-mapper.internal/api/v1/suggest/mapping",
                        "payload_schema": {
                            "type": "object",
                            "properties": {
                                "source_dataset_id": {"title": "Source Dataset ID","type": "string"},
                                "target_dataset_id": {"title": "Target Dataset ID","type": "string"
                                }
                            },
                            "required": [ "source_dataset_id", "target_dataset_id"
                            ]
                        },
                        "workspace_id": "7b8c9d0e-1f2a-4b4c-5d6e-7f8a9b0c1d2e"
                    },
                    {
                        "name": "Pivot",
                        "description": "Executes an ad-hoc SQL query against a specified data warehouse and returns the results. This agent is for exploratory analysis. Requires the data warehouse ID and the SQL query string.",
                        "http_endpoint": "https://query-gateway.corp/api/v1/execute/ad_hoc",
                        "payload_schema": {
                            "type": "object",
                            "properties": {
                                "data_warehouse_id": {"title": "Data Warehouse ID","type": "string"
                                },
                                "sql_query": {"title": "SQL Query","type": "string"
                                },
                                "max_rows": {"title": "Max Rows to Return","type": "integer"
                                }
                            },
                            "required": ["data_warehouse_id","sql_query"
                            ]
                        },
                        "workspace_id": "f8a9b0c1-d2e3-4f4a-5b6c-7d8e9f0a1b2c"
                    },
                  
                ],
                "llm_handlers": [
                    {
                        "name": "deepseek_edge_case_generator",
                        "description": "Analyzes code to identify and generate test cases specifically targeting boundary conditions, error handling, and other edge cases.",
                        "model_provider": "Deepseek",
                        "model_name": "deepseek-reasoner",
                        "is_workspace_default": false
                    },
                    {
                        "name": "llama3_story_starter",
                        "description": "Generates an opening paragraph for a story to help overcome writer's block.",
                        "model_provider": "META",
                        "model_name": "Llama-3.3-70B-Instruct",
                        "is_workspace_default": false
                    }                
                ],
                "rag_handlers": [
                    {
                        "name": "promo_code_validator",
                        "description": "Validates a promotional code against a set of rules, checking for expiration, applicability to cart items, and single-use restrictions.",
                        "handler_payload": {
                            "copilot_id": "e1f2a3b4-c5d6-7890-1234-f12345678901"
                        }
                    },
                    {
                        "name": "site_feasibility_matrix",
                        "description": "Matches protocol requirements against a database of clinical sites' capabilities, investigator experience, and past performance metrics.",
                        "handler_payload": {
                            "copilot_id": "e5f6a7b2-3c4d-5e6f-9a0b-1c2d3e4f5a6b"
                        }
                    },
                   
                    }
                ],
                "compiled_at": "2023-12-09T17:18:42.767856",
                "user_id": "fa255dc9-da62-480b-ace9-0a747e4f2a29",
                "workspace_id": "36876599-3f6b-428f-9ae7-367fc0bb5409"
            }
        ],
        "copilot_id": null,
        "thread_id": "ce549e3b-4ce5-4819-9b3e-a5a802dd9aa0"
    },
    "output": {
        "select_handler_type": "worker_agent",
        "handler_name": "Stitch",
        "server_name": null,
        "tool_name": null,
        "copilot_id": null,
        "missing_fields": [
            "source_dataset_id"
        ],
        "optional_suggestions": [],
        "suggested_payload": {
            "source_dataset_id": "missing",
            "target_dataset_id": "prod_inventory_table",
            "summary": "User wants to get a schema mapping for the target dataset 'prod_inventory_table'."
        },
        "confidence": 0.728923,
        "reasoning": "The user intends to perform schema mapping, which correctly points to the `Stitch` worker agent. While the `target_dataset_id` is clearly identified, the required `source_dataset_id` is missing from both the query and the conversation history. The agent cannot be invoked without it.",
        "chain_of_thought": [
            "The user's request is to get a 'schema mapping' for the `prod_inventory_table`.",
            "This intent aligns with the `Stitch` worker agent, which suggests field-to-field connections between schemas.",
            "I examined the agent's schema requirements: `source_dataset_id` and `target_dataset_id` are both mandatory.",
            "The `target_dataset_id` ('prod_inventory_table') is explicitly mentioned in the query and reinforced in the summary.",
            "However, after reviewing both the query and the conversation summary, I found no mention of a `source_dataset_id`.",
            "Since a required parameter is missing, the agent cannot be executed.",
            "The system's confidence score of 0.728923 reflects a high certainty in the tool's relevance, but the inputs are incomplete."
        ],
        "workspace_preference_override": false
    }
}

```
  
  #### Saving data 
  Final data entries are saved batch-wise and appended to the final data .jsonl file.
  
  ## Key Features

- Supports batch-wise execution for scalability and organization.
- Designed for concurrent processing with separate API key configurations per handler type.
- Clean directory structure for step-by-step tracking of output at each pipeline stage.
