MCP_TOOL_PROMPT = """

This process is designed to generate a training dataset for responsible for routing user queries to the appropriate MCP (MODEL CONTEXT PROTOCAL) tool in an enterprise system.
You are simulating a Router LLM that receives user input and determines the most suitableBase MCP tool to invoke based on a registry of handlers. This dataset captures realistic  decision patterns for use in downstream LLM-based orchestration systems.
Key Concepts : 
1. MCP Handlers
  -Each MCP handler entry in the handler_registry represents a MCP TOOl with specific capabilities and metadata. Fields typically include:
   - Fields typically include:
     - `name`: Unique name of the tool.
     - `server_name`: The system that exposes this tool.
     - `description`: Explanation of what the tool does, including parameter usage.
     - `input_schema`: A JSON schema object describing expected fields:
       - `required`: A list of field names that must be provided fro the tool invocation.
       - `properties`: A dictionary where each key represents an input field and its metadata (e.g., type, title).   
       -handler_registry: {"mcp_tools": [{"name": "get_customer_by_id", "server_name": "SalesforceMCP", "description": "Retrieves detailed information for a specific customer record from the CRM.\n\n:param customer_id: The unique identifier for the customer.\n:return: A dictionary containing customer details such as name, email, phone, and address. (Server: SalesforceMCP)", "input_schema": {"type": "object", "properties": {"customer_id": {"title": "Customer ID", "type": "string"}, "api_key": {"title": "API Key", "type": "string"}, "instance_url": {"title": "Instance URL", "type": "string"}}, "required": ["customer_id", "api_key", "instance_url"]}}

For each  sample, we simulate how a Router LLM would behave by starting from the available MCP handler(s) in the handler_registry and generating a realistic user interaction that would lead to selecting that handler.
The steps are:
    -Start from a given MCP handler  in the handler_registry.
    Extract its:
        -name
        -server_name
        -description
        -input_schema
        - `required`: 
        - `properties`:
    -Based on the handler’s description and capabilities, generate:
    -A natural-sounding user query that would require this handler.
    -A conversation_summary simulating context from previous turns.
    -tool_name should convey a meaning similar to output.handler_name but must not be identical. the two names should be distinct yet semantically aligned.
    - handle missing_fields, suggested_payload, optional_suggetion according to the way the conversation_summary and user query is implemented
    -Create structured fields that simulate how a Router LLM would explain its selection:
    -reasoning: Why was this handler picked?
    -chain_of_thought: Step-by-step reasoning chain that shows matching between query and handler.
    -Insert generated fields back into the original input/output JSON structure, to complete the training example.


## TASK OVERVIEW:
- This task involves a two-stage process for each INPUT_JSON provided:
    -STAGE 1 — Generate Content: Based on the INPUT_JSON, generate 6 unique and dynamic data entries. Each entry will contain a user query, the reasoning for the routing decision, and a detailed chain-of-thought.
    -STAGE 2 — Update and Finalize JSON: For each of the 6 generated entries, create a deep copy of the original INPUT_JSON and inject the generated content into the appropriate fields.

### STAGE 1
    - You will be given  a SAMPLE INPUT JSONL as follows:

    {"input": {"id": "1874d50c-dc1b-4a46-8586-4c2697de4941", "timestamp": "2023-12-31T02:02:22.905632", "query": "", "conversation_summary": "", "handler_registry": {"mcp_tools": [{"name": "get_customer_by_id", "server_name": "SalesforceMCP", "description": "🔗 [REQUIRES SETUP] \nRetrieves detailed information for a specific customer record from the CRM.\n\n:param customer_id: The unique identifier for the customer.\n:return: A dictionary containing customer details such as name, email, phone, and address. (Server: SalesforceMCP)", "input_schema": {"type": "object", "properties": {"customer_id": {"title": "Customer ID", "type": "string"}, "api_key": {"title": "API Key", "type": "string"}, "instance_url": {"title": "Instance URL", "type": "string"}}, "required": ["customer_id", "api_key", "instance_url"]}}], "worker_agents": [], "llm_handlers": [], "rag_handlers": [], "compiled_at": "2023-12-29T10:28:06.905632", "user_id": "68766fb8-1be6-489b-8470-d87351ff1b4c", "workspace_id": "dfe8cc93-c88b-45e4-b581-3b888debfe26"}, "copilot_id": null, "thread_id": "6f129fbc-5852-4943-ac66-d560dd30a712"}, "output": {"select_handler_type": "mcp_tool", "handler_name": "get_customer_by_id", "server_name": "SalesforceMCP", "tool_name": null, "copilot_id": null, "missing_fields": [], "optional_suggestions": [], "suggested_payload": {}, "confidence": 0.94891, "reasoning": "", "chain_of_thought": [], "workspace_preference_override": false}}

#### Generate 6 Data Points
    -Create six (6) data points following the structure below:

    I. Complete Parameter Coverage (3 Data Points)
    -Generate six (6) data points where all required fields are present. Use any two of the following inclusion types:
        - All required fields are included in both conversation_summary and query.
        - All required fields are included only in query.
        - All required fields are included only in conversation_summary.

    II. Missing Parameter Scenarios (3 Data Points)
    - Generate six (6) data points where one or more required fields are missing. Choose any two from the following missing field cases:
        - Required fields are missing in both conversation_summary and query.
        - Required fields are missing only in query.
        - Required fields are missing only in conversation_summary.


-For each INPUT_JSON, generate six diverse output samples simulating how a user might trigger the selected handler. Each sample must include the following fields:
  -Required Fields per Sample:
    -query: A natural-sounding user query that would appropriately invoke the selected handler. This may contain implicit or explicit references to required schema parameters.
    -conversation_summary: A realistic summary of prior conversation context, helping justify parameter grounding or task continuity.
    -tool_name :tool_name should convey a meaning similar to output.handler_name but must not be identical. the two names should be distinct yet semantically aligned.
    - handle missing_fields, suggested_payload, optional_suggetion according to the way the conversation_summary and user query is implemented {based on how required parameters are applied on query and conversation memory}
    -reasoning: A concise justification explaining why the selected handler is the most appropriate match for the query.
    -chain_of_thought (CoT): A step-by-step explanation of how the Router llm  analyzed the query, considered handler capabilities, and validated parameter readiness to select the given mcp tool.
  -Each of the 4 samples should simulate a distinct and realistic user scenario, varying in phrasing, specificity  to ensure dataset diversity.


Output Schema STAGE 1(Per Generated Entry):

{
  "query": "<string>",                     // Natural-language user request
  "conversation_summary": "<string>",     // Prior context simulating memory
  "tool_name": "<string>", // Action-oriented name of the selected MCP tool
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

### **Example 01 – Few Required Parameters Are Missing**

```json
{
  "query": "We have a deadline approaching. Can you please prioritize validating the payroll batch? It's urgent.",
  "conversation_summary": "The user is using the 'FY25-Audit-Compliance' validation ruleset for this check. Secure credentials for the main HR database have been loaded for this task. This validation is part of the pre-audit checks for the fiscal year-end. The user has been authenticated via their SSO token, REQ-SSO-FIN-8A3B4C. A notification should be sent to the audit team upon completion.",
  "tool_name": "execute_urgent_payroll_validation",
  "missing_fields": [
    "payroll_data_batch",
    "payroll_system_access"
  ],
  "optional_suggestions": [],
  "suggested_payload": {
    "payroll_data_batch": "missing",
    "payroll_system_access": "missing",
    "validation_ruleset": "FY25-Audit-Compliance",
    "hr_database_credentials": "REQ-SSO-FIN-8A3B4C",
    "summary": "Execute an urgent payroll validation using the 'FY25-Audit-Compliance' ruleset."
  },
    "reasoning": "The request aligns with the intended purpose of the `execute_urgent_payroll_validation` tool, but it cannot be invoked due to missing secure inputs. This tool mandates complete parameter coverage to comply with strict audit validation protocols."
    "chain_of_thought": [
    "The user has submitted an urgent request to validate a payroll batch ahead of a deadline.",
    "After reviewing the handler registry, I determined that the `payroll_data_validation` tool is the most suitable for this task.",
    "This tool requires the following parameters: `payroll_data_batch`, `validation_ruleset`, `payroll_system_access`, and `hr_database_credentials`.",
    "Based on the conversation summary, I can confirm that the `validation_ruleset` is 'FY25-Audit-Compliance' and that `hr_database_credentials` have already been provided.",
    "However, the specific `payroll_data_batch` and credentials for `payroll_system_access` are missing.",
    "There are no optional parameters available to supplement or bypass these requirements.",
    "Since two critical inputs are absent, I cannot proceed with invoking the tool at this time.",
    "I would rate my confidence at 0.72—while the user's intent is clear, the necessary input coverage is incomplete."
    ]
    }
```

---

###  **Example 02 – All Required Parameters Are Included**

```json
{
  "query": "Let's run the autograder on the 'Advanced Algorithms' homework, ID CS-ALGO-HW4. Submissions are in hw4_submissions.zip and the rubric is algo_hw4_rubric.yaml. Use the department API key. Also, use the 'detailed feedback' template for the comments.",
  "conversation_summary": "The user is grading an assignment for the 'Advanced Algorithms' course. The assignment ID is CS-ALGO-HW4. The department LMS API key is `lms-api-cs-dept-9a8b7c6d`. The user mentioned using a specific feedback template named 'detailed feedback'.",
  "tool_name": "execute_autograder",
  "missing_fields": [],
  "optional_suggestions": [
    "feedback_template"
  ],
  "suggested_payload": {
    "assignment_id": "CS-ALGO-HW4",
    "submission_data": "hw4_submissions.zip",
    "grading_rubric": "algo_hw4_rubric.yaml",
    "lms_api_key": "lms-api-cs-dept-9a8b7c6d"
  },
  "reasoning": "This request is a strong match for the `execute_autograder` tool. All required parameters are accounted for, making the tool ready for execution without any issues.",
  "chain_of_thought": [
    "The user wants to run an autograder on a specific homework assignment.",
    "I've identified the `grade_assignment_automatically` tool as the correct handler.",
    "The tool requires `assignment_id`, `submission_data`, `grading_rubric`, and `lms_api_key`.",
    "The query and summary provide all required fields: `assignment_id` (CS-ALGO-HW4), `submission_data` (hw4_submissions.zip), `grading_rubric` (algo_hw4_rubric.yaml), and `lms_api_key` (lms-api-cs-dept-9a8b7c6d).",
    "The user also requested a specific optional feature: the 'detailed feedback' template.",
    "The optional `feedback_template` parameter was also identified from the query.",
    "With all required fields and an optional field provided, the tool is fully ready for invocation.",
    "The alignment is excellent, and all information is present, leading to a high confidence score of 0.98."
  ]
}
```
### STAGE 2 
- Apply generated fields to INPUT_JSON:
- For each generated output entry in stage 1:
    - 1. Create a deep copy of the original INPUT_JSON.
    - 2. Replace or update the corresponding fields in the deep copy with the stage 1  values as follows:
           - input.query → from generated query
           - input.conversation_summary → from generated conversation_summary
           - output.tool_name → from generated tool_name
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
    "tool_name": "<replaced with Stage 2 → tool_name>",
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
        "id": "12a2f3df-f2ca-405a-be07-90b6eec30521",
        "timestamp": "2025-04-18T23:59:31.538006",
        "query": "We have a deadline approaching. Can you please prioritize validating the payroll batch? It's urgent.",
        "conversation_summary": "The user is using the 'FY25-Audit-Compliance' validation ruleset for this check. Secure credentials for the main HR database have been loaded for this task. This validation is part of the pre-audit checks for the fiscal year-end. The user has been authenticated via their SSO token, REQ-SSO-FIN-8A3B4C. A notification should be sent to the audit team upon completion.",
        "handler_registry": {
            "mcp_tools": [
                {
                    "name": "payroll_data_validation",
                    "server_name": "HumanResourcesMCP",
                    "description": "🔗 [REQUIRES SETUP] \nValidates payroll data for accuracy, including employee hours, deductions, and tax information.\n\n:param payroll_data_batch: A batch of payroll data.\n:param validation_ruleset: The set of rules for payroll validation.\n:param payroll_system_access: Credentials for accessing the payroll system.\n:return: A report of validated payroll data and any identified discrepancies. (Server: HumanResourcesMCP)",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "payroll_data_batch": {
                                "title": "Payroll Data Batch",
                                "type": "string"                                
                                }
                            },
                            "validation_ruleset": {
                                "title": "Validation Ruleset",
                                "type": "string"
                            },
                            "payroll_system_access": {
                                "title": "Payroll System Access",
                                "type": "string"
                            },
                            "hr_database_credentials": {
                                "title": "HR Database Credentials",
                                "type": "string"
                            }
                        },
                        "required": [
                            "payroll_data_batch",
                            "validation_ruleset",
                            "payroll_system_access",
                            "hr_database_credentials"
                        ]
                    }
                }
            ],
            "worker_agents": [],
            "llm_handlers": [],
            "rag_handlers": [],
            "compiled_at": "2025-04-17T09:37:50.538006",
            "user_id": "748f5bf9-b3db-4f68-87bd-072622b69e06",
            "workspace_id": "de17df0e-5894-4d02-9882-a35c64a9bfa0"
        },
        "copilot_id": null,
        "thread_id": "1bc1d24b-2f50-4e58-bc46-a2d0574821a3"
    },
    "output": {
        "select_handler_type": "mcp_tool",
        "handler_name": "payroll_data_validation",
        "server_name": "HumanResourcesMCP",
        "tool_name": "execute_urgent_payroll_validation",
        "copilot_id": null,
        "missing_fields": [
            "payroll_data_batch",
            "payroll_system_access"
        ],
        "optional_suggestions": [],
        "suggested_payload": { // 
            "payroll_data_batch": "missing",
            "payroll_system_access": "missing",
            "validation_ruleset":"FY25-Audit-Compliance",
            "hr_database_credentials" :" REQ-SSO-FIN-8A3B4C",
            "summary": "Execute an urgent payroll validation using the 'FY25-Audit-Compliance' ruleset." // Some Required Fields Missing so there is a summary key
        },
        "confidence": 0.720124,
        "reasoning": "The user's urgent request to validate payroll aligns well with the purpose of the `payroll_data_validation` tool. While the `validation_ruleset` and `hr_database_credentials` are already available, the tool cannot be executed without the `payroll_data_batch` and the `payroll_system_access` credentials, both of which are currently missing.",
        "chain_of_thought": [
        "The user submitted an urgent request to validate a payroll batch ahead of a looming deadline.",
        "I reviewed the handler registry and determined that the `payroll_data_validation` tool is the most appropriate match for this task.",
        "According to its schema, the tool requires four fields: `payroll_data_batch`, `validation_ruleset`, `payroll_system_access`, and `hr_database_credentials`.",
        "The conversation summary confirms that the `validation_ruleset` is set to 'FY25-Audit-Compliance' and the `hr_database_credentials` have already been provided.",
        "However, the `payroll_data_batch` and the credentials for `payroll_system_access` are still missing.",
        "This tool does not support any optional fields that could compensate for the missing inputs.",
        "Because these two required parameters are absent, the tool cannot be invoked at this time.",
        "I am confident in the intent behind the request, but due to the incomplete input set, I would assign a confidence score of 0.72."
        ]

        "workspace_preference_override": false
    }
}
- Example 02 - All the required parameters are included 


{
    "input": {
        "id": "f1f2580e-c9f9-4e53-ac24-e12283967b8a",
        "timestamp": "2025-06-17T02:02:18.753302",
        "query": "Let's run the autograder on the 'Advanced Algorithms' homework, ID CS-ALGO-HW4. Submissions are in hw4_submissions.zip and the rubric is algo_hw4_rubric.yaml. Use the department API key. Also, use the 'detailed feedback' template for the comments.",
        "conversation_summary": "The user is grading an assignment for the 'Advanced Algorithms' course. The assignment ID is CS-ALGO-HW4. The department LMS API key is `lms-api-cs-dept-9a8b7c6d`. The user mentioned using a specific feedback template named 'detailed feedback'.",
        "handler_registry": {
            "mcp_tools": [
                {
                    "name": "grade_assignment_automatically",
                    "server_name": "AutomatedGradingMCP",
                    "description": "🔗 [REQUIRES SETUP] \nAutomates the grading of student assignments submitted through a learning management system (LMS).\n\n:param assignment_id: Identifier for the assignment.\n:param submission_data: A JSON string or dictionary containing student submissions.\n:param grading_rubric: The rubric used for grading, provided as a JSON string or dictionary.\n:param feedback_template: A template for providing automated feedback.\n:return: Graded submissions with scores and feedback, or an error message. (Server: AutomatedGradingMCP)",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "assignment_id": {
                                "title": "Assignment ID",
                                "type": "string"
                            },
                            "submission_data": {
                                "title": "Submission Data",
                                "type": "string"
                            },
                            "grading_rubric": {
                                "title": "Grading Rubric",
                                "type": "string"
                            },
                            "feedback_template": {
                                "title": "Feedback Template",
                                "type": "string"
                            },
                            "lms_api_key": {
                                "title": "LMS API Key",
                                "type": "string"
                            }
                        },
                        "required": [
                            "assignment_id",
                            "submission_data",
                            "grading_rubric",
                            "lms_api_key"
                        ]
                    }
                }
            ],
            "worker_agents": [],
            "llm_handlers": [],
            "rag_handlers": [],
            "compiled_at": "2025-06-16T15:35:07.753302",
            "user_id": "7f380c1b-ce9d-47fa-ba0a-6d5a431f504b",
            "workspace_id": "2f6772e7-e667-4655-83fa-dadb7237f7eb"
        },
        "copilot_id": null,
        "thread_id": "264cd785-7f2d-4d4c-b486-06e4818851ba"
    },
    "output": {
        "select_handler_type": "mcp_tool",
        "handler_name": "grade_assignment_automatically",
        "server_name": "AutomatedGradingMCP",
        "tool_name": "execute_autograder",
        "copilot_id": null,
        "missing_fields": [],
        "optional_suggestions": [
            "feedback_template"
        ],
        "suggested_payload": {
            "assignment_id": "CS-ALGO-HW4",
            "submission_data": "hw4_submissions.zip",
            "grading_rubric": "algo_hw4_rubric.yaml",
            "lms_api_key": "lms-api-cs-dept-9a8b7c6d"
        },
        "confidence": 0.98,
        "reasoning": "The user's request to run an autograder aligns perfectly with the `grade_assignment_automatically` tool. All required parameters (`assignment_id`, `submission_data`, `grading_rubric`, `lms_api_key`) are present in the query and conversation summary. The user also specified using the optional `feedback_template`. The tool is ready to execute.",
        "chain_of_thought": [
            "The user wants to run an autograder on a specific homework assignment.",
            "I've identified the `grade_assignment_automatically` tool as the correct handler.",
            "The tool requires `assignment_id`, `submission_data`, `grading_rubric`, and `lms_api_key`.",
            "The query and summary provide all required fields: `assignment_id` (CS-ALGO-HW4), `submission_data` (hw4_submissions.zip), `grading_rubric` (algo_hw4_rubric.yaml), and `lms_api_key` (lms-api-cs-dept-9a8b7c6d).",
            "The user also requested a specific optional feature: the 'detailed feedback' template.",
            "The optional `feedback_template` parameter was also identified from the query.",
            "With all required fields and an optional field provided, the tool is fully ready for invocation.",
            "The alignment is excellent, and all information is present, leading to a high confidence score of 0.98."
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
    -Purpose: -The query helps the Router LLM decide, Which MCP tool is appropriate for the request.

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
    -user s not part of the system and should not be made aware of its internal behavior. Do not instruct the user to explicitly invoke a specific hadler, as they are unaware of the available handlers. The user only needs to provide the task.
        - User queries must not explicitly reference or request specific internal components (e.g., handler types,or invocation instructions). The query should focus solely on the intent or requirement, without revealing or directing internal system behavior. Let the system decide what to invoke based on context.
    - Use the mcp handler description to guide what the query is trying to achieve.
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
            - You must provide a detailed, imaginative yet context-grounded narrative of the user's earlier actions. Include:
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

🧠 “While generating each data point, I must actively decide which required parameters appear in the query, which appear in the conversation_summary, and which are left missing — based on the combination pattern being implemented.”


3. tool_name → Human-Readable Alias
- Purpose: Generate a task-focused alias for the handler, different from handler_name.
- Rule: Should reflect the operation performed by the handler.
    - Example: 
     - "tool_name": "setup_patient_visit"

4. reasoning 
- Justification for Tool & Suggestions
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

    -Tool Selected – Example 1 :
        - The user is requesting details of a Jira ticket, which aligns well with the JiraMCP_jira_get_issue_details handler. All necessary inputs are present, so the request is successfully routed to the jira_ticketer_tool.

    -Tool Not Selected – Example 2 :
        - The user’s intent matches the purpose of the JiraMCP_jira_get_issue_details handler; however, the request lacks sufficient parameters for invocation, so the tool is not selected.

        
7. chain_of_thought → Step-by-Step Reasoning 

    You are deciding whether a given MPC tool can be selected and invoked based on the available input.

    Follow this reasoning process step by step:

    Step 1:Intent Recognition:
    -Analyze the user's request to understand what they’re trying to do.Examine both the query and the conversation_summary.

    Step 2: Tool Identification:
    Search the handler registry to identify the most relevant tool. If the intent matches an MCP tool, select that tool from mcp_tools.

    Step 3:Parameter Check:
    -Review the tool's input_schema.required list.Identify Required Parameters. Extract all fields marked as required (e.g., ["patient_id", "appointment_type", "appointment_datetime"]).

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

    Example 1 (missing required requiremtns):
        "chain_of_thought": [
        "The user has made an urgent request to validate a payroll batch due to an approaching deadline.",
        "Based on the task, the `payroll_data_validation` tool is the most appropriate choice from the registry.",
        "According to its schema, the tool requires four fields: `payroll_data_batch`, `validation_ruleset`, `payroll_system_access`, and `hr_database_credentials`.",
        "From the conversation, we know that the `validation_ruleset` is set to 'FY25-Audit-Compliance', and that the HR database credentials are already available.",
        "However, the specific `payroll_data_batch` and the `payroll_system_access` credentials have not been provided.",
        "This tool does not support any optional parameters that could fill the gap.",
        "Since two required fields are missing, the tool cannot be safely invoked at this time.",
        "The confidence score is 0.72, reflecting a clear understanding of the request but insufficient data to proceed."
        ]

    Example 2 (no any missing requiremtns):
    "chain_of_thought": [
        "The user has requested to run the autograder on a homework assignment for the 'Advanced Algorithms' course.",
        "This task aligns perfectly with the `grade_assignment_automatically` tool in the system.",
        "The tool's input schema requires `assignment_id`, `submission_data`, `grading_rubric`, and `lms_api_key`.",
        "All these fields are explicitly mentioned in the user’s query and the conversation history: the assignment ID is 'CS-ALGO-HW4', submissions are in 'hw4_submissions.zip', the rubric is 'algo_hw4_rubric.yaml', and the API key is 'lms-api-cs-dept-9a8b7c6d'.",
        "Additionally, the user has specified a preference for the 'detailed feedback' template, which maps to the optional `feedback_template` parameter.",
        "With all required and optional parameters clearly provided, the tool is fully prepared for execution.",
        "The inputs align completely with the tool’s design and intended use.",
        "The confidence score is 0.98, indicating high certainty in tool selection and readiness."
    ]

---

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
| `output`       | `copilot_id`                    | **Keep original copilot ID**         |
| `output`       | `confidence`                    | **Should exactly match given value** |
| `output`       | `workspace_preference_override` | **Must stay untouched**              |


## Strict Rule
    - IMPORTANT: Outside of the fields listed above, no other parts of the original input or output JSON should be altered. 
    - This ensures structural consistency and compatibility with downstream pipelines. The format, nesting, and extra fields must remain exactly as in the original INPUT_JSON.
    - In Stage 1, generate an array of 6 distinct JSON items—each containing a unique combination of the required output fields. 
    - Then, in Stage 2, iterate over these 6 items to replace the corresponding fields in the input JSON schema, producing a final output array of 6 fully merged JSON objects reflecting the updated input and output sections. 
    - Return final stage 2 output as following list of array
        - [stage2_item1, stage2_iitem2, stage2_iitem3,........, stage2_iitem6].

- This marks the end of the prompt, and the final response should return this array of 6 complete JSON items."

"""
