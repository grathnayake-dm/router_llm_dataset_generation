WORKER_AGENT_PROMPT ="""

This process is designed to generate a training dataset for responsible for routing user queries to the appropriate Worker Agent in an enterprise system.
You are simulating a Router LLM that receives user input and determines the most suitableBase worker agent to invoke based on a registry of handlers. This dataset captures realistic  decision patterns for use in downstream LLM-based orchestration systems.
Key Concepts : 
1. worker Agent Handlers
  -Each worker agent handler entry in the handler_registry represents a  worker agent with specific capabilities and metadata. Fields typically include:
   - Fields typically include:
     - `name`: Unique name of the tool.
     - `description`: A brief explanation of what the agent does, including its primary function and when it should be used..
     - `http_endpoint`: The HTTP URL where the service can be accessed or invoked. This endpoint accepts requests using the provided payload schema.
     - `payload_schema`:  schema definition (based on JSON Schema) describing the required structure of the input payload the tool accepts:
       - `required`: A list of field names that must be provided fro the agent invocation.
       - `properties`: A dictionary where each key represents an input field and its metadata (e.g., type, title).   
       -handler_registry: {"name": "analyze_error_log_for_root_cause", "description": "Analyzes a given application error log to identify the root cause of an issue. It requires the raw log content and the type of application (e.g., 'Java', 'Node.js') to provide a detailed analysis and suggest potential fixes.", "http_endpoint": "https://debugger.corp-tools.net/v2/logs/analyze", "payload_schema": {"type": "object", "properties": {"log_content": {"title": "Log Content", "type": "string"}, "application_type": {"title": "Application Type", "type": "string"}}, "required": ["log_content", "application_type"]}, "workspace_id": "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e"}

For each  sample, we simulate how a Router LLM would behave by starting from the available workder agent) in the handler_registry and generating a realistic user interaction that would lead to selecting that handler.
The steps are:
    -Start from a given worker agent handler  in the handler_registry.
    Extract its:
        -name
        -description
        -http_endpoint
        -payload_schema
        - `required`: 
        - `properties`:
        - workspace_id
    -Based on the handler’s description and capabilities, generate:
    -A natural-sounding user query that would require this handler.
    -A conversation_summary simulating context from previous turns.
    - handle missing_fields, suggested_payload, optional_suggetion according to the way the conversation_summary and user query is implemented
    -Create structured fields that simulate how a Router LLM would explain its selection:
    -reasoning: Why was this handler picked?
    -chain_of_thought: Step-by-step reasoning chain that shows matching between query and handler.
    -Insert generated fields back into the original input/output JSON structure, to complete the training example.

## TASK OVERVIEW:
- This task involves a two-stage process for each INPUT_JSON provided:
    -STAGE 1 — Generate Content: Based on the INPUT_JSON, generate 4 unique and dynamic data entries. Each entry will contain a user query, the reasoning for the routing decision, and a detailed chain-of-thought.
    -STAGE 2 — Update and Finalize JSON: For each of the 4 generated entries, create a deep copy of the original INPUT_JSON and inject the generated content into the appropriate fields.

### STAGE 1
    - You will be given  a SAMPLE INPUT JSONL as follows:
{"input": {"id": "1a28002b-5f5d-46a9-8458-c5ec28f76ccb", "timestamp": "2025-03-20T14:49:36.125555", "query": "", "conversation_summary": "", "handler_registry": {"mcp_tools": [], "worker_agents": [{"name": "proactive_risk_identifier", "description": "Predicts potential project risks like delays or resource shortages by analyzing current project data and historical trends. Requires the project ID to analyze.", "http_endpoint": "https://risk-sentinel.monday.com/api/v2/projects/risks/predict", "payload_schema": {"type": "object", "properties": {"project_id": {"title": "Project ID", "type": "string"}, "risk_category_filter": {"title": "Risk Category Filter", "type": "string"}}, "required": ["project_id"]}, "workspace_id": "e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b"}], "llm_handlers": [], "rag_handlers": [], "compiled_at": "2025-03-19T18:38:59.125555", "user_id": "1f71b28a-08a3-474a-abee-ae6ea4909a08", "workspace_id": "2bc3faa6-dcc7-404a-ad8b-dcf3dc4701c3"}, "copilot_id": null, "thread_id": "e3d69e32-2c81-4ad8-9a36-a33b2c7023f9"}, "output": {"select_handler_type": "worker_agent", "handler_name": "proactive_risk_identifier", "server_name": null, "tool_name": null, "copilot_id": null, "missing_fields": [], "optional_suggestions": [], "suggested_payload": {}, "confidence": 0.604968, "reasoning": "", "chain_of_thought": [], "workspace_preference_override": false}}

#### Generate 4 Data Points
    -Create four (4) data points following the structure below:

    I. Complete Parameter Coverage (2 Data Points)
    -Generate two (2) data points where all required fields are present. Use any two of the following inclusion types:
        - All required fields are included in both conversation_summary and query.
        - All required fields are included only in query.
        - All required fields are included only in conversation_summary.

    II. Missing Parameter Scenarios (2 Data Points)
    - Generate two (2) data points where one or more required fields are missing. Choose any two from the following missing field cases:
        - Required fields are missing in both conversation_summary and query.
        - Required fields are missing only in query.
        - Required fields are missing only in conversation_summary.


-For each INPUT_JSON, generate four diverse output samples simulating how a user might trigger the selected handler. Each sample must include the following fields:
  -Required Fields per Sample:
    -query: A natural-sounding user query that would appropriately invoke the selected handler. This may contain implicit or explicit references to required schema parameters.
    -conversation_summary: A realistic summary of prior conversation context, helping justify parameter grounding or task continuity.
    - handle missing_fields, suggested_payload, optional_suggetion according to the way the conversation_summary and user query is implemented {based on how required parameters are applied on query and conversation memory}
    -reasoning: A concise justification explaining why the selected handler is the most appropriate match for the query.
    -chain_of_thought (CoT): A step-by-step explanation of how the Router llm  analyzed the query, considered handler capabilities, and validated parameter readiness to select worker agent.
  -Each of the 4 samples should simulate a distinct and realistic user scenario, varying in phrasing, specificity  to ensure dataset diversity.

{
  "query": "<string>",                     // Natural-language user request
  "conversation_summary": "<string>",     // Prior context simulating memory
  "missing_fields": ["<string>", ...],    // List of required fields that are missing
  "optional_suggestions": ["<string>", ...], // List of optional fields not required but possibly useful
  "suggested_payload": {                  // Key-value pairs of parameters based on what user has provided
    "<key>": "<value | 'missing'>"    
    <summary> : <value>  // this key value pare is applide when few of the required paramera are missing only
  },
  "reasoning": "<string>",                // Justification for why this handler is selected
  "chain_of_thought": [                   // Multi-step reasoning process
    "<string>",                           // Step 1
    "<string>",                           // Step 2
    "...",
    "<final handler selection conclusion>"
  ]
}


Each generated data point must strictly adhere to the schema below. This ensures consistent formatting and supports downstream model training and evaluation.
Example Output Entry :

- Example 01 Few the required parameters are missing 

{
  "query": "We’re seeing performance issues with the billing application again. Can you check the status of the latest incident ticket for PROD-19?",
  "conversation_summary": "The user reported intermittent slowdowns in the billing application on PROD-19 earlier today. They confirmed the environment ID as PROD-19 and provided the ITSM API token for authentication as 58965MKI-ko . The issue is critical as it impacts end-of-month reconciliations.",
  "missing_fields": [
    "incident_id"
  ],
  "optional_suggestions": [
    "priority_level"
  ],
  "suggested_payload": {
    "incident_id": "missing",
    "environment_id": "PROD-19",
    "itsm_api_token": "58965MKI-ko",
    "summary": "Check the status of an incident ticket for the billing application in the PROD-19 environment."
  },
  "reasoning": "The user's request to check the status of an incident ticket aligns with the `check_incident_status` Worker Agent, but the specific `incident_id` is missing, preventing invocation. The environment ID and API token are provided, but complete parameter coverage is required for execution.",
  "chain_of_thought": [
    "The user is requesting a status update on an incident ticket related to performance issues in the billing application.",
    "I identified the `check_incident_status` Worker Agent as the best match, as it retrieves incident ticket details from the ITSM system.",
    "The agent requires `incident_id`, `environment_id`, and `itsm_api_token` as mandatory parameters.",
    "The conversation summary provides the `environment_id` (PROD-19) and confirms the availability of the `itsm_api_token`.",
    "The query does not specify the `incident_id`, and it’s not mentioned in the conversation summary either.",
    "The optional parameter `priority_level` could enhance the request but is not required.",
    "Due to the missing `incident_id`, the Worker Agent cannot be invoked at this time.",
    "The confidence score of 0.72 reflects a clear understanding of the intent but incomplete inputs for execution."
  ]
}

- Example 02 - All the required parameters are included 

{
  "query": "Please validate the change request CR-3921 for the firewall update in the QA-07 environment. Use the compliance ruleset SEC-2025-Q2 and the ITSM API token for authentication.",
  "conversation_summary": "The user is preparing for a firewall configuration update scheduled for next week. They previously submitted change request CR-3921 for the QA-07 environment and confirmed the compliance ruleset SEC-2025-Q2. The ITSM API token is available for system access(58965MKI-ko).",
  "tool_name": "validate_change_request",
  "missing_fields": [],
  "optional_suggestions": [
    "validation_report_format"
  ],
  "suggested_payload": {
    "change_request_id": "CR-3921",
    "environment_id": "QA-07",
    "compliance_ruleset": "SEC-2025-Q2",
    "itsm_api_token": "58965MKI-ko"
  },
  "reasoning": "The request to validate a change request aligns perfectly with the `validate_change_request` Worker Agent. All required parameters—change_request_id, environment_id, compliance_ruleset, and itsm_api_token—are provided, making the agent ready for invocation.",
  "chain_of_thought": [
    "The user is requesting validation of a change request for a firewall update.",
    "The `validate_change_request` Worker Agent is the best match, as it automates change request validation in the ITSM system.",
    "The agent requires `change_request_id`, `environment_id`, `compliance_ruleset`, and `itsm_api_token`.",
    "The query provides `change_request_id` (CR-3921), `environment_id` (QA-07), and `compliance_ruleset` (SEC-2025-Q2), and confirms the `itsm_api_token` is available.",
    "The conversation summary reinforces these parameters, ensuring complete coverage.",
    "The optional parameter `validation_report_format` could be suggested to customize the output, but it’s not required.",
    "With all required parameters present, the Worker Agent is fully prepared for execution.",
    "The confidence score of 0.98 indicates high certainty in agent selection and readiness."
  ]
}

### STAGE 2 
- Apply generated fields to INPUT_JSON:
- For each generated output entry in stage 1:
    - 1. Create a deep copy of the original INPUT_JSON.
    - 2. Replace or update the corresponding fields in the deep copy with the stage 1  values as follows:
           - input.query → from generated query
           - input.conversation_summary → from generated conversation_summary
           - output.missing_fields -> from generated missing_fields
           - output.optional_suggestions → from generated optional_suggestions
           - output.suggested_payload → from generated suggested_payload
           - output.reasoning → from generated reasoning
           - output.chain_of_thought → from generated chain_of_thought
- This yields 4 updated INPUT_JSON objects, each representing one enriched and realistic scenario.
- All the  other fields in the original INPUT_JSON remain unchanged .
-The final output should be a list of 4 modified JSON objects, each being a fully updated copy of the original INPUT_JSON,  with the following updated values  in its input and  output fields replaced using the generated schema fields.

{
  "input": {
    "query": "<replaced with Stage 2 → query>",
    "conversation_summary": [
      "<replaced with Stage 2 → conversation_summary item 1>",
      "<replaced with Stage 2 → conversation_summary item 2>"
    ],
    "other_fields_preserved": "..."
  },
  "output": {
    "missing_fields" :  "<replaced with Stage 2 → missing_fields>",
    "optional_suggestions": [
      "<replaced with Stage 2 → optional_suggestions value>"
    ],
    "suggested_payload": {
      "<replaced with Stage 2 → payload_key>": "<value : "missing">",

    },
    "reasoning": "<replaced with Stage 2 → reasoning>",
    "chain_of_thought": [
      "<replaced with Stage 2 → chain_of_thought 1>",
      "<replaced with Stage 2 → chain_of_thought 2>",
      "...",
      "<final conclusion>"
    ],

  }
}


Final Output Format (After Stage 2)
final output must strictly preserve the structure of the original INPUT_JSON schema. Only the specified fields should be updated with values from Stage 2, while all other keys and nesting should remain exactly the same to ensure structural consistency.


- Example 01 Few the required parameters are missing 
  {
    "input": {
        "id": "50bb1913-ae7d-45db-8099-d2febcd8ef95",
        "timestamp": "2024-06-13T21:48:01.125167",
        "query": "We need to run the optimizer on the 'Market-Expansion-APAC' project.",
        "conversation_summary": "User has been assigned as the lead for the 'Market-Expansion-APAC' project (ID: PROJ-APAC-2024-07). They are reviewing the initial budget and timeline.",
        "handler_registry": {
            "mcp_tools": [],
            "worker_agents": [
                {
                    "name": "resource_allocation_optimizer",
                    "description": "Optimizes the allocation of personnel and equipment for a given project based on requirements, skills, and cost, aiming to minimize waste. Requires the project ID and resource types to consider.",
                    "http_endpoint": "https://smartsheet-allocator.io/api/v3/projects/resources/optimize",
                    "payload_schema": {
                        "type": "object",
                        "properties": {
                            "project_id": {
                                "title": "Project ID",
                                "type": "string"
                            },
                            "resource_types": {
                                "title": "Resource Types",
                                "type": "string"
                            },
                            "optimization_goal": {
                                "title": "Optimization Goal",
                                "type": "string"
                            }
                        },
                        "required": [
                            "project_id",
                            "resource_types"
                        ]
                    },
                    "workspace_id": "c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f"
                }
            ],
            "llm_handlers": [],
            "rag_handlers": [],
            "compiled_at": "2024-06-13T05:30:31.125167",
            "user_id": "2b005ed3-7a3b-4014-9a25-1e7c93f37a79",
            "workspace_id": "3fecd56d-06b5-435d-aaa5-27a5bcfa8d1f"
        },
        "copilot_id": null,
        "thread_id": "e9e3ee25-c6ba-4dd7-a019-a02911bd6957"
    },
    "output": {
        "select_handler_type": "worker_agent",
        "handler_name": "resource_allocation_optimizer",
        "server_name": null,
        "tool_name": null,
        "copilot_id": null,
        "missing_fields": [
            "resource_types"
        ],
        "optional_suggestions": [
            "optimization_goal"
        ],
        "suggested_payload": {
            "project_id": "PROJ-APAC-2024-07",
            "resource_types": "missing",
            "summary": "User wants to optimize resources for the 'Market-Expansion-APAC' project."
        },
        "confidence": 0.69052,
        "reasoning": "The user's intent to use the 'optimizer' for a specific project clearly points to the `resource_allocation_optimizer` agent. However, the agent cannot be invoked because the required `resource_types` parameter is missing. The `project_id` was found, but more information is needed.",
        "chain_of_thought": [
            "I identified the user's intent is to 'run the optimizer' on a project.",
            "The `resource_allocation_optimizer` agent is the only handler that matches this function.",
            "I checked the agent's schema, which requires `project_id` and `resource_types`.",
            "The conversation summary provides the `project_id` as 'PROJ-APAC-2024-07'.",
            "Neither the query nor the summary specifies which `resource_types` (e.g., personnel, equipment, software licenses) to optimize.",
            "Therefore, the `resource_types` field is missing.",
            "Since one required parameter is missing, the agent cannot be invoked. The system needs to ask the user for clarification.",
            "The confidence score of 0.69052 indicates a good match in intent, but the inputs are incomplete for execution."
        ],
        "workspace_preference_override": false
    }
}

- Example 02 - All the required parameters are included 
  {
      "input": {
          "id": "50bb1913-ae7d-45db-8099-d2febcd8ef95",
          "timestamp": "2024-06-13T21:48:01.125167",
          "query": "For that 'Infra-Upgrade-Q3' initiative, let's optimize the equipment and on-site staff.",
          "conversation_summary": "The user is currently discussing the 'Infra-Upgrade-Q3' project (ID: 98a65f4b-7e8d-4c3b-9a1f-0d2c1b3e4a5d). The main goal is to reduce operational overhead.",
          "handler_registry": {
              "mcp_tools": [],
              "worker_agents": [
                  {
                      "name": "resource_allocation_optimizer",
                      "description": "Optimizes the allocation of personnel and equipment for a given project based on requirements, skills, and cost, aiming to minimize waste. Requires the project ID and resource types to consider.",
                      "http_endpoint": "https://smartsheet-allocator.io/api/v3/projects/resources/optimize",
                      "payload_schema": {
                          "type": "object",
                          "properties": {
                              "project_id": {
                                  "title": "Project ID",
                                  "type": "string"
                              },
                              "resource_types": {
                                  "title": "Resource Types",
                                  "type": "string"
                              },
                              "optimization_goal": {
                                  "title": "Optimization Goal",
                                  "type": "string"
                              }
                          },
                          "required": [
                              "project_id",
                              "resource_types"
                          ]
                      },
                      "workspace_id": "c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f"
                  }
              ],
              "llm_handlers": [],
              "rag_handlers": [],
              "compiled_at": "2024-06-13T05:30:31.125167",
              "user_id": "2b005ed3-7a3b-4014-9a25-1e7c93f37a79",
              "workspace_id": "3fecd56d-06b5-435d-aaa5-27a5bcfa8d1f"
          },
          "copilot_id": null,
          "thread_id": "e9e3ee25-c6ba-4dd7-a019-a02911bd6957"
      },
      "output": {
          "select_handler_type": "worker_agent",
          "handler_name": "resource_allocation_optimizer",
          "server_name": null,
          "tool_name": null,
          "copilot_id": null,
          "missing_fields": [],
          "optional_suggestions": [
              "optimization_goal"
          ],
          "suggested_payload": {
              "project_id": "98a65f4b-7e8d-4c3b-9a1f-0d2c1b3e4a5d",
              "resource_types": "equipment, on-site staff"
          },
          "confidence": 0.69052,
          "reasoning": "The `resource_allocation_optimizer` is the correct agent for this task. The `project_id` was identified from the conversation summary, and the `resource_types` were specified in the user's latest query. With all required parameters available, the agent is ready to run.",
          "chain_of_thought": [
              "The user's query asks to 'optimize' specific resources for a project.",
              "This aligns with the `resource_allocation_optimizer` agent's purpose.",
              "The agent requires `project_id` and `resource_types`.",
              "The conversation summary establishes the context, providing the `project_id` as '98a65f4b-7e8d-4c3b-9a1f-0d2c1b3e4a5d'.",
              "The user's new query specifies the `resource_types` as 'equipment, on-site staff'.",
              "The optional parameter `optimization_goal` could be inferred from the summary ('reduce operational overhead'), but it is not explicitly requested for the payload and can be suggested.",
              "All required parameters are gathered from the combination of the summary and query, so the agent is invokable.",
              "The confidence of 0.69052 supports this selection, as the intent is clear and all prerequisites are met."
          ],
          "workspace_preference_override": false
      }
  }


## Critical Warning – Mandatory Output Quality Standards

To ensure the usefulness, realism, and diversity the following strict rules must be followed without exception:

-Avoid Repeating Patterns, Filler Text, and Predictable Values
    -Do not use generic, repetitive, or placeholder-style values that reduce realism and signal synthetic data. This includes:
        -Predictable Numbering:
        -Bad: User1, User2, Item3, ID4
        -Reason: These follow simple, incremental patterns that LLMs easily overfit or ignore.

    -Default or Placeholder Text:
        -Bad: CompanyX, TestName, City1, SampleValue, XYZ123   
        -Reason: These look like scaffolding, not real data — they weaken authenticity.

    -Template-Like Reuse:
        -Bad: Using the same name (John Doe, Jane Smith) or location (New York) across many samples
        -Reason: Lack of variation hurts model exposure to real-world diversity

    -Instead, Use Realistic, Varied, and Contextual Values:
        -Good IDs: VISIT-2025-BLR-QA92Z, REQ-HOSP-NJ-84A2F, c7e35a8f-63dd-4e91-a2fd-bdd7e58ed430 (UUID)
        -Good Names: Priya Menon, Liam Rodriguez, Amara Chen, Oluwaseun Adebayo
        -Good Locations: Columbus, OH, London, Canada, Tallahassee, FL
        -Good Dates/Notes: Routine follow-up for hypertension, Scheduled MRI due to persistent lower back pain
        -Ensure every field (ID, name, city, description, diagnosis, etc.) feels plausible and unique — like real data from different users, places, and situations.

    -ID Generation Guidelines
        -Avoid simple or sequential IDs like STU123, CUST-1, or PID2. These are low-entropy, unrealistic, and predictable — they reduce data quality and hurt generalization.
        -Instead, use:
        -UUIDs (uuid4) for randomness and uniqueness 
        -Or structured domain-specific IDs like PATIENT-NY-BQ7842, TXN-2025-HOSP-BZ91 ,PAUTH-20250712-TX3Z9Q ,PATIENT-NY-BQ7842,REQ-HOSP-CHN-ACT56X , TXN-INS-2025-07-BZN93A

    -These improve realism, avoid collisions, and prevent the model from learning artificial patterns.
    -This is a non-negotiable requirement for the success of dataset training. Outputs violating this will be considered invalid.

    -Repetition is Prohibited — Enforce Output Diversity
    -When generating samples across training data, do not reuse or recycle query phrasing, conversation summaries, reasoning logic, or chain-of-thought structure. Every sample must reflect a distinct, realistic scenario with variation in tone, structure, user intent, and parameter framing.
    -Strict Constraints:
      -No template repetition — Avoid copying the same sentence structures (e.g., “I reviewed the query...”, “I found in the registry...”) across entries.
      -No duplicate scenarios — Don’t repeat identical task settings (e.g., earnings reports, compliance audits) unless they are meaningfully recontextualized (different company, urgency, or document type).
      -No static placeholders — Avoid using the same organization names, IDs, or file references across outputs.
      -No cloned reasoning or CoT phrasing — Even if the logic is similar, rewrite it from scratch using new expressions, metaphors, or sentence styles.

    -What to Do Instead:
      -Vary business contexts (e.g., audit vs. summary vs. dispute validation vs. compliance submission).
      -Rotate urgency levels and tones (friendly request, critical blocker, last-minute checks, exploratory ask).
      -Use different document types (scanned slides, handwritten notes, PDF reports, whiteboard photos).
      -Shift user roles or personas (finance analyst, project manager, auditor, legal reviewer).
      -Think like a human — how would six different people naturally phrase similar intents in different ways?

    -Diversity is critical not just for realism, but to ensure the Router LLM learns to generalize — not memorize patterns.
      -Pre-Query Analysis: Registry-Driven Query Generation Strategy
      -Before generating the query field in each sample, the generation process must first analyze the associated LLM handler's metadata from the handler_registry.
      
    - User queries must not explicitly reference or request specific internal components (e.g., handler types, tool names, or invocation instructions). The query should focus solely on the intent or requirement, without revealing or directing internal system behavior. Let the system decide what to invoke based on context.
      
## Key Decision Rule

### behaviour of the missing_fields

    If all required fields are found across query and conversation_summary:
        "missing_fields": []

    If any required fields are missing in both:
        "missing_fields": ["testing_platform_url", "traffic_allocation", "variants"]

###  `suggested_payload` Generation Guidelines for LLM

The system must decide what to include in `missing_fields` and `suggested_payload` **based on how many required parameters are missing**. Follow these **three explicit cases**:

---

#### Case A — **All Required Fields Missing**

* 🔹 **When to Trigger:**
  None of the required fields can be extracted from the query or memory. You don't have any parameter values at all.

    * 🔹 **What to Output:**
    ```json
    "missing_fields": ["field1", "field2", "field3"],
    "suggested_payload": {}
    ```
    * 🔹 **Key Rule:**
    `suggested_payload` must be completely empty because nothing is known. All required fields must be listed in `missing_fields`.

    ---

#### Case B — **Some Required Fields Missing**
    * 🔹 **When to Trigger:**
    You can extract **at least one required field** from the query or memory, but **some fields are still missing**.

    * 🔹 **What to Output:**

    ```json
    "missing_fields": ["fieldX"],
    "suggested_payload": {
        "fieldA": "value_from_query_or_memory",
        "fieldX": "missing",
        "summary": "A natural sentence clearly describing what the user wants."
    }
    ```

* **Key Rules:**

    1. **Include a `summary`** in `suggested_payload` as a natural English sentence describing the user’s request.

        * Example: `"summary": "User is requesting to check the project details."`
    2. **Mark missing fields explicitly** with `"missing"` as their value.

        * Example: `"issue_type_id": "missing"`
    3. **Do not fabricate values.** Only use what you can extract or infer confidently.

---

#### Case C — **No Required Fields Missing**
    * **When to Trigger:**
    You can extract or infer **all required fields** from the query and/or memory. Nothing is missing.

    * **What to Output:**
        ```json
        "missing_fields": [],
        "suggested_payload": {
            "field1": "value1",
            "field2": "value2"
        }
        ```

    * **Key Rule:**
    No `missing` markers or `summary` are needed in this case. Just list the complete and correct values for all required fields.

---

### Final Notes for the LLM
    * Think step-by-step: first determine which fields are available, then construct `missing_fields` and `suggested_payload` accordingly.
    * Do **not** invent missing values. Use `"missing"` as a placeholder.
    * Always follow the matching behavior for the correct case (A, B, or C).
    * Only include `summary` in Case B, never in A or C.

---

---

### Behavior of the `summary` Key in `suggested_payload`

The `summary` field inside the `suggested_payload` is **only included under a specific scenario** — when **some (but not all)** required fields are missing.

---

#### When is `summary` used?
The `summary` key is **only present when:**
    * `missing_fields` is **non-empty** (i.e., at least one required field is missing),
    **AND**
    * Some required fields are already populated in the `suggested_payload`.

---

#### Important Rule
> The `summary` field **must not** be included in the following scenarios:
    > * All required fields are missing (`suggested_payload` is empty).
    > * All required fields are present (`missing_fields` is empty).

---

####Purpose of `summary`

In this special case (partially missing fields), the `summary` provides a **brief natural-language explanation** of what the user is trying to accomplish based on the available input. This helps downstream agents or UIs show a meaningful preview of the intended action.

---

#### Example:

```json
{
  "missing_fields": ["issue_type_id"],
  "suggested_payload": {
    "project_id": "dm",
    "issue_type_id": "missing",
    "summary": "User is requesting to check the project details."
  }
}
```

---
           
### optional_parameters Behavior
    - All properties listed in input.input_schema.properties that are not listed in input.input_schema.required are considered optional.
    - Given the input schema:
        "input_schema": {  "type": "object",  "properties": {    "student_id": { "type": "string" },    "course_id": { "type": "string" },    "enrollment_date": { "type": "string" },    "override_prerequisites": { "type": "boolean" },    "access_token": { "type": "string" }  },
        "required": ["student_id", "course_id", "access_token"]
        }
    - The optional parameters are:
    - "optional_parameters": ["enrollment_date", "override_prerequisites"]

### How to Implement query and conversation_summary with Varying Parameter Placements

To ensure diverse yet realistic data coverage, you must intentionally control where the required parameters appear across query and conversation_summary. You are generating 4 data points total, each belonging to one of two categories.
    I. Complete Parameter Coverage (2 Data Points)
    -Generate two (2) data points where all required fields are present. Use any two of the following inclusion types:
        - All required fields are included in both conversation_summary and query.
        - All required fields are included only in query.
        - All required fields are included only in conversation_summary.

    II. Missing Parameter Scenarios (2 Data Points)
    - Generate two (2) data points where one or more required fields are missing. Choose any two from the following missing field cases:
        - Required fields are missing in both conversation_summary and query.
        - Required fields are missing only in query.
        - Required fields are missing only in conversation_summary.

   -Mandatory Rule – Enforced Parameter Placement Awareness
    - At all times, you must consciously track where the required fields appear. This behavioral pattern is not optional — it is central to your dataset's diversity.
    - With  Missing Parameter Scenarios  --> You must include context not related to the required parameters when developing query and conversation summary

   
    Example 1: All Required Fields Present
        - Required Fields from Tool:    ["patient_id", "appointment_type", "appointment_datetime"]
        - missing_fields : []
        - query : "Can you confirm the routine check-up scheduled for patient PAT-9482-LA on July 18th at 10:00 AM?"
        - Conversation Summary:" The patient ID is PAT-9482-LA.  The appointment type is a routine check-up.  The appointment is scheduled for July 18th at 10:00 AM."
        - Suggested Payload:   {    "patient_id": "PAT-9482-LA",    "appointment_type": "routine check-up",    "appointment_datetime": "2025-07-18T10:00:00",}

    Example 2: Some Required Fields Missing
        - Required Fields from Tool:["patient_id", "appointment_type", "appointment_datetime"]
        - missing_fields:["appointment_datetime"]
        - query : "I’d like to schedule a routine check-up for patient PAT-9482-LA"
        - Conversation Summary:"The patient ID is PAT-9482-L The appointment type is a routine check-up."
        - Suggested Payload:{  "appointment_datetime": "missing",  "patient_id" : "PAT-9482-L ","appointment_type" :"routine check-up" "summary": "Schedule a routine check-up for the patient."}

        
    Example 3: All Required Fields Missing
        - Required Fields from Tool:["patient_id", "appointment_type", "appointment_datetime"]
        - missing_fields:["patient_id", "appointment_type", "appointment_datetime"]
        - query : "Can you help me set up a new appointment for one of our patients?"
        - Conversation Summary:" The user has previously asked for help managing patient appointments.They’re likely trying to schedule something but haven’t provided any specifics yet.""
        - Suggested Payload:{  "appointment_datetime": "missing",  "patient_id" : "PAT-9482-L ",  "summary": "Schedule a routine check-up for the patient."}


## Schema Generation Instructions
-You have to follow guidance during the following field creating process
1. query → Human-Readable User Request
    -Role: End-User Simulation
    -The query field must simulate how a real user would naturally ask the system to perform a task — using clear, human-like language that reflects their intent, not internal system mechanics.
    -Purpose: -The query helps the Router LLM decide, Which agent is appropriate for the request.

    -Query Generation Process
    -Step 1: Understand the Handler’s Real-World Function
    -Carefully review the description in the handler registry.
    -Ask: What would a user want to accomplish by invoking this  LLM?
    -Example:
        "description": "Analyzes employee skill assessment data to identify proficiency levels and areas for development."
    -Real-world Use Case:
        -An HR user or manager wants to see how well an employee performed in a recent skill assessment.
    -Inferred Contextual Inputs:
        -Employee name  (e.g., "Saman") and some reference to the specific assessment or time (e.g., “latest”, “Q1 2024 assessment”). Use specific context to enrich the query with evidance

    -Step 3: Write a Human-Centered, Realistic Query
    -Combine the task (from the description) and the parameters (from the input schema) into a natural user sentence.
    - Make it intent-driven, not system-driven.

    - Vary the phrasing style:
    - Direct: Ask clearly and factually
    - Indirect: Ask via references or secondary goals
    - Uncertain: Reflect user confusion or partial understanding
    - Batch or comparative: Include the same intent in a broader/multi-part query

    -Good Examples:
    “I need to review Jane Kim's performance on the March training evaluation.”
    “How did the product team do in their recent collaboration skills assessment?”

    -What to Avoid how to avoide
    "Enter employee_id to continue"  --> "Can you show me results for employee NM-XI4329?"
    "test", "example", "xxx"  --> Use realistic names, IDs, dates, or contexts
    "employee_id" in raw text  --> Say “employee”, “team member”, or use a name/number

    - Summary Guidelines
    
    - Act like a real user trying to solve a specific task.
    -user s not part of the system and should not be made aware of its internal behavior. Do not instruct the user to explicitly invoke a specific agent, as they are unaware of the available agents. The user only needs to provide the task.
        - User queries must not explicitly reference or request specific internal components (e.g., handler types, or invocation instructions). The query should focus solely on the intent or requirement, without revealing or directing internal system behavior. Let the system decide what to invoke based on context.
    - Use the worker agent handler description to guide what the query is trying to achieve.
    - Use the input_schema to inform your phrasing — never expose raw schema terms in the query.
    - Make sure the query sounds contextual, not like a prompt for a tool or test system.
    “While generating each data point, I must actively decide which required parameters appear in the query, which appear in the conversation_summary, and which are left missing — based on the combination pattern being implemented.”


 2 conversation_summary 

The `conversation_summary` simulates realistic, memory-aware interactions between a user and the system. It acts as a **contextual bridge** between past and present queries, helping the system reason about continuity, intent, and user goals.
Begin by understanding the handler’s functionality. 

    -Guideline to cretate conversation_summary
        -Ground it in the Handler’s Purpose
            - Read the handler_registry entry carefully .
            - Identify realistic enterprise workflows or interactions that could lead to the current query.
            - Use Domain-Relevant Scenarios . Build summaries around authentic user behavior.

        - Include Parameter Seeds or Identifiers
            - Use specific names, IDs, and terms to simulate grounded memory. These are important for relevance and contextual linking.
                - >*“You previously reviewed the `AuthController.validateToken()` method after encountering a session expiry issue in `release-v2.9.3`.”*

        - Simulate a Chronological Memory Trail
            - Write 2–4 lines showing **conversation flow** over time:
                - Initial request  
                - System response  
                - User clarification  
                - System follow-up  
            - > *“You first investigated the structure of the `report_generator` module. After identifying missing dependencies, you asked for design notes connected to the data ingestion component.”*

        - Reflect Multi-Turn or Ongoing Engagement
            - Simulate continuity — make it feel like part of a **threaded initiative** or **recurring process**.
            - >*“As part of the Q2 compliance review, you’ve been exploring access control logic across the `UserPolicy` layer. In the last session, you confirmed gaps in the audit trail and requested links to the policy validation logic.”*
                
                - Add Rich Context + Prior Contacts
            -You must provide a detailed, imaginative yet context-grounded narrative of the user's earlier actions. Include:
                - Broader initiatives
                - Realistic — infer probable past steps from current query


-You can implement conversation_summary in two ways:
    -As a list of multiple summary strings, like this:
        conversation_summary = "Last week, user explored architectural dependencies around the `BillingService` class after reporting inconsistent charge logic during nightly ETL jobs."
    -Sometimes this summary may be empty. if you chose this way make sur to add all the necessary content with in query.
        conversation_summary = ""

-Example for Converstion memory
    > *user previously explored how the `DataSyncManager` interacts with `SyncWorker` during job execution. After retrieving class definitions and init methods, user asked for related design notes tied to the `stream_batch()` pipeline. The system retrieved class hierarchy mappings and pointed out recent architectural changes merged from `dev/feature-sync`.”*
    > *“Last week, user explored architectural dependencies around the `BillingService` class after reporting inconsistent charge logic during nightly ETL jobs.”*

While generating each data point, I must actively decide which required parameters appear in the query, which appear in the conversation_summary, and which are left missing — based on the combination pattern being implemented.”


3. reasoning 
- agent  Suggestions
- You are evaluating whether the current user query and conversation memory provide enough information to **select and invoke a specific MPC tool** from the registry.
- Follow these steps strictly:
        Step 1: Check Required Parameters
            - Refer to the `input_schema` of the MPC tool.
            - Identify the list of **required fields** (e.g., `["patient_id", "appointment_type", "appointment_datetime"]`).
        Step 2: Assess Parameter Coverage
            - Examine whether **all required parameters** are present, either in the `query`, the `conversation_summary`, or a combination of both.
            - If **all required fields are present**, respond with a sentence like “This request can be delegated to the MPC tool as all invocation requirements are satisfied.”
        Step 3: Identify Missing Parameters (If Any)
            - If **one or more required fields are missing** across both `query` and `conversation_summary`, the tool **cannot be invoked**.
            - Respond clearly, stating that the tool is **not selected**, and list the missing fields.Optional alternate phrasing:
- Summary Rule
    > Always decide **tool selection status** based solely on the presence of **all required parameters**.
    > A single missing parameter invalidates invocation.

    -Agent Selected – Example 1 :
      - All  invocation requirements  are present in the query or memory. The agent is successfully selected and invoked to generate the requested summary.
    -Agent Not Selected – Example 2 :
        - Due to insufficient context, the system does not select or invoke any agent, and may instead ask a follow-up question to gather missing information.
        
7. chain_of_thought → Step-by-Step Reasoning 

    You are deciding whether a given worker agent can be selected and invoked based on the available input.

    Follow this reasoning process step by step:

    Step 1:Intent Recognition:
    -Analyze the user's request to understand what they’re trying to do.Examine both the query and the conversation_summary.

    Step 2: Worker agent Identification:
    Search the handler registry to identify the most relevant tool. If the intent matches an Worker agent , select that agent.

    Step 3:Parameter Check:
    -Review the worker agents's payload_schema.required list.Identify Required Parameters. Extract all fields marked as required (e.g., ["patient_id", "appointment_type", "appointment_datetime"]).

    Step 4: Match and Coverage Evaluation
        -If all required fields are present (either in query, conversation, or combined), then:
            -Conclude that the tool can be selected.
            -State that the invocation requirements are fully satisfied.
            -Justify by listing where each parameter was found (query, summary, or both).

        -If any required field is missing across both the query and memory, then:
            -Conclude that the tool cannot be selected.
            -Explain that the request is insufficient for invocation.
            -Clearly list all missing fields.

    Step 5: **Confirm Selection & Confidence:**
        - Conclude with the selected handler, the matched copilot ID, and restate the confidence score **as-is**.
        - Your final sentence must include this score exactly (e.g., "The system's confidence score of 0.73 confirms this selection.").
        - confidance level defined in the output.confidence must be taken as the confidence. do not use random guesses.

    -Style & Tone Guidelines
        - Always use first-person voice (“I assessed...”, “I determined...”) to simulate internal reasoning.
        -Keep explanations formal and evidence-backed.
        -Avoid repetition — even across different samples.

    -Reasoning Styles to Rotate Across Entries
        -To avoid repetition across dataset rows, vary your **reasoning styles**:
            - **Deductive:** From input → conclude best match.
            - **Inductive:** From clues → infer the most likely handler.
            - **Comparative:** Weigh between multiple handlers before concluding.
            - **Context-first:** Start from prior memory, then match forward.

    Diversification Tips for chain_of_thought`
    **1. Rotate how you enter the task:**
    - "The user's request clearly mentions..."
    - "Upon reading the query, it's evident that..."
    - "Based on the user's input, I inferred..."

    **2. Switch the matching mechanism:**
    - "I compared the query against each handler’s description."
    - "I isolated key action verbs and aligned them with copilet  roles."
    - "I noted thematic overlap in the wording of the query and handler purpose."

    **3. Vary what field you emphasize:**
    - Query-focused → "The phrasing in the user request strongly aligns with..."
    - Memory-focused → "Drawing from the previous conversation, I matched continuity with..."
    - Registry-focused → "Among the available RAG handlers, the one that most directly..."

    **4. Alternate logic flow types:**
    - Deductive → "Given ---- and ---, the only logical handler is -----."
    - Elimination → "Other handlers were dismissed due to lack of overlap, leaving only ----."
    - Inductive → "The combination of terms hints at a use case that best fits --- copolot"

    **5. Confidence expression tweaks:**
    - "The system's confidence score  reinforces the validity of this match."
    - "The match is backed by a computed confidence score give in the input."

    Example 1 (missing required requiremtns):
        [
            "Upon reading the query, I determined that the user is seeking a status update on an incident ticket related to performance issues in the billing application.",
            "I reviewed the handler registry and identified the `check_incident_status` Worker Agent as the most suitable match, given its role in retrieving incident ticket details from the ITSM system.",
            "The agent's payload schema requires three mandatory fields: `incident_id`, `environment_id`, and `itsm_api_token`.",
            "The conversation summary explicitly provides the `environment_id` as 'PROD-19' and confirms the availability of the `itsm_api_token`.",
            "However, the query does not mention a specific `incident_id`, and no such identifier is found in the conversation summary.",
            "I noted that the optional parameter `priority_level` could enhance the request but is not mandatory.",
            "Since the `incident_id` is absent, the Worker Agent cannot be invoked, as all required parameters must be present.",
            "The system's confidence score of 0.72 reinforces the validity of this match, despite the incomplete inputs."
        ]
        

    Example 2 (no any missing requiremtns):
        [
        "Drawing from the conversation summary, I noted that the user is preparing for a firewall configuration update and has already submitted change request CR-3921 for the QA-07 environment.",
        "The query further specifies validating this change request using the compliance ruleset SEC-2025-Q2, indicating a clear intent to automate validation in the ITSM system.",
        "I searched the handler registry and confirmed that the `validate_change_request` Worker Agent is the best match, as it automates change request validation processes.",
        "The agent's payload schema requires four fields: `change_request_id`, `environment_id`, `compliance_ruleset`, and `itsm_api_token`.",
        "The query provides `change_request_id` (CR-3921), `environment_id` (QA-07), and `compliance_ruleset` (SEC-2025-Q2), while the conversation summary confirms the availability of the `itsm_api_token`.",
        "I also observed that the optional parameter `validation_report_format` could be suggested to customize the output, though it’s not required.",
        "With all required fields fully provided across the query and summary, the Worker Agent is ready for invocation.",
        "The system's confidence score of 0.98 confirms the strong alignment and completeness of the inputs."
        ]


### How to Build Query and Conversation Memory

    1. **First, identify** the required and optional parameters defined in the handler.

    2. **Then, generate the query and conversation memory** for the following scenarios:

    ---

    #### Scenario 1: All required parameters are present

    * You can include all the required parameters in the **query**, **conversation summary**, or split them across **both**.
    * To make the query and conversation summary richer, you may also include context related to **optional parameters**.

    ---

    #### Scenario 2: Some required parameters are missing

    * Decide which required parameter(s) should be missing from the **query** and **conversation summary**.
    * Then generate the query and conversation summary **excluding any context related to the missing parameters**.
    * Again, you can enrich the query and summary with context related to **optional parameters**, as long as it doesn’t conflict with the missing required fields.


### Diverse User Queries + Conversation Memory
    All queries are meant to trigger Worker Agents in an ITSM context.

    - Variant 1 – Friendly Follow-up on Server Outage
    - Query: "Hey, can you take a deeper look at the  model outage from this morning? I thought the restart fixed it, but we’re still seeing connection timeouts in the billing app. Might need to escalate."
    -Conversation Memory: "User asked the incident agent to check PROD-23 due to a service interruption.The System reported a successful restart and system stabilization.user acknowledged it worked earlier but wanted to monitor further for any anomalies.The billing team just reported fresh timeouts post-restart. "

    - Variant 2 – Deployment Window Validation
    - Query:"Please confirm that CR-2458 has received final approval from InfoSec and compliance before our 6 PM deployment window today. We can’t proceed without the green light."
    - Conversation Memory: "You submitted a Change Request CR-2458 last Monday for a scheduled firewall update.The request was pending InfoSec review and compliance sign-off.The deployment window is today at 6 PM sharp.You are waiting on approval before proceeding.

    - Variant 3 – Slightly Vague Monitoring Request
    - Query: "Something's definitely off with the main DB in prod — we’re getting random lags during report generation. Could your monitoring assistant check if anything unusual popped up in the last 4 hours?"
    - Conversation Memory: " user previously flagged high latency during batch report processing.No clear root cause was found during the last agent scan.Report generation is business-critical for daily reconciliation.user is now ticing sporadic lag again, especially this morning. "

    - Variant 4 – Batch Uptime & SLA Report
    - Query: "I need a weekly uptime and incident summary for DEV-02, QA-11, and PROD-44 — mainly focusing on any SLA breaches or escalations. We’re prepping for the ops review tomorrow."
    -Conversation Memory: "You’ve been collecting operational metrics for the quarterly ITSM review.You already pulled ticket resolution times for QA-11.The ops team asked for uptime trends and SLA breaches across environments.This data is due by tomorrow's 9 AM review call. "

    - Variant 5 – Clarification on Deployment Outcome
    - Query: "Just to clarify — did the firewall config change from yesterday get deployed, and did it pass validation? Security was worried about the outbound rule exceptions."
    - Conversation Memory: "You pushed a firewall config update yesterday at 7 PM.A change request was created, but validation results weren’t shared yet.InfoSec raised concerns about new outbound rules before the change.You now want to ensure the deployment was completed and validated. "

    Variant 6 – Unexplained Network Activity
    -Query: "We got a bunch of failed pings to QA-03 overnight, but there’s no incident ticket. Could your system monitoring agent figure out if it was a temporary spike or something serious?"
    -Conversation Memory: "You previously had intermittent issues on QA-03, which were unresolved.Overnight logs show multiple ICMP ping failures, but no alert was triggered.There’s concern this might be a silent failure or a monitoring gap.You’re relying on the monitoring agent to diagnose without formal ticket escalation. "


---
## Fields That Must Remain Unchanged

These fields are critical to the system's integrity. Do not modify their keys, default values, or internal structure.
The following fields must be preserved exactly as they are. No changes, overwrites, or reassignments should be made to their structure, names, or values during processing or reasoning:

| Field Location | Field Name                      | Rule                                 |
| -------------- | ------------------------------- | ------------------------------------ |
| `input`        | `id`                            | **Must not be modified**             |
| `input`        | `timestamp`                     | **Must not be modified**             |
| `input`        | `handler_registry`              | **Must remain exactly as provided**  |
| `input`        | `copilot_id`                    | **Do not alter or override**         |
| `input`        | `thread_id`                     | **Leave untouched**                  |
| `output`       | `select_handler_type`           | **Keep original value**              |
| `output`       | `handler_name`                  | **Must not change**                  |
| `output`       | `server_name`                   | **Preserve null or given value**     |
| `output`       | `tool_name`                     | **Preserve null or given value**     |
| `output`       | `copilot_id`                    | **Preserve null**         |
| `output`       | `confidence`                    | **Should exactly match given value** |
| `output`       | `workspace_preference_override` | **Must stay untouched**              |



## Strict Rule
    - IMPORTANT: Outside of the fields listed above, no other parts of the original input or output JSON should be altered. 
    - This ensures structural consistency and compatibility with downstream pipelines. The format, nesting, and extra fields must remain exactly as in the original INPUT_JSON.
    - In Stage 1, generate an array of 4 distinct JSON items—each containing a unique combination of the required output fields. 
    - Then, in Stage 2, iterate over these 4 items to replace the corresponding fields in the input JSON schema, producing a final output array of 4 fully merged JSON objects reflecting the updated input and output sections. 
    - Return final stage 2 output as following list of array
        - [stage2_item1, stage2_iitem2, stage2_iitem3, stage2_iitem4].

- This marks the end of the prompt, and the final response should return this array of 4 complete JSON items."


"""
