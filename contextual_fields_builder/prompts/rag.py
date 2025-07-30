RAG_PROMPT ="""

You are a knowledge system analyst.

You will be given an input JSON containing a `handler_registry` with its metadata. Your task is to **simulate realistic usage scenarios** by filling ONLY the following empty fields in the corresponding JSON block:

- `query`: A natural language question that a user would ask related to this registry's  rag copilet capabilities.
- `conversation_summary`: A realistic prior user interaction summarizing what has been discussed before (e.g., exploration, debugging context, or code-related discussion).
- `reasoning`: A short justification for why the selected handler (e.g., `code_context_expander`) is suitable for the given query.
- `chain_of_thought`: A step-by-step decision trace explaining why this handler was selected over others, referencing the query, possible memory state, copilot goals, and evidence from the handler's capabilities.

### Step 1: Scan Available RAG Handlers
You inspect the handler_registry.rag_handlers section, which lists all RAG-based copilots available in the current workspace.
For each handler, consider:
    - The name and description fields
    - The handler_payload which includes the copilot_id

The match between the user query and the handler’s domain of expertise

## TASK OVERVIEW:
- This task involves a two-stage process for each INPUT_JSON provided:
    -STAGE 1 — Generate Content: Based on the INPUT_JSON, generate 4 unique and dynamic data entries. Each entry will contain a user query, the reasoning for the routing decision, and a detailed chain-of-thought.
    -STAGE 2 — Update and Finalize JSON: For each of the 4 generated entries, create a deep copy of the original INPUT_JSON and inject the generated content into the appropriate fields.

### STAGE 1
You will be given  a SAMPLE INPUT JSONL as follows:
{"input":{"id":"4293fa4f-9099-4a5e-b645-b70c68863b0e","timestamp":"2025-03-23T12:16:35.085127","query":"","conversation_summary":"","handler_registry":{"mcp_tools":[],"worker_agents":[],"llm_handlers":[],"rag_handlers":[{"name":"lecture_summary_generator","description":"Summarizes lengthy lectures, academic articles, or chapters into concise/bullet points or brief paragraphs for quick review.","handler_payload":{"copilot_id":"931abcf2-5f1f-4a8a-9f63-e335467f1209"}}],"compiled_at":"2025-03-21T15:50:51.085127","user_id":"c473d21c-901b-431e-a758-62c82e4e70ab","workspace_id":"234e8b34-2bd8-4c41-a6e1-e26981867fb7"},"copilot_id":null,"thread_id":"64bbf60c-107e-45b4-abba-dba14ccf1dec"},"output":{"select_handler_type":"rag","handler_name":"lecture_summary_generator","server_name":null,"tool_name":null,"copilot_id":"931abcf2-5f1f-4a8a-9f63-e335467f1209","missing_fields":[],"optional_suggestions":[],"suggested_payload":{},"confidence":0.67089,"reasoning":"","chain_of_thought":[],"workspace_preference_override":false}}

containing a `handler_registry` with its metadata. Your task is to **simulate realistic usage scenarios** by filling ONLY the following empty fields in the corresponding JSON block
- `query`: A natural language question that a user would ask related to this registry's  rag copilet capabilities.
- `conversation_summary`: A realistic prior user interaction summarizing what has been discussed before (e.g., exploration, debugging context, or code-related discussion).
- `reasoning`: A short justification for why the selected handler (e.g., `code_context_expander`) is suitable for the given query.
- `chain_of_thought`: A step-by-step decision trace explaining why this handler was selected over others, referencing the query, possible memory state, copilot goals, and evidence from the handler's capabilities.


- Generate **4 dynamic and diverse** outputs based on the `INPUT_JSON` content.
    - Each output must strictly follow the output schema below.
    - Each entry should reflect a **unique, realistic scenario**, using different user queries,

- Required output for the stage 1:
    {
    "query": "<string>", // Natural-language user request
    "conversation_summary": "<string>", // Nprio converstions with the given copilet
    "reasoning": "<string>", // Short explanation of rag choice
    "chain_of_thought": ["<string>", "<string>", "..."] // Step-by-step self-reflective reasoning
    }
Example of stage 1 output

-      {
        "query": "I'm preparing a compliance brief for our expansion into Southeast Asia. Can you provide a summary of the key differences in data privacy regulations (similar to GDPR) for financial institutions in Singapore, Malaysia, and Vietnam?",
        "conversation_summary": "The user has been tasked with creating a market-entry risk assessment report. Earlier, they requested information on capital adequacy requirements for the same set of countries.",
        "reasoning": "The user is requesting a comparative summary of financial regulations ('data privacy regulations for financial institutions') across multiple jurisdictions. The `regulatory_compliance_search` handler is the appropriate tool as it is designed to retrieve and interpret such 'financial regulations' and 'compliance guidelines.'",
        "chain_of_thought": [
            "The user's query asks for a comparative summary of 'data privacy regulations' for 'financial institutions' across three different countries: 'Singapore, Malaysia, and Vietnam'.",
            "The `conversation_summary` confirms the user's broader goal: a 'market-entry risk assessment', which often involves comparing regulatory landscapes. This context reinforces the need for a regulation-focused tool.",
            "I've examined the `handler_registry` and the `regulatory_compliance_search` handler is the only one available. Its description states it retrieves 'financial regulations, compliance guidelines, and legal interpretations'.",
            "Data privacy laws, especially as they apply to financial institutions, are a key component of the regulatory framework. The user's request to compare these laws across several jurisdictions is a complex task that fits the handler's domain.",
            "The handler is designed to pull this type of information, making it the only suitable option to address the user's multi-jurisdictional compliance question.",
            "The alignment between the query's focus on cross-border financial regulations and the handler's explicit purpose justifies the selection. I am choosing the `regulatory_compliance_search` handler with a confidence of 0.86."
        ],
      }
  
- Then pass them to stage 2 for futher processing
    - The JSON objects generated in Stage 1 are intermediate artifacts intended exclusively for internal use. They should not be exposed back to the end user.
    - This structure is designed to support Stage 2 processing, enabling more effective reasoning, enrichment, or validation downstream. By producing structured, machine-readable representations in Stage 1, we lay the groundwork for more intelligent decision-making in Stage 2.

### STAGE 2 
- Apply generated fields to INPUT_JSON:
- For each generated output entry in stage 1:
    - 1. Create a deep copy of the original INPUT_JSON.
    - 2. Replace or update the corresponding fields in the deep copy with the stage 1  values as follows:
        - input.query → from generated query
        - input.conversation_summary → from generated conversation_summary
        - output.reasoning → from generated reasoning
        - output.chain_of_thought → from generated chain_of_thought
- This yields 4 updated INPUT_JSON objects, each representing one enriched and realistic scenario.
- All the  other fields in the original INPUT_JSON remain unchanged .
-The final output should be a list of 4 modified JSON objects, each being a fully updated copy of the original INPUT_JSON,  with the following updated values  in its input and  output fields replaced using the generated schema fields.
    - Example output structure of a single modified output:

        {
        "input": {
            "query": "<replaced with Stage 1 → query>",
            "conversation_summary": "<replaced with Stage 1 → conversation_summary>",
            "other_fields_preserved": "..."
        },
        "output": {
            "reasoning": "<replaced with Stage 1 → reasoning>",
            "chain_of_thought": [
            "<replaced with Stage 1 → chain_of_thought 1>",
            "<replaced with Stage 1 → chain_of_thought 2>",
            "...",
            "<final conclusion>"
            ],
        }
        }

- Final Output After Stage 2 Injection (Updated Only Targeted Fields)

{
  "input": {
      "id": "1c45c26b-67a4-4a5f-94d3-e7f04c633a65",
      "timestamp": "2025-03-23T12:16:35.085127",
      "query": "I'm preparing a compliance brief for our expansion into Southeast Asia. Can you provide a summary of the key differences in data privacy regulations (similar to GDPR) for financial institutions in Singapore, Malaysia, and Vietnam?",
      "conversation_summary": "The user has been tasked with creating a market-entry risk assessment report. Earlier, they requested information on capital adequacy requirements for the same set of countries.",
      "handler_registry": {
          "mcp_tools": [],
          "worker_agents": [],
          "llm_handlers": [],
          "rag_handlers": [
              {
                  "name": "regulatory_compliance_search",
                  "description": "Retrieves financial regulations, compliance guidelines, and legal interpretations relevant to banking operations.",
                  "handler_payload": {
                      "copilot_id": "1f9d472e-0bea-4898-baab-fdef8cd70c96"
                  }
              }
          ],
          "compiled_at": "2025-03-21T15:50:51.085127",
          "user_id": "c473d21c-901b-431e-a758-62c82e4e70ab",
          "workspace_id": "234e8b34-2bd8-4c41-a6e1-e26981867fb7"
      },
      "copilot_id": null,
      "thread_id": "64bbf60c-107e-45b4-abba-dba14ccf1dec"
  },
  "output": {
      "select_handler_type": "rag",
      "handler_name": "regulatory_compliance_search",
      "server_name": null,
      "tool_name": null,
      "copilot_id": "1f9d472e-0bea-4898-baab-fdef8cd70c96",
      "missing_fields": [],
      "optional_suggestions": [],
      "suggested_payload": {},
      "confidence": 0.86,
      "reasoning": "The user is requesting a comparative summary of financial regulations ('data privacy regulations for financial institutions') across multiple jurisdictions. The `regulatory_compliance_search` handler is the appropriate tool as it is designed to retrieve and interpret such 'financial regulations' and 'compliance guidelines.'",
      "chain_of_thought": [
          "The user's query asks for a comparative summary of 'data privacy regulations' for 'financial institutions' across three different countries: 'Singapore, Malaysia, and Vietnam'.",
          "The `conversation_summary` confirms the user's broader goal: a 'market-entry risk assessment', which often involves comparing regulatory landscapes. This context reinforces the need for a regulation-focused tool.",
          "I've examined the `handler_registry` and the `regulatory_compliance_search` handler is the only one available. Its description states it retrieves 'financial regulations, compliance guidelines, and legal interpretations'.",
          "Data privacy laws, especially as they apply to financial institutions, are a key component of the regulatory framework. The user's request to compare these laws across several jurisdictions is a complex task that fits the handler's domain.",
          "The handler is designed to pull this type of information, making it the only suitable option to address the user's multi-jurisdictional compliance question.",
          "The alignment between the query's focus on cross-border financial regulations and the handler's explicit purpose justifies the selection. I am choosing the `regulatory_compliance_search` handler with a confidence of 0.86."
      ],
      "workspace_preference_override": false
  }
}

       
- The final output must strictly preserve the structure of the original INPUT_JSON schema. Only the specified fields should be updated with values from Stage 2, while all other keys and nesting should remain exactly the same to ensure structural consistency.

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

## Key sections to Consider When Generating Each Data Point

-Handler Registry – RAG Reading Guide
    -"handler_registry": {"mcp_tools": [], "worker_agents": [], "llm_handlers": [], "rag_handlers": [{"name": "regulatory_compliance_search", "description": "Retrieves financial regulations, compliance guidelines, and legal interpretations relevant to banking operations.", "handler_payload": {"copilot_id": "1f9d472e-0bea-4898-baab-fdef8cd70c96"], 
    -Study the tool listed in the handler_registry carefully. This is where all rag details are defined. Treat it as the source of truth.
        -Name: regulatory_compliance_search
        -Purpose:. To retrieve legal, financial, and compliance-related information relevant to banking operations.
        -Description :  Identify Core Responsibilities:, Intended Use Cases

## Schema Generation Instructions
-You have to follow guidance during the following field creating process

1. query → Human-Readable Question
    - Role: End User Simulation . 
    - Purpose: Simulate how a real user would ask the system to perform an action using natural language — reflecting their intent, not internal tool mechanics and create a Question for each training data point.
    - Guidelines for query Generation:
        - Act from a User’s Perspective:
            - The query must reflect what a user would naturally say when asking the system to perform a task. 
        - Study the Handler Registry First:
            - Before crafting the query:
            - Review the handler's description in the handler registry to understand what the rag  is designed to do. Use them to construct a natural-sounding, context-aware query.
        - Flexible Format:
            - The query can be a single sentence or a couple of brief, coherent sentences.
            - Ensure it flows naturally, like something a user would speak or type.
            - Avoid making it sound like a system-generated prompt or form-fill request.
            - Ensure query  align with the handler's domain (e.g., use real-looking IDs, dates, etc.).
        - Bad Examples (System-oriented or unrealistic):
            - “Please provide the student ID and performance data.”  -->This is how a system would ask, not a user.
            - “Enter the physician ID for scheduling.” --> Users don’t think in terms of field names.
            - dummy text like "test" or "example". --> these are not using by enterprise level senarios
        - Good Examples (User-oriented and realistic):
            - “Can you help generate a personalized learning plan for a student?”
        - Vary Phrasing: For the 4 scenarios, create different types of queries:
            - Direct: A clear, factual request. ("Pull up the EU requirements for correspondent banking.")
            - Indirect: A request embedded in a larger context. ("I'm checking our AML audit and need to confirm if FATF rule 10 applies to shell companies.")
            - Uncertain: A query from a confused user. ("We got a flag on a transaction. Are there EU sanctions we might have missed?")
            - Batch: A request covering multiple items or jurisdictions. ("I need a breakdown of KYC requirements for France, Germany, and Italy.")
            -user s not part of the system and should not be made aware of its internal behavior. Do not instruct the user to explicitly invoke a specific hadler, as they are unaware of the available handlers. The user only needs to provide the task.
                - User queries must not explicitly reference or request specific internal components (e.g., handler types,or invocation instructions). The query should focus solely on the intent or requirement, without revealing or directing internal system behavior. Let the system decide what to invoke based on context.


 2 conversation_summary 

The `conversation_summary` simulates realistic, memory-aware interactions between a user and the system. It acts as a **contextual bridge** between past and present queries, helping the system reason about continuity, intent, and user goals.
Begin by understanding the handler’s functionality. 

    -Guideline to cretate conversation_summary
        -Ground it in the Handler’s Purpose
            - ead the handler_registry entry carefully .
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
        conversation_summary = []

-Example for Converstion memory
    > *user previously explored how the `DataSyncManager` interacts with `SyncWorker` during job execution. After retrieving class definitions and init methods, user asked for related design notes tied to the `stream_batch()` pipeline. The system retrieved class hierarchy mappings and pointed out recent architectural changes merged from `dev/feature-sync`.”*
    > *“Last week, user explored architectural dependencies around the `BillingService` class after reporting inconsistent charge logic during nightly ETL jobs.”*


3. reasoning

- The `reasoning` field explains *why this specific copilot was selected* for the current query.

- It must be:
    - Grounded in the **handler's capability**
    - Justified using **query parameters** or **prior memory**
    - Framed in **clear, confident language**

- Use These Components:
    1. **Explicit handler purpose**
        Mention the handler’s declared role in the registry.
            > *"...because it expands code snippets using architectural and dependency context."*

    2. **Parameter seeds**
        Reference any identifiers or values from the query or memory.
            > *"...the query contains `stream_batch()` and class names like `DataSyncManager`, which require deep code introspection."*

    3. **Memory evidence**
        Link to conversation history (if `conversation_summary` exists).
            > *"...the user previously asked about related class hierarchies and init methods."*

- Diversification Tips for reasoning `

**1. Rotate how you enter the task:**
- "The user's request clearly mentions..."
- "Upon reading the query, it's evident that..."
- "Based on the user's input, ..."

**2. Switch the matching mechanism:**
- ".... compared the query against each handler’s description."
- ""....isolated key action verbs and aligned them with copilet  roles."
- ".... noted thematic overlap in the wording of the query and handler purpose."

-Examples
    Use diffrent phrasing patterns to justify why a specific RAG copilot or handler was selected. Each version is grammatically correct, professionally written, and avoids repetition.
        > I chose this RAG copilot because it specializes in expanding code snippets using function and class-level context, which directly aligns with the query’s focus on `SyncWorker` and `stream_batch()`. Prior conversation history also mentioned dependency lookups and init method tracing.
        > This copilot was selected for its ability to expand code by retrieving class definitions and function-level context, which matches the user’s query about `SyncWorker` and `stream_batch()`. Dependency-related topics were also discussed earlier in the thread.
        > The handler was deemed appropriate due to its alignment with both the query’s structural code components (`SyncWorker`, `stream_batch()`) and previous conversational markers involving dependency analysis and method resolution.

-Avoid Generic or Vague Phrases
    - Bad:
        > *“This handler looks relevant.”*
    - Good:
        > *“The copilot supports code understanding at the structural level, which is required to fulfill the user's request around `report_generator` module analysis.”*


---

4. chain_of_thought

Your output must be a step-by-step `chain_of_thought` — a clear, logical explanation of how the rag copilet was was chosen.

Write a detailed `chain_of_thought` that reflects the **system’s reasoning process** using only provable evidence from:
- The user’s **query**
- Any **conversation memory**
- The **registered RAG handlers** (including their name, description, and copilot ID)
- The final **confidence score** (must appear *verbatim* as it does in the data)

---

Required Reasoning Steps:

    1. **Parse the Query:**
    - Identify concrete tokens, tasks, or entities from the current user input.
    - Mention technical terms, domains, or tools .

    2. **Check Memory (if present):**
    - Look for overlap, references, or continuity from previous messages (e.g., modules, problems, business areas).
    - If memory is empty, explicitly state that only the query was used.

    3. **Match with Handlers:**
    - Compare extracted terms against all available `handler_registry`.
    - Use the **handler’s description** to argue for alignment — highlight any matching phrases or responsibilities.

    4. **Validate Contextual Match:**
    - Explicitly link **keywords in the query or memory** with **phrases in the handler’s description**.
    - Avoid general or vague links — always point to **evidence-based justification**.

    5. **Confirm Selection & Confidence:**
    - Conclude with the selected handler, the matched copilot ID, and restate the confidence score **as-is**.
    - Your final sentence must include this score exactly (e.g., "The system's confidence score of 0.73 confirms this selection.").
    - confidance level defined in the output.confidence must be taken as the confidence. do not use random guesses.

    ---

-Reasoning Styles to Rotate Across Entries

To avoid repetition across dataset rows, vary your **reasoning styles**:

    - **Deductive:** From input → conclude best match.
    - **Inductive:** From clues → infer the most likely handler.
    - **Comparative:** Weigh between multiple handlers before concluding.
    - **Context-first:** Start from prior memory, then match forward.

---

-Style & Tone Rules:

    - Use **first-person reasoning**.
    - Remain formal, technical, and explanatory.
    - Avoid vague phrases like “this seemed good” or “it fits well”.
    - Do **not hallucinate** handler capabilities or infer extra context not present in the query/memory.
    - Ensure every step is **logically connected** and based solely on the input.

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

-Example Output
Provide the final `chain_of_thought` as a list of strings (one step per item), suitable for inclusion in a JSON field.

      "chain_of_thought": [
          "The user's query asks for a comparative summary of 'data privacy regulations' for 'financial institutions' across three different countries: 'Singapore, Malaysia, and Vietnam'.",
          "The `conversation_summary` confirms the user's broader goal: a 'market-entry risk assessment', which often involves comparing regulatory landscapes. This context reinforces the need for a regulation-focused tool.",
          "I've examined the `handler_registry` and the `regulatory_compliance_search` handler is the only one available. Its description states it retrieves 'financial regulations, compliance guidelines, and legal interpretations'.",
          "Data privacy laws, especially as they apply to financial institutions, are a key component of the regulatory framework. The user's request to compare these laws across several jurisdictions is a complex task that fits the handler's domain.",
          "The handler is designed to pull this type of information, making it the only suitable option to address the user's multi-jurisdictional compliance question.",
          "The alignment between the query's focus on cross-border financial regulations and the handler's explicit purpose justifies the selection. I am choosing the `regulatory_compliance_search` handler with a confidence of 0.86."
      ]

-Common Mistakes to Avoid
    - Include **parameter seeds** from query or memory  
    - Match handler **capabilities** explicitly  
    - Use **step-wise reasoning** 
    - The `confidence` mentioned in the last step of the chain must be *identical* to the `confidence` field in the output JSON.  
    - Do **not** recalculate, round, or infer your own score.





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
| `output`       | `copilot_id`                    | **Keep original copilot ID**         |
| `output`       | `missing_fields`                | **Must not be altered and should be empty**              |
| `output`       | `optional_suggestions`          | **Do not modify or remove* and should be empty*          |
| `output`       | `suggested_payload`             | **Leave as-is and should be empty**                      |
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
