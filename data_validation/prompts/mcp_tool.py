MCP_TOOL_PROMPT = """

based on bellow  given instructions validate following json:  

You are a validation agent responsible for both evaluating and refining structured JSON inputs.

Your behavior follows a strict 3-stage process:



Below is a concise validation section specifically for evaluating the provided `mcp_tool` JSON object, which represents a single mcp_tool in a `handler_registry.mcp_tools` list. The section is designed to validate the structure and content of the mcp tool object, ensuring it meets schema requirements and logical constraints. It aligns with clear terminology, streamlined rules, and edge case handling.


# Stage 1

## Schema Validation
-
You are a validation agent responsible for evaluating and refining structured JSON inputs for an MCP tools context, based on the provided JSON and schema. Your behavior follows a strict 3-stage process: validation, refinement (if invalid), and post-refinement re-validation. 
---

### *schem Validation**

Validate the provided JSON against the following schema, ensuring all required fields are present, data types are correct, and content is logically coherent. The schema is  for `mcp_tools`

```json
{
  "input": {
    "id": "Required. String in UUID format (e.g., '33af660b-6ac4-46ed-8544-8ccb73ca27a0'). Must not be null.",
    "timestamp": "Required. String in ISO 8601 datetime format (e.g., '2023-08-03T00:45:51.547020'). Must not be null.",
    "query": "Required. Non-empty string. Must not be null. Must be realistic, no dummy values.",
    "conversation_summary": "Non-empty or empty string. Must be realistic, no dummy values",
    "handler_registry": {
      "mcp_tools": "Required. Non-empty list of objects, each with 'name' (string), 'server_name' (string), 'description' (string), 'input_schema' (object with 'type', 'properties', 'required'),",
      "worker_agents": "Required. Must be an empty list ([]).",
      "llm_handlers": "Required. Must be an empty list ([]).",
      "rag_handlers": "Required. Must be an empty list ([]).",
      "compiled_at": "Required. String in ISO 8601 datetime format. Must not be null.",
      "user_id": "Required. String in UUID format. Must not be null.",
      "workspace_id": "Required. String in UUID format. Must not be null."
    },
    "copilot_id": "Optional. String in UUID format or null.",
    "thread_id": "Required. Non-empty string. Must not be null."
  },
  "output": {
    "select_handler_type": "Required. Must be 'mcp_tool'.",
    "handler_name": "Required. Non-empty string. Must match the 'name' field of an object in input.handler_registry.mcp_tools. Must not be null. Must be realistic, no dummy values.",
    "server_name": "Required. Non-empty string. Must match the 'server_name' field of the selected mcp_tool. Must not be null.",
    "tool_name": "Required. Non-empty string. Must be realistic and align with the tool's purpose. Must not be null. shoul not to be similar as handler_name",
    "copilot_id": "Must be null.",
    "missing_fields": "Required. List of strings (can be empty).",
    "optional_suggestions": "Required. List of strings (can be empty). Suggests optional fields from the handler's input_schema.properties.",
    "suggested_payload": "Required. Dictionary (can be empty in Case A).",
    "confidence": "Required. Float between 0.5 and 1.0 (inclusive).",
    "reasoning": "Required. Non-empty string justifying why the selected handler is suitable.",
    "chain_of_thought": "Required. Non-empty list of strings describing the step-by-step evaluation process.",
    "workspace_preference_override": "Required. Must be false."
  }
}

--



### **input.id**

- **Presence**: Must not be null.
- **Data Type**: String in UUID format.
- **Content**: Must be a valid, unique identifier.

---

### **input.timestamp**

- **Presence**: Must not be null.
- **Data Type**: String in ISO 8601 datetime format (e.g., `2025-04-23T21:04:45.124977`).
- **Content**: Must represent a valid datetime.

---

### **input.query**

- **Presence**: Must not be null.
- **Data Type**: Non-empty string.
- **Content**: Must clearly specify the user’s request (e.g., running a schedule adjuster with project and event details). 

---

### **input.conversation_summary**

- **Presence**: Must not be null.
- **Data Type**: can be empty or Non-empty string.
- **Content**: Must provide relevant context about prior user interactions (e.g., project monitoring details).

---

### **input.handler_registry**

- **Presence**: Must not be null.
- **Data Type**: Object with:
  - mcp_tools: Non-empty list of objects, each with:
        -name: Non-empty string.
        -server_name: Non-empty string describing the server hosting the tool (e.g., AidocMCP).
        -description: Non-empty string describing functionality.
        -input_schema: Object with type: "object", properties (object with field definitions), required (array of strings) .
  - `worker_agents`:  Empty list (`[]`)
  - `llm_handlers`: Empty list (`[]`).
  - `rag_handlers`: Empty list (`[]`).
  - `compiled_at`: ISO 8601 datetime string.
  - `user_id`: UUID string.
  - `workspace_id`: UUID string.

- **Content**:
  - `mcp_tools` objects must align with the query’s task (e.g., schedule adjustment).
  - `input_schema.required` must only include fields from `input_schema.properties`.
  - All UUIDs and URLs must be valid.

---

### **output.select_handler_type**

- **Presence**: Must not be null.
- **Data Type**: String, must be `"mcp_tool"`.
- **Content**: Must match the handler type used in the system (mcp tool for schedule adjustment tasks).

---

### **output.handler_name**

- **Presence**: Must not be null.
- **Data Type**: Non-empty string.
- **Content**: Must match the `name` field of an object in `input.handler_registry.mcp_tools` (e.g., `dynamic_schedule_adjuster`).

---

### **output.server_name**

- **Presence**: Must be null.
- **Data Type**: Must be `null`.
- **Content**: No value allowed, as server name is not used in this context.

---

### **output.tool_name**

    -Presence: Must not be null.
    -Data Type: Non-empty string.
    -Content: Must match the server_name field of the selected mcp_tool in input.handler_registry.mcp_tools (e.g., AidocMCP). 
    -Must be realistic and align with the tool’s purpose.

---

### **output.copilot_id**

- **Presence**: Must be null.
- **Data Type**: Must be `null`.
- **Content**: No value allowed, as copilot ID is not used in this worker mcp_tool context.

---

### **output.optional_suggestions**

- Presence: Must not be null.
-Data Type: Non-empty string.
-Content: Must be a realistic name describing the tool’s function (e.g., request_radiology_analysis). Must align with the selected mcp_tool’s purpose. 
-should not be equal to handler_name. but it should soundlike similar

---

### **output.confidence**

- **Presence**: Must not be null.
- **Data Type**: Float between 0.5 and 1.0 (inclusive).
- **Content**: Must reflect the system’s confidence in the handler selection (e.g., `0.890368`), verifiable in `output.chain_of_thought`.

---

### MCP_TOOL Object Validation
- Validate a single mcp tool object from a handler_registry.mcp_tools list against the schema below. Ensure all required fields are present, data types are correct, and content is logically coherent for use in a mcp tool-based system.
{
  "name": "Required. Non-empty string. Unique identifier for the MCP tool. Must not be null. Must be realistic, no dummy values.",
  "server_name": "Required. Non-empty string. Must not be null. Must be realistic.",
  "description": "Required. Non-empty string describing the tool’s functionality. Must not be null. Must be realistic, no dummy values.",
  "input_schema": "Required. Object with 'type' (string, must be 'object'), 'properties' (object with field definitions), and 'required' (array of strings). Must not be null.",
  "workspace_id": "Required. String in UUID format (e.g., '7c453ac8-cccf-4d83-8cda-a970c3c85a8a'). Must not be null."
}

1. **Schema Validation**:
    -Check for required fields (name, server_name, description, input_schema, workspace_id) and correct data types.
    -Ensure input_schema structure is valid (type, properties, required).

2. **Content Validation**:
   - Confirm name, server_name, and description align with the tool’s purpose (e.g., radiology analysis).
    -Verify input_schema.required fields are defined in input_schema.properties.

### **Example worker_agent hanlder to Validate**

```json
{
                    "name": "request_ai_radiology_analysis",
                    "server_name": "AidocMCP",
                    "description": "Submits a retrieved imaging study to an AI radiology platform for analysis and preliminary findings. :param study_instance_uid: The unique identifier for the imaging study to be analyzed. :param analysis_type: The type of analysis to perform, e.g., 'stroke_detection', 'fracture_assessment'. :return: An analysis ID to track the progress and retrieve results. (Server: AidocMCP)",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "study_instance_uid": {
                                "title": "Study Instance UID",
                                "type": "string"
                            },
                            "analysis_type": {
                                "title": "Analysis Type",
                                "type": "string"
                            }
                        },
                        "required": [
                            "study_instance_uid",
                            "analysis_type"
                        ]
                    }
                }
```

### **Critical Evaluation for output.missing_fields and output.suggested_payload**

**Critical Note**: These fields are critical to evaluate as they determine whether the required parameters for the mcp tools are correctly identified and handled. Pay close attention to matching the `handler_registry.mcp_tools.input_schema.required` fields with data extracted from `input.query` and `input.conversation_summary`.

---

### **output.missing_fields**

- **Presence**: Must not be null.
- **Data Type**: List of strings (can be empty).
- **Content**:
  - Identify required parameters from `input.handler_registry.mcp_tools[].input_schema.required` for the selected `handler_name` (e.g., `["project_id", "triggering_event_id"]`).
  - Check if each required parameter is present in `input.query` or `input.conversation_summary`.
  - **Behavior**:
    - **If all required parameters are found**: `missing_fields` must be an empty list (`[]`).
    - **If any required parameters are missing**: List the missing parameter names (e.g., `["fieldX"]`).
  - **Validation**:
    - Ensure listed fields are only those in `input_schema.required` and not present in `input.query` or `input.conversation_summary`.
    - If non-required fields are listed, it is invalid.
    - If `missing_fields` includes fields present in `input.query` or `input.conversation_summary`, it is invalid.

---

### **output.suggested_payload**

- **Presence**: Must not be null.
- **Data Type**: Dictionary (can be empty in Case A).
- **Content**:
  - Must align with `input.handler_registry.mcp_tools[].input_schema.required` for the selected `handler_name`.
  - Follow these cases based on required parameter availability in `input.query` and `input.conversation_summary`:
    - **Case A: All Required Fields Missing**:
      - **Trigger**: None of the required parameters are found in `input.query` or `input.conversation_summary`.
      - **Output**: Empty dictionary (`{}`).
          * 🔹 **What to Output:**
                    ```json
                    "missing_fields": ["field1", "field2", "field3"],
                    "suggested_payload": {}
                    ```
      - **Validation**: Ensure `suggested_payload` is empty and all required fields are listed in `missing_fields`.
    - **Case B: Some Required Fields Missing**:
      - **Trigger**: At least one required parameter is found, but some are missing.
      - **Output**: Include:
        - Available parameters with values extracted from `input.query` or `input.conversation_summary`.
        - Missing parameters with value `"missing"`.
        - A `summary` key with a natural English sentence describing the user’s request (e.g., `"User requests schedule adjustment for a project due to a supply chain failure."`).
      - **Validation**: Ensure all required fields are listed, missing fields are marked `"missing"`, and `summary` is present and accurate.

        * 🔹 **What to Output:**
                    ```json
                    "missing_fields": ["fieldX"],
                    "suggested_payload": {
                        "fieldA": "value_from_query_or_memory",
                        "fieldX": "missing",
                        "summary": "A natural sentence clearly describing what the user wants."
                    }
                    ```

    - **Case C: No Required Fields Missing**:
      - **Trigger**: All required parameters are found in `input.query` or `input.conversation_summary`.
      - **Output**: Include all required parameters with their extracted values, no `summary` or `"missing"` markers.
      - **Validation**: Ensure all required fields are present with correct values, and no extra fields (like `summary`) are included.

          * **What to Output:**
        ```json
        "missing_fields": [],
        "suggested_payload": {
            "field1": "value1",
            "field2": "value2"
        }
        ```
        
  - **Validation**:
    - Values must match those in `input.query` or `input.conversation_summary` exactly.
    - Do not invent values; use `"missing"` for unavailable parameters in Case B.
    - If `missing_fields` is non-empty, `suggested_payload` must reflect Case A or B, not C.

---

### **Validation Process**

1. **Identify Required Parameters**:
   - Extract `input_schema.required` from the selected `mcp_tools` object in `input.handler_registry` (e.g., `["project_id", "triggering_event_id"]`).
2. **Check Parameter Availability**:
   - Search `input.query` and `input.conversation_summary` for each required parameter’s value.
3. **Evaluate missing_fields**:
   - If all parameters are found, `missing_fields` must be `[]`.
   - If any are missing, list them in `missing_fields`.
4. **Evaluate suggested_payload**:
   - Apply Case A, B, or C based on parameter availability.
   - Ensure `summary` is included only in Case B and accurately reflects the user’s request.
5. **Error Checks**:
   - invalid if `missing_fields` includes fields not in `input_schema.required` or present in `input.query`/`input.conversation_summary`.
   - invalide if `suggested_payload` includes fabricated values or omits required fields.
---

### output.workspace_preference_override
 - this should alwas be false


### Converstion_summary

- `conversation_summary` shoild not repeats or rephrases the user's current query.   These are often sentences that describe the same action or request already covered in the `query` field.
 
- Remove any sentence from the `conversation_summary` that:Describes, Summarizes, or Anticipates  the user's current query.
- These are typically:Forward-looking, - Reflective of the user's current intention
- They belong **only** in the `query` field, **not** in the summary of prior interactions.
- These Sentences Often:
    - Restate the current request
    - Describe what the user is trying to do right now
    - Predict or reflect their immediate goal

- Common Phrasings (Examples):
    - “Now, you are asking to…”
    - “You want to…”
    - “Today, you asked for…”
    - “Your goal is to…”
    - “Currently, you are trying to…”

####  What to Remove
- **Example 1**
**Query:**
> "I've transcribed five user interviews about our new prototype, 'WorkflowAI'. Can you analyze the transcripts and highlight all instances where users expressed feelings of confusion or delight?"

**Conversation Summary:**
> "As a UX researcher, you just completed a round of usability testing for the 'WorkflowAI' prototype. In a previous step, you used a tool to tag specific UI interaction problems, creating a list of 12 critical usability issues (e.g., 'user failed to find the export button'). **Now, you want to analyze the emotional component of the user feedback. Your goal is to extract direct quotes reflecting user sentiment to include in your final report for the product team, providing context beyond just the interaction errors.**"

**What should be removed:**
> **Remove:**
> "Now, you want to analyze the emotional component of the user feedback. Your goal is to extract direct quotes reflecting user sentiment to include in your final report for the product team, providing context beyond just the interaction errors."

###  Reasoning Field Requirements

The `reasoning` field must:

1. **Directly address whether the selected worker agent aligns with the user query.**

   * Clearly state if the selected agent is the correct match for the intent expressed in the `query`.

2. **State the invocation eligibility based on required parameters:**

   * If all required parameters are satisfied across `query` and `conversation_summary`:

     * The reasoning must confirm that **the agent can be invoked**.
   * If any required parameter is missing:

     * The reasoning must clearly state that **the agent cannot be invoked** due to missing required fields.
     * The reasoning should briefly mention which fields are missing or how the input is insufficient.

3. **Avoid contradictions with the chain\_of\_thought and output fields.**

   * The reasoning must summarize and align with the final conclusion from the `chain_of_thought`.
   * It must not introduce new logic or refer to mismatched handlers.

. **Maintain grammatical correctness and clarity.**

   * The reasoning should be a clean, coherent summary of the CoT, written in a formal.

--

###  Validation Instruction: `chain_of_thought` 

Use this checklist to verify that `chain_of_thought` correctly follow the generation framework for selecting and invoking worker agents.

---

#### **Intent Recognition**

* ✔ Ensure the CoT clearly analyzes the user’s intent using both `query` and `conversation_summary`.

#### **Worker Agent Identification**

* ✔ Confirm that the CoT identifies the selected `worker_agent` (by name) and justifies it based on task alignment.

#### **Required Parameter Validation**

* ✔ CoT must:

  * List all fields in `payload_schema.required`.
  * Check their presence in the `query` and/or `conversation_summary`.

#### **Coverage and Invocation Logic**

* ✔ If **all required fields are present**:

  * CoT must state the agent **can be invoked**.
  * Justify where each field was found.

* ✔ If **any required field is missing**:

  * CoT must state the agent **cannot be invoked**.
  * List all missing fields.
  * `output.missing_fields` must match the CoT.

* ✔ If optional fields are discussed, they must match `payload_schema.properties` and appear in `output.optional_suggestions`.

####  **Handler Selection & Confidence**

* ✔ CoT must conclude with:

  * The final selection status (invoked or not).
  * The selected `handler_name`.
  * The **exact** `confidence` value from output.

####  **Style and Tone**

* ✔ Use **first-person** perspective (“I assessed…”, “I determined…”).

#### **Output Field Consistency**

* ✔ All output fields must align with CoT and reasoning:

  * `select_handler_type`, `handler_name`, `missing_fields`, `optional_suggestions`, `confidence`, `suggested_payload`.

* If any output contradicts the CoT or reasoning, mark as **non-compliant**.


####  **Rule 1: Confidence Usage Is Mandatory and Exact**

* The `confidence` value in `output.confidence` **must be restated exactly** in the the `chain_of_thought` as it is defined value.
The sentence must connect the **confidence score** with the **invocation conclusion** ---

#### **Rule 2: Query and Summary Content Must Be Interpreted — Not Quoted**

* **Direct quotations from the `query` or `conversation_summary` are not allowed** in the CoT or reasoning.

  * E.g., Do **not** say:

    > “The user asked: ‘Can you help me check if a certificate is valid?’”

*  You must **paraphrase and interpret** the query or summary using natural reasoning language.

  * E.g., Say:

    > “The user appears to be requesting verification of a certificate’s validity...”

---

### Final Alignment and Consistency Check

All components — `query`, `conversation_summary`, 'hander_registy'`reasoning`, `chain_of_thought`, 'required field','missing_fields'` — **must be fully aligned and address the same intent and handler**.

* The selected `handler_name`, its purpose, and required parameters must be consistent across:
    * `output.handler_name`
    * The `reasoning` narrative
    * The `chain_of_thought` logic

* The `query` and `conversation_summary` must be **interpreted (not quoted)** and accurately reflected in the CoT.
* If a mismatch is found between any of these sections (e.g., handler mismatch, parameter mismatch, contradictory logic), the validator must:

  * Identify the minimal edit needed to bring all sections into alignment.
  * Ensure no new contradictions or errors are introduced during correction.

* The `reasoning` section must be **grammatically correct**, coherent, and free of sentence-level errors or awkward phrasing.
* The tone must remain consistent,first person or third person perspective is allowed.
--
### Finally :

You must thoroughly examine the logical relationships between the query, conversation summary, missing fields, suggested fields, reasoning, and the chain of thought. These elements should be tightly integrated, with each component logically supporting the others, ensuring the generated outputs are not only coherent and contextually aligned but also grammatically correct and semantically meaningful.

---


#### sample input : this is a correct data learn form this

 {"input": {"id": "33af660b-6ac4-46ed-8544-8ccb73ca27a0", "timestamp": "2023-08-03T00:45:51.547020", "query": "I've just pulled up the chest X-ray, study UID `2.16.840.1.113669.632.20.121511.20230802184511250.2`. Please send it for AI analysis.", "conversation_summary": "The user is working on a case involving a patient, Johnathan P. Meyers, who was brought in following a high-impact motor vehicle accident. The trauma protocol has been initiated.", "handler_registry": {"mcp_tools": [{"name": "request_ai_radiology_analysis", "server_name": "AidocMCP", "description": "Submits a retrieved imaging study to an AI radiology platform for analysis and preliminary findings. :param study_instance_uid: The unique identifier for the imaging study to be analyzed. :param analysis_type: The type of analysis to perform, e.g., 'stroke_detection', 'fracture_assessment'. :return: An analysis ID to track the progress and retrieve results. (Server: AidocMCP)", "input_schema": {"type": "object", "properties": {"study_instance_uid": {"title": "Study Instance UID", "type": "string"}, "analysis_type": {"title": "Analysis Type", "type": "string"}}, "required": ["study_instance_uid", "analysis_type"]}}], "worker_agents": [], "llm_handlers": [], "rag_handlers": [], "compiled_at": "2023-08-02T14:56:12.547020", "user_id": "0c4cbfa9-ab21-427b-88c7-0ddc43a1a5c8", "workspace_id": "7c453ac8-cccf-4d83-8cda-a970c3c85a8a"}, "copilot_id": null, "thread_id": "e387f73a-7f6e-49fd-b8e9-fd50ff55c930"}, "output": {"select_handler_type": "mcp_tool", "handler_name": "request_ai_radiology_analysis", "server_name": "AidocMCP", "tool_name": "submit_image_for_ai_review", "copilot_id": null, "missing_fields": ["analysis_type"], "optional_suggestions": [], "suggested_payload": {"study_instance_uid": "2.16.840.1.113669.632.20.121511.20230802184511250.2", "analysis_type": "missing", "summary": "Submit the chest X-ray with UID 2.16.840.1.113669.632.20.121511.20230802184511250.2 for AI analysis."}, "confidence": 0.668673, "reasoning": "The user's intent to submit an imaging study for AI analysis clearly matches the `request_ai_radiology_analysis` handler. While the `study_instance_uid` is provided, the mandatory `analysis_type` parameter is missing. The tool cannot be invoked until the specific type of analysis is clarified.", "chain_of_thought": ["The user wants to send a specific chest X-ray for AI analysis.", "This intent directly maps to the `request_ai_radiology_analysis` tool in the handler registry.", "I've examined the tool's schema, which requires two parameters: `study_instance_uid` and `analysis_type`.", "The `query` successfully provides the `study_instance_uid` as '2.16.840.1.113669.632.20.121511.20230802184511250.2'.", "However, after reviewing both the query and the conversation summary, I found that the `analysis_type` (e.g., 'fracture_assessment', 'pneumothorax_detection') has not been specified.", "Because a required parameter is missing, the tool cannot be executed.", "I will need to prompt the user to provide the analysis type before proceeding.", "The system's confidence score of 0.668673 reflects that the tool is a good match, but the inputs are incomplete."], "workspace_preference_override": false}}


##   Stage 2: Refinement (only if invalid)

If Stage 1 identified input json id as INVALID, you must refine the original input using only the issues list from Stage 1. No other assumptions should be made.

Refinement Rules:
  - Apply only the recommended fixes from the issues section in Stage 1.

  - Do not introduce new context withch create contradictions, and do not change the order.

  - Make sure each sentence is grammatically correct and logically connected.

  - All contextual relationships between fields must remain valid and meaningful.

  - The refinement must result in a clean, valid JSON, free of contradictions.

  - Do not include any explanatory text. 

---

## Stage 3: Post-Refinement Re-Validation

After refinement:

Re-run the validation process using all rules from Stage 1.

If the refined input now satisfies all validation rules, return:

{
  "status": "REFINED",
  "corrections": "Describe the issues identified and what changes were made to correct them.",
  "data": {
    # Include the updateded data point here
  }
}
If the refined input still fails validation, return:

{
  "status": "INVALID",
  "corrections": "Updated explanation of issues that could not be resolved."
  "data": {add ONLY the orginal INPUT JSON here}  
}

Important Constraints

Do not generate or invent new content outside of the issues described in recorection field.

Always preserve structural and contextual integrity.

All responses must be in pure JSON format. Do not include any additional commentary or text outside of the JSON block.




"""





