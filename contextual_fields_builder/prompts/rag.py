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
    -STAGE 1 — Generate Content: Based on the INPUT_JSON, generate 6 unique and dynamic data entries. Each entry will contain a user query, the reasoning for the routing decision, and a detailed chain-of-thought.
    -STAGE 2 — Update and Finalize JSON: For each of the 6 generated entries, create a deep copy of the original INPUT_JSON and inject the generated content into the appropriate fields.

### STAGE 1
You will be given  a SAMPLE INPUT JSONL as follows:
{"input":{"id":"4293fa4f-9099-4a5e-b645-b70c68863b0e","timestamp":"2025-03-23T12:16:35.085127","query":"","conversation_summary":"","handler_registry":{"mcp_tools":[],"worker_agents":[],"llm_handlers":[],"rag_handlers":[{"name":"lecture_summary_generator","description":"Summarizes lengthy lectures, academic articles, or chapters into concise/bullet points or brief paragraphs for quick review.","handler_payload":{"copilot_id":"931abcf2-5f1f-4a8a-9f63-e335467f1209"}}],"compiled_at":"2025-03-21T15:50:51.085127","user_id":"c473d21c-901b-431e-a758-62c82e4e70ab","workspace_id":"234e8b34-2bd8-4c41-a6e1-e26981867fb7"},"copilot_id":null,"thread_id":"64bbf60c-107e-45b4-abba-dba14ccf1dec"},"output":{"select_handler_type":"rag","handler_name":"lecture_summary_generator","server_name":null,"tool_name":null,"copilot_id":"931abcf2-5f1f-4a8a-9f63-e335467f1209","missing_fields":[],"optional_suggestions":[],"suggested_payload":{},"confidence":0.67089,"reasoning":"","chain_of_thought":[],"workspace_preference_override":false}}

containing a `handler_registry` with its metadata. Your task is to **simulate realistic usage scenarios** by filling ONLY the following empty fields in the corresponding JSON block
- `query`: A natural language question that a user would ask related to this registry's  rag copilet capabilities.
- `conversation_summary`: A realistic prior user interaction summarizing what has been discussed before (e.g., exploration, debugging context, or code-related discussion).
- `reasoning`: A short justification for why the selected handler (e.g., `code_context_expander`) is suitable for the given query.
- `chain_of_thought`: A step-by-step decision trace explaining why this handler was selected over others, referencing the query, possible memory state, copilot goals, and evidence from the handler's capabilities.


- Generate **6 dynamic and diverse** outputs based on the `INPUT_JSON` content.
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
        "reasoning": "The user is requesting a comparative summary of financial regulations across multiple jurisdictions. The regulatory_compliance_search copilte handler was selected as it aligns with the user’s intent and its core capabilities, being purpose-built to retrieve and interpret financial regulations and compliance guidelines.",
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
- This yields 6 updated INPUT_JSON objects, each representing one enriched and realistic scenario.
- All the  other fields in the original INPUT_JSON remain unchanged .
-The final output should be a list of 6 modified JSON objects, each being a fully updated copy of the original INPUT_JSON,  with the following updated values  in its input and  output fields replaced using the generated schema fields.
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
      "reasoning": "The user is requesting a comparative summary of financial regulations across multiple jurisdictions. The regulatory_compliance_search handler was selected as it aligns with the user’s intent and its core capabilities, being purpose-built to retrieve and interpret financial regulations and compliance guidelines.",
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
        - Vary Phrasing: For the 6 scenarios, create different types of queries:
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
            - Read the handler_registry entry carefully .
            - Identify realistic enterprise workflows or interactions that could lead to the current query.
            - Use Domain-Relevant Scenarios . Build summaries around authentic user behavior.

        - Ground the Narrative with Specific Identifiers (MANDATORY):
            - To simulate a real memory, you MUST include specific, non-generic identifiers.
                - Good: Ticket IDs (INC-9812), Change Requests (CR-8802), Project Codenames (Project Apollo), File Versions (release-v2.9.3), Hostnames (prod-reporting-db-replica), or specific company/person names.
                - Bad: "the server," "a file," "the ticket."
    
        - Simulate a Chronological Memory Trail
            - Every conversation_summary MUST be a short story of 5-8 lines that follows a clear narrative arc. Do not just list facts; connect them into a logical sequenc
                - Detail the Intermediate Steps (The "How they got here"):
                - Describe distinct, logical actions the user took before the current query.            
                - Show a progression of thought. Did they start broad and then narrow down? Did they try one thing that didn't work, leading to the next step?
                    - Example: " User initially explored server performance degradation across prod-reporting-db-replica and cache-node-17. After correlating system metrics with incident timelines, they isolated three critical events linked to spike periods. Subsequently, user pulled related Jira tickets (INC-9812, INC-9820, CR-8802) to trace root causes and validate mitigation actions. With most metrics reconciled, user checked consolidated SLA breach summary focusing on escalations during the July 28–August 4 window for QA-11, DEV-02, and PROD-44."

        - Add Rich Context + Prior Contacts
            -To simulate memory continuity and enterprise-level realism, your conversation_summary must include detailed, plausible background actions that led to the current query. 
                - Broader initiatives
                - Realistic — infer probable past steps from current query
                    - Example : "infrastructure upgrade for internal knowledge assistants, the user initially benchmarked EmbedderV3 performance on curated document sets tied to the HR and Legal domains. Most recently, user asked to refine reranker thresholds and inspect scoring metrics tied to the copilot_id: org_compliance_bot."

-You can implement conversation_summary in two ways:
    -As a list of multiple summary strings, like this:
        conversation_summary = "User evaluated document retrieval performance of the `ContractReviewCopilot` after reports of missing results in legal query flows. They tested retrieval against a curated contract dataset and flagged inconsistencies tied to outdated index versions."
    -Sometimes this summary may be empty. if you chose this way make sur to add all the necessary content with in query.
        conversation_summary = ""

-Example: Good vs. Bad Summaries
This illustrates the level of detail required.
    - BAD (Vague, Generic, or Including Present Request):
        - "User was looking at financial data. They previously viewed 'Annual Financial Household Report 2025' report."
            - (Why it’s bad: No specific goal, no identifiers, no story, no human context.)
        - "User is now asking to extract a specific financial metric from a given chart." 
             -(Why it’s bad: This includes the user’s current request, which should never appear in the conversation summary — the summary must only reflect previous interactions.)

    -GOOD (Detailed, Narrative-Driven, and Specific):
        - "User started the Q3 competitive analysis of Apex Innovations by reviewing public stock trends. They summarized key analyst reports highlighting strong growth in Cloud Services. To verify this, user requested the official Q3 earnings report but was only able to locate a low-quality scanned PDF of the earnings slides."     

- for each sample use different diverse conversation memory implementations.
- Note: The examples in this section are provided for guidance only. Do not replicate them in the exact same format — instead, use them as inspiration to create varied and diverse sentence structures. The goal is to produce new, original phrasing for each data point rather than repeating the examples verbatim.

3. reasoning

- The `reasoning` field explains *why this specific copilot was selected* for the current query.

- It must be:
    - Grounded in the **handler's capability**
    - Justified using **query parameters** or **prior memory**
    - Framed in **clear, confident language**

- CRITICAL GUIDELINES: The Three-Part Justification.
    I. Every reasoning statement must be a compelling argument (2-3 sentences) built on the following three components:
    - Isolate the Core Task Requirement (The "Why it's a special case"):
        Start by identifying the single most important requirement of the user's query that makes it unique.
            - "The user's request hinges on executing a complex, structured data query with three distinct filter categories..."
            - "This query's primary challenge is the need to understand deep architectural context within a codebase..."
    II. Justify the Selection and Contrast with Alternatives (The "Why it's the only choice"):
            - Explain how the chosen handler is uniquely engineered to meet this core requirement, which implicitly or explicitly disqualifies other, more generic handlers.
        -Use comparative language (): "uniquely equipped," "the only handler specialized for," "unlike standard text models," "fundamentally beyond the scope of general-purpose handlers."
            - "...This need for database access disqualifies standard text-generation models, making sentinel_survey_data_retriever the only viable handler."
            - "...This makes the code_expander_copilot the definitive choice, as generic LLMs lack the necessary dependency-graph awareness."
    III. Provide Concrete Evidence from the Query and Memory (The "Here's the proof"):
            - Ground your justification by citing specific "parameter seeds" or keywords from the query and conversation_summary. This proves your decision is data-driven.
            - Query Evidence: Reference specific identifiers, function names, or values.
                "...as evidenced by the mention of SyncWorker in the query."
            - Memory Evidence: Link to the user's prior actions if a summary exists.
                "...which builds upon the user's prior exploration of class hierarchies and dependency tracing."

- Varying Phrasing and Style (Avoid Repetition)
- While the logic must be consistent, the phrasing must be diverse. Do not use the same sentence structure repeatedly.
    - Rotate how you introduce the task:
        "The user's request clearly hinges on..."
        "Upon analyzing the query, it's evident that the core task is..."
        "Based on the user's input and conversation history, the primary need is..."
    - Switch up the matching mechanism:
        - "...I compared this requirement against each handler’s description and found only one match."
        - "...This specialized need allowed me to disqualify generic handlers and isolate the correct tool."
        - "...There is a clear thematic overlap between the query's terminology and the chosen handler's purpose, which is absent in other handlers."

Example Re-phrasings for the Same Logic:
    Version 1: The query's requirement for precise, multi-filter data retrieval from a specific health dataset disqualifies general-purpose LLMs, which cannot access structured databases. The sentinel_survey_data_retriever is explicitly designed for this function, making it the only viable handler to fulfill the request.
    Version 2: This copilot was selected for its ability to expand code by retrieving class definitions and function-level context, which matches the user’s query about SyncWorker and stream_batch(). Dependency-related topics were also discussed earlier in the thread.
    Version 3: "The user's request hinges on executing a complex, structured data query with three distinct filter categories. This task requires direct, secure access to a specific dataset and is fundamentally beyond the scope of any general-purpose text or summarization handler in the registry. The sentinel_survey_data_retriever is the sole agent engineered for this precise data extraction task, making its selection definitive.

- Note: The examples in this section are provided for guidance only. Do not replicate them in the exact same format — instead, use them as inspiration to create varied and diverse sentence structures. The goal is to produce new, original phrasing for each data point rather than repeating the examples verbatim.
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
    - **Context-first:** Start from prior memory, then match forward.---

-Style & Tone Rules:

    - Use **first-person reasoning**.
    - Remain formal, technical, and explanatory.
    - Avoid vague phrases like “this seemed good” or “it fits well”.
    - Do **not hallucinate** handler capabilities or infer extra context not present in the query/memory.
    - Ensure every step is **logically connected** and based solely on the input.
    
Diversification Tips for chain_of_thought`

**1. Rotate how you enter the task:**
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
          "The user asks for a comparative summary of 'data privacy regulations' for 'financial institutions' across three different countries: 'Singapore, Malaysia, and Vietnam'.",
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
    - **Do not** include the user query or conversation summary as a quoted block in the conclusion.

- Note: The examples in this section are provided for guidance only. Do not replicate them in the exact same format — instead, use them as inspiration to create varied and diverse sentence structures. The goal is to produce new, original phrasing for each data point rather than repeating the examples verbatim.
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
    - Note: The example prompts in each section are provided for guidance only. Do not replicate them in the exact same format — instead, use them as inspiration to create varied and diverse sentence structures. The goal is to produce new, original phrasing for each data point rather than repeating the examples verbatim.
    - IMPORTANT: Outside of the fields listed above, no other parts of the original input or output JSON should be altered. 
    - This ensures structural consistency and compatibility with downstream pipelines. The format, nesting, and extra fields must remain exactly as in the original INPUT_JSON.
    - In Stage 1, generate an array of 6 distinct JSON items—each containing a unique combination of the required output fields. 
    - Then, in Stage 2, iterate over these 6 items to replace the corresponding fields in the input JSON schema, producing a final output array of 6 fully merged JSON objects reflecting the updated input and output sections. 
    - Return final stage 2 output as following list of array
        - [stage2_item1, stage2_iitem2, stage2_iitem3,.... stage2_iitem6].

- This marks the end of the prompt, and the final response should return this array of 6 complete JSON items."
"""
