RAG_PROMPT = """

based on bellow  given instructions validate following json:  

You are a validation agent responsible for evaluating and refining structured JSON inputs for a rag system context, based on the provided JSON and schema. Your behavior follows a strict 3-stage process: validation, refinement (if invalid), and post-refinement re-validation

### **Stage 1: Validation**


Validate the provided JSON against the following schema, ensuring all required fields are present, data types are correct, and content is logically coherent.

```json
{
  "input": {
    "id": "Required. String in UUID format (e.g., 'bd76d69c-3e71-4c47-9d32-5d110653ef6d'). Must not be null.",
    "timestamp": "Required. String in ISO 8601 datetime format (e.g., '2024-09-19T01:27:18.222130'). Must not be null.",
    "query": "Required. Non-empty string. Must not be null. Must be realistic, no dummy values.",
    "conversation_summary": "Non-empty or empty string. Must be realistic, no dummy values",
    "handler_registry": {
      "mcp_tools": "Required. Must be an empty list ([]).",
      "worker_agents": "Required. Must be an empty list ([]).",
      "llm_handlers": "Required. Must be an empty list ([]).",
      "rag_handlers": "Required. Non-empty list of objects, each with 'name' (string), 'description' (string), 'handler_payload' (object with a 'copilot_id' string in UUID format).",
      "compiled_at": "Required. String in ISO 8601 datetime format. Must not be null.",
      "user_id": "Required. String in UUID format. Must not be null.",
      "workspace_id": "Required. String in UUID format. Must not be null."
    },
    "copilot_id": "Optional. String in UUID format or null.",
    "thread_id": "Required. Non-empty string. Must not be null."
  },
  "output": {
    "select_handler_type": "Required. Must be 'rag'.",
    "handler_name": "Required. Non-empty string. Must match the 'name' field of an object in input.handler_registry.rag_handlers. Must not be null. Must be realistic, no dummy values.",
    "server_name": "Must be null.",
    "tool_name": "Must be null.",
    "copilot_id": "Required. String in UUID format.Must match the 'copilot_id' in the selected rag_handler's handler_payload. Must not be null.",
    "missing_fields": "Must be empty list ([]).",
    "optional_suggestions": "Must be empty list ([]).",
    "suggested_payload": "Required. empty Dictionary, should be empty ({})",
    "confidence": "Required. Float between 0.5 and 1.0 (inclusive).",
    "reasoning": "Required. Non-empty string justifying why the selected RAG handler is suitable is provided here.",
    "chain_of_thought": "Required. Non-empty list of strings ",
    "workspace_preference_override": "Required. Must be false."
  }
}
```

#### **RAG Handler Object Validation**
Validate a single RAG handler object from `input.handler_registry.rag_handlers`:
```json
{
  "name": "Required. Non-empty string. Unique identifier for the RAG handler. Must not be null. Must be realistic, no dummy values.",
  "description": "Required. Non-empty string describing the handler’s functionality (e.g., retrieving curriculum-aligned content). Must not be null. Must be realistic, no dummy values.",
  "handler_payload": "Required. Object containing a 'copilot_id' field (string in UUID format). Must not be null."
}
```
1. **Schema Validation**:
   - Check for required fields (`name`, `description`, `handler_payload.copilot_id`) and correct data types.
2. **Content Validation**:
   - Confirm `name` and `description` align with the handler’s purpose (e.g., retrieving educational content).
   - Verify `handler_payload.copilot_id` is a valid UUID string.

#### **Logical Conditions**
- **Query-Based Handler Selection**:
  - The `input.query` must align with the selected RAG handler’s purpose (e.g., educational queries for a learning objective mapper).
  - The selected `output.handler_name` must match a `name` in `input.handler_registry.rag_handlers`.
  - The `output.copilot_id` must match the `copilot_id` in the selected handler’s `handler_payload`.
- **Validation**:
  - Invalid if `output.handler_name` does not match any `name` in `input.handler_registry.rag_handlers`.
  - Invalid if `output.copilot_id` does not match the `copilot_id` in the selected handler’s `handler_payload`.
  - Invalid if `input.query` does not align with the selected handler’s purpose (e.g., a non-educational query for a learning objective mapper).
  - Invalid if `workspace_preference_override` is `true` (must always be `false` for RAG handlers).

#### **Input Field Validation**
- **input.id**: Must be a valid UUID string, not null.
- **input.timestamp**: Must be a valid ISO 8601 datetime string, not null.
- **input.query**: Must be a non-empty, realistic string specifying the user’s request (e.g., seeking educational content).
- **input.conversation_summary**: Optional, can be empty or a realistic string providing context.
- **input.handler_registry**:
  - `mcp_tools`, `worker_agents`, `llm_handlers`: Must be empty lists (`[]`).
  - `rag_handlers`: Non-empty list of valid RAG handler objects.
  - `compiled_at`: Valid ISO 8601 datetime string.
  - `user_id`, `workspace_id`: Valid UUID strings.
- **input.copilot_id**: UUID string or null.
- **input.thread_id**: Non-empty string, typically UUID.

#### **Output Field Validation**
- **output.select_handler_type**: Must be `"rag"`.
- **output.handler_name**: Must match `name` in `input.handler_registry.rag_handlers`.
- **output.server_name**: Must be `null`.
- **output.tool_name**: Must be `null`.
- **output.copilot_id**: Must match the `copilot_id` in the selected handler’s `handler_payload`.
- **output.missing_fields**: Must be empty list (`[]`).
- **output.optional_suggestions**: Must be empty list (`[]`).
- **output.suggested_payload**: Mus be empty (`{}`).
- **output.confidence**: Float between 0.5 and 1.0, reflecting handler selection confidence.

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

1. **Directly address whether the selected handler is  aligns with the user query.**

   * Clearly state if the selected handler is the correct match for the intent expressed in the `query`.

3. **Avoid contradictions with the chain\_of\_thought and output fields.**

   * The reasoning must summarize and align with the final conclusion from the `chain_of_thought`.
   * It must not introduce new logic or refer to mismatched handlers.

. **Maintain grammatical correctness and clarity.**

   * The reasoning should be a clean, coherent summary of the CoT, written in a formal,.

--

###  Validation Instruction: `chain_of_thought` 

Use this checklist to verify that `chain_of_thought` correctly follow the generation framework for selecting and invoking the handler.

---

#### **Intent Recognition**

* ✔ Ensure the CoT clearly analyzes the user’s intent using both `query` and `conversation_summary`.

#### **handler Identification**

* ✔ Confirm that the CoT identifies the selected `handler` (by name) and justifies it based on task alignment.

####  **Handler Selection & Confidence**

* ✔ CoT must conclude with:

  * The final selection handler.
  * The selected `handler_name`.
  * The **exact** `confidence` value from output.
  * include the selected copile id 

####  **Style and Tone**

* ✔ Use **first-person** perspective (“I assessed…”, “I determined…”).

#### **Output Field Consistency**

* ✔ All output fields must align with CoT and reasoning:

  * `select_handler_type`, `handler_name`, `confidence`, `suggested_payload`.

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

    * Final Alignment and Consistency Check

    All components — `query`, `conversation_summary`, 'hander_registry'`reasoning`, `chain_of_thought`, '` — **must be fully aligned and address the same intent and handler**.

    * The selected `handler_name`, its purpose, must be consistent across:
        * The `reasoning` narrative
        * The `chain_of_thought` logic

    * `reasoning` must summarize the same judgment expressed in the CoT, not contradict or reinterpret it.
    * The `query` and `conversation_summary` must be **interpreted (not quoted)** and accurately reflected in the CoT.
    * If a mismatch is found between any of these sections (e.g., handler mismatch, parameter mismatch, contradictory logic), the validator must:

      * Identify the minimal edit needed to bring all sections into alignment.
      * Ensure no new contradictions or errors are introduced during correction.

    * The `reasoning` and chain_of_thoughtsection must be **grammatically correct**, coherent, and free of sentence-level errors or awkward phrasing.
    * The tone must remain consistent, formal, and written 
  - Must demonstrate clear decision-making, comparing the selected handler to others.
  - Must address invocation feasibility (e.g., availability of copilot_id).




#### **Logical Integration**
- Thoroughly examine the logical relationships between the query, conversation summary, missing fields, suggested fields, reasoning, and chain of thought.
- Ensure these elements are tightly integrated, with each component logically supporting the others, and are coherent, contextually aligned, grammatically correct, and semantically meaningful.


---

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
