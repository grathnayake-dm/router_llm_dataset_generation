BASE_LLM_PROMPT="""

This process is designed to generate a training dataset for responsible for routing user queries to the appropriate llm in an enterprise system.
You are simulating a Router LLM that receives user input and determines the most suitableBase LLM to invoke based on a registry of handlers. This dataset captures realistic  decision patterns for use in downstream LLM-based orchestration systems.
Key Concepts

1. LLM Handlers
  -Each LLM handler entry in the handler_registry represents a large language model with specific capabilities and metadata. Fields typically include:
  -name: Unique identifier for the handler.
  -description: Functional focus of the handler (e.g., financial extraction, image understanding).
  -model_provider: Company or source (e.g., OpenAI, Alibaba).
  -model_name: The specific LLM version or architecture.
  -is_workspace_default: Boolean flag indicating whether this LLM is the default, locally hosted workspace LLM.
    -Example of llm handler registry
    {
      "name": "operational_dashboard_creator",   "description": "Creates custom operational dashboards with real-time data visualization based on text-based performance metrics.",   "model_provider": "Meta",   "model_name": "Llama 3.2 Instruct 90B",   "is_workspace_default": false
    },
   -handler_registry": {"mcp_tools": [], "worker_agents": [], "llm_handlers": [{"name": "python_boilerplate_generator", "description": "Generates common Python boilerplate code for various applications and frameworks.", "model_provider": "Mistral", "model_name": "Codestral", "is_workspace_default": false}]

2. Base LLM
    -These are general-purpose models provided by third-party vendors (e.g., OpenAI, Anthropic, Alibaba).
    -They are not hosted within the user’s enterprise environment.
    -They are used when the query does not require internal data or workspace-specific restrictions.
    -is_workspace_default is set to false.

3. Workspace-Local LLM (Workspace LLM)
    -These models are deployed within the user's enterprise workspace.
    -Often optimized for internal data, private reasoning tasks, or domain-specific operations.
    -Queries that mention things like "search this on our internal LLM", "use the workspace model", or "run this securely in-house" should be routed to this handler.
    -is_workspace_default is set to true.

For each training sample, we simulate how a Router LLM would behave by starting from the available LLM handler(s) in the handler_registry and generating a realistic user interaction that would lead to selecting that handler.
The steps are:
Start from a given LLM handler  in the handler_registry.
  Extract its:
    -name
    -description
    -model_provider
    -model_name
    -is_workspace_default flag
-Based on the handler’s description and capabilities, generate:
  -A natural-sounding user query that would require this handler.
    -Inject workspace-awareness in the query if is_workspace_default = true:
    -Use phrases like "use our workspace LLM", "run this inside our internal system", or "analyze using in-house model".
    -If false, make it a general query without workspace references.
  -A conversation_summary simulating context from previous turns.

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

{"input":{"id":"e963d0cc-f687-4f4a-93d2-dd5cff7061b3","timestamp":"2025-06-11T06:50:27.092867","query":"","conversation_summary":"","handler_registry":{"mcp_tools":[],"worker_agents":[],"llm_handlers":[{"name":"financial_report_image_parser","description":"Extracts key financial data and tables from scanned annual reports and earnings slides, converting them into structured text for analysis.","model_provider":"Alibaba","model_name":"Qwen 2.5-VL","is_workspace_default":false}],"rag_handlers":[],"compiled_at":"2025-06-09T22:15:32.092867","user_id":"f299ec2e-0148-45a1-8836-d9c1809d747c","workspace_id":"2fb629c6-8dbb-4eec-b8c8-590e19ba20fc"},"copilot_id":null,"thread_id":"124ea2eb-db4c-4560-be89-7472d53f84b9"},"output":{"select_handler_type":"base_llm","handler_name":"financial_report_image_parser","server_name":null,"tool_name":null,"copilot_id":null,"missing_fields":[],"optional_suggestions":[],"suggested_payload":{},"confidence":0.877404,"reasoning":"","chain_of_thought":[],"workspace_preference_override":false}}

-For each INPUT_JSON, generate four diverse output samples simulating how a user might trigger the selected handler. Each sample must include the following fields:
  -Required Fields per Sample:
    -query: A natural-sounding user query that would appropriately invoke the selected handler. This may contain implicit or explicit references to required schema parameters.
    -conversation_summary: A realistic detailed summary of prior conversation context, helping justify parameter grounding or task continuity.
    -suggested_payload: The generated query above should be appended as a key–value pair.
    -reasoning: A concise justification explaining why the selected handler is the most appropriate match for the query.
    -chain_of_thought (CoT): A step-by-step explanation of how the Router LLM analyzed the query, considered handler capabilities, and validated parameter readiness.
  -Each of the 4 samples should simulate a distinct and realistic user scenario, varying in phrasing, specificity  to ensure dataset diversity.

Output Schema STAGE 1(Per Generated Entry):

{
  "query": "<string>",                     // Natural-language user request
  "conversation_summary": "<string>",     // Prior context simulating memory
  "suggested_payload" : <key, value>      // above generated query above should be appended 
  "reasoning": "<string>",                // Justification for handler selection
  "chain_of_thought": [                   // Multi-step reasoning process
    "<step 1>",
    "<step 2>",
    "...",
    "<final handler selection conclusion>"
  ]
}

Each generated data point must strictly adhere to the schema below. This ensures consistent formatting and supports downstream model training and evaluation.
Example Output Entry (1 of 4):

{
  "query": "I’m starting a new Django project for an e-commerce platform. Can you generate the initial Python boilerplate with models and views?",
  "conversation_summary": "The user mentioned planning an e-commerce project and asked about Django setup best practices earlier. They now want a complete boilerplate to kickstart development.",
  "suggested_payload" : {
    "query": "I’m starting a new Django project for an e-commerce platform. Can you generate the initial Python boilerplate with models and views?",
  }
  "Reasoning": "The request for a Django project boilerplate with models and views for an e-commerce platform directly matches the python_boilerplate_generator’s ability to generate Python code for web frameworks like Django. This handler is well-equipped to provide the structured code needed for this task.",
  "chain_of_thought": [
    "I examined the user’s query, which requests a Python boilerplate for a Django project with models and views for an e-commerce platform.",
    "I searched the LLM handler registry for handlers capable of generating Python code for web frameworks like Django.",
    "The python_boilerplate_generator is designed to create boilerplate code for various applications, including Django-based web projects.",
    "The query specifies ‘Django,’ ‘models,’ ‘views,’ and ‘e-commerce,’ providing clear evidence of the need for web app code generation.",
    "The handler’s is_workspace_default flag is false, which aligns with the query’s general-purpose nature.",
    "Mistral’s Codestral model is optimized for generating framework-s  -A natural-sounding user query that would require this handler.]

  -A conversation_summary simulating context from previous turns.
    -Inject workspace-awareness in the query if is_workspace_default = true:
    -Use phrases like "use our workspace LLM", "run this inside our internal system", or "analyze using in-house model".
    -If false, make it a general query without workspace references.pecific Python code, making it suitable for this task.",
    "The strong alignment between the query and handler capabilities supports a confident selection (confidence score: 0.625944).",
    "I confirm that python_boilerplate_generator is the correct handler for this query and is ready to be invoked."
  ]
}
  -Use following variations for generation:
  -With different company names, financial metrics (e.g., EBITDA, gross margin), or timeframes (e.g., annual vs quarterly).
  -Vary phrasing, memory context, and reasoning styles.

 
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
        - output.suggested_payload ->  from genrated suggested_payload
        - output.reasoning → from generated reasoning
        - output.chain_of_thought → from generated chain_of_thought
- This yields 4 updated INPUT_JSON objects, each representing one enriched and realistic scenario.
- All the  other fields in the original INPUT_JSON remain unchanged .
-The final output should be a list of 4 modified JSON objects, each being a fully updated copy of the original INPUT_JSON,  with the following updated values  in its input and  output fields replaced using the generated schema fields.

  {
    "input": {
      "query": "<replaced with Stage 1 → query>",
      "conversation_summary": "<replaced with Stage 1 → conversation_summary>",
      "other_fields_preserved": "..."
    },
    "output": {
      "suggested_payload" : "<replaced with Stage 1 → suggested_payload>",,
      "reasoning": "<replaced with Stage 1 → reasoning>",
      "chain_of_thought": [
        "<CoT step 1>",
        "<CoT step 2>",
        "...",
        "<final conclusion>"
      ],
      "other_fields_preserved": "..."
    }
  },
  ...

Final Output Format (After Stage 2)

  {
    "input": {
      "id": "e57147b5-428c-4221-80e9-741641e142fc",
      "timestamp": "2025-06-08T07:51:08.416580",
      "query": "I’m starting a new Django project for an e-commerce platform. Can you generate the initial Python boilerplate with models and views?",
    "conversation_summary": "The user is in the early stages of developing an e-commerce platform using Django. In previous sessions, they explored Django project structuring best practices, specifically modular app separation and reusable components. They reviewed DRY principles and asked whether to scaffold reusable components such as `user_profile`, `product_catalog`, and `order_tracking`. Earlier, they examined trade-offs between using `GenericViewSet` and function-based views for rapid prototyping. They also discussed integration options with `django-rest-framework` and explored boilerplate generation strategies for API-first development."
      "handler_registry": {
        "mcp_tools": [],
        "worker_agents": [],
        "llm_handlers": [
          {
            "name": "python_boilerplate_generator",
            "description": "Generates common Python boilerplate code for various applications and frameworks.",
            "model_provider": "Mistral",
            "model_name": "Codestral",
            "is_workspace_default": false
          }
        ],
        "rag_handlers": [],
        "compiled_at": "2025-06-07T23:55:53.416580",
        "user_id": "9cf41cb2-6ec7-471e-85e8-f8a582bea350",
        "workspace_id": "e2aa118a-014b-429c-9c9e-9da5fc9c91b3"
      },
      "copilot_id": null,
      "thread_id": "2a219814-07e3-4c4c-8c02-a5e9b9676b67"
    },
    "output": {
      "select_handler_type": "base_llm",
      "handler_name": "python_boilerplate_generator",
      "server_name": null,
      "tool_name": null,
      "copilot_id": null,
      "missing_fields": [],
      "optional_suggestions": [],
      "suggested_payload": {
        "query": "I’m starting a new Django project for an e-commerce platform. Can you generate the initial Python boilerplate with models and views?",
      },
      "confidence": 0.625944,
      "reasoning": "The request for a Django project boilerplate with models and views for an e-commerce platform directly matches the python_boilerplate_generator’s ability to generate Python code for web frameworks like Django. This handler is well-equipped to provide the structured code needed for this task.",
      "chain_of_thought": [
        "I examined the user’s query, which requests a Python boilerplate for a Django project with models and views for an e-commerce platform.",
        "I searched the LLM handler registry for handlers capable of generating Python code for web frameworks like Django.",
        "The python_boilerplate_generator is designed to create boilerplate code for various applications, including Django-based web projects.",
        "The query specifies ‘Django,’ ‘models,’ ‘views,’ and ‘e-commerce,’ providing clear evidence of the need for web app code generation.",
        "The handler’s is_workspace_default flag is false, which aligns with the query’s general-purpose nature.",
        "Mistral’s Codestral model is optimized for generating framework-specific Python code, making it suitable for this task.",
        "The strong alignment between the query and handler capabilities supports a confident selection of 0.625944.",
        "I confirm that python_boilerplate_generator is the correct handler for this query and is ready to be invoked."
      ],
      "workspace_preference_override": false
    }
  }
]
final output must strictly preserve the structure of the original INPUT_JSON schema. Only the specified fields should be updated with values from Stage 2, while all other keys and nesting should remain exactly the same to ensure structural consistency.

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

## Key Decision Rule: Check is_workspace_default
- Inspect the handler's is_workspace_default flag:
    If true:
      This means the model is a Workspace-Local LLM, hosted internally in the user’s environment.
    If false:
      This is a General-Purpose External LLM, suitable for public or vendor-hosted tasks.

- Query Design Guidelines Based on is_workspace_default
  | Handler Type | `is_workspace_default` | Query Requirements |
  | ------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | Workspace LLM | `true` | The query **must include language implying internal system access**, e.g.:<br>• "Use the workspace LLM to..."<br>• "Search in our internal/private models"<br>• "Run this securely using our in-house LLM" |
  | General-purpose LLM | `false` | The query should **sound generic**, with **no reference to internal systems**, e.g.:<br>• "Can you summarize..."<br>• "Extract this data using Alibaba's Qwen..."<br>• "What’s the answer to..." |


## Schema Generation Instructions
-You have to follow guidance during the following field creating process

1. query → Human-Readable User Request
-Role: End-User Simulation
-The query field must simulate how a real user would naturally ask the system to perform a task — using clear, human-like language that reflects their intent, not internal system mechanics.
-Purpose: -The query helps the Router LLM decide, Which handler or agent is appropriate for the request.

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
  - Use the handler description to guide what the query is trying to achieve.
  - Use the input_schema to inform your phrasing — never expose raw schema terms in the query.
  - Make sure the query sounds contextual, not like a prompt for a tool or test system.
  - If is_workspace_default = true, the query must mention internal use, like:
      "Use the workspace model to..."
      "Run this through our internal system..."
      "Search using our in-house LLM..."



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
                    - Example : "As part of an ongoing  infrastructure upgrade for internal knowledge assistants, the user initially benchmarked EmbedderV3 performance on curated document sets tied to the HR and Legal domains. Most recently, they asked to refine reranker thresholds and inspect scoring metrics tied to the copilot_id: org_compliance_bot."
-You can implement conversation_summary in two ways:
    -As a list of multiple summary strings, like this:
        conversation_summary = "Last week, user explored architectural dependencies around the `BillingService` class after reporting inconsistent charge logic during nightly ETL jobs."
    -Sometimes this summary may be empty. if you chose this way make sur to add all the necessary content with in query.
        conversation_summary = ""

-Example for Converstion memory
    > *user previously explored how the `DataSyncManager` interacts with `SyncWorker` during job execution. After retrieving class definitions and init methods, user asked for related design notes tied to the `stream_batch()` pipeline. The system retrieved class hierarchy mappings and pointed out recent architectural changes merged from `dev/feature-sync`.”*
    > *“Last week, user explored architectural dependencies around the `BillingService` class after reporting inconsistent charge logic during nightly ETL jobs.”*

3. Reasoning
  -Reasoning Instructions for LLM Handler Selection
  -You are a router assistant tasked with selecting the most appropriate LLM Handler based on a user query.
  -Carefully read and interpret the user’s query and conversation memroy to understand the underlying intent.
  -Identify which LLM Handler best matches the task domain or function described in the handler registry.
  -Check the handler's is_workspace_default flag:
      -If true, the handler is a workspace-local LLM intended for secure or internal usage.
      -If false, it is a general-purpose external LLM.
  -Clearly and concisely explain (in 2 to 3 sentences) why the selected LLM Handler is the best fit for fulfilling the user’s request.
  -If the handler is workspace-local (is_workspace_default = true), mention that the request will be handled by the default workspace LLM or an internal model to reflect privacy or internal system preference.
  -Focus on how the handler’s purpose, capabilities, and workspace preference align with the user’s needs.
  -Use a natural and professional tone, avoiding technical jargon, system calls, or internal routing details.
  -Discuss only the handler’s role, relevance, and workspace preference if applicable.

-Example
  User Query:
  "Can you extract key financial figures such as revenue and net profit from the scanned Q2 2024 earnings slide?"
  Reasoning:
  The user’s query requests extraction of financial metrics from a scanned document, which aligns closely with the capabilities of the financial_report_image_parser LLM . This handler specializes in processing scanned financial reports and converting visual data into structured text, making it the ideal choice to fulfill this request..

-Example (Workspace-Local Handler)
  User Query:
  "Please analyze the internal employee skill assessment data securely using our in-house model."
  Reasoning:
  The user requests analysis of employee skill assessments through an internal and secure process, which matches the workspace-local LLM handler designed for private organizational data. This default workspace LLM ensures data privacy while providing accurate skill analysis, making it the best handler for this request.

4 Chain of Thought
-Each chain_of_thought must simulate how a Router LLM arrives at its decision in real time, using first-person, self-reflective language (e.g., “I reviewed…”, “I identified…”).
-Write a detailed `chain_of_thought` that reflects the **system’s reasoning process** using only provable evidence from:
  - The user’s **query**
  - Any **conversation memory**
  - The **registered RAG handlers** (including their name, description, and copilot ID)
  - The final **confidence score** (must appear *verbatim* as it does in the data)

-Use 8 logically connected steps per entry.
-Each step should be logically proven and should be a step by step process.

🪜 Step-by-Step Breakdown
  -Intent Recognition
    -Start by analyzing the user’s query and determining what they’re trying to achieve or inquire about.
    -Example:
    -“I reviewed the user’s query requesting extraction of revenue and net profit from a scanned earnings report.”

  -Search the LLM Handler Registry
    -Review the available  handlers in the registry. Identify one that could fulfill the task described in the query.
    -Example:
    -“I examined the list of handlers define in the handler registry and found one capable of extracting structured data from scanned financial documents.”

  -Initial Match Justification
    -Justify why a particular handler seems relevant. Reference the handler name and paraphrase its description.
    -Example:
    -“The  financial_report_image_parser llm is specifically designed to extract financial data from scanned earnings reports, which aligns directly with the user’s request.”

  **Validate Contextual Match:**
    - Explicitly link **keywords in the query or memory** with **phrases in the handler’s description**.
    - Avoid general or vague links — always point to **evidence-based justification**.
   -Example:
    -“The mention of 'Q2 2024 earnings slide' and request for 'revenue and net profit' indicates the need for structured data extraction from visual financial content.”
  
  -Check Workspace Preference (if applicable)
    -Inspect the is_workspace_default flag:
      -If true: Confirm that the query is aligned with internal/private model expectations.
      -If false: Confirm the query does not require internal system execution.
    -Example:
    -“This llm is not marked as a workspace default, which is appropriate since the user did not specify any internal or private system preference.”

-**Confirm Selection & Confidence:**
    - Conclude with the selected handler, the matched copilot ID, and restate the confidence score **as-is**.
    - Your final sentence must include this score exactly  as defined in the input json(e.g., "The system's confidence score of 0.73 confirms this selection.").
    -“Given the precise match between the task and the handler’s description ->  I am 87%  highly confident in this selection ”
    - confidance level defined in the output.confidence must be taken as the confidence. do not use random guesses.

  -Final Decision Statement
    -Conclude your decision clearly and assertively. Confirm selected name name and readiness.
    -Example:
    “I confirm that financial_report_image_parser is the correct LLM  for this query and is ready to be invoked.”

-Style & Tone Guidelines
    - Always use first-person voice (“I assessed...”, “I determined...”) to simulate internal reasoning.
    -Keep explanations formal and evidence-backed.
    -Avoid repetition — even across different samples.
    -Don’t mention technical terms like “schema,” “registry field,” or “endpoint.”
    - Respect workspace context: only refer to internal/private models when is_workspace_default = true.

Example — Workspace-Local Handler

User Query:
 "Can you use our internal model to analyze this PDF of Q2 employee performance data and extract key leadership metrics?"

Chain of Thought:
I reviewed the user’s query, which requests an internal analysis of Q2 employee performance using a company model.
I searched the handler registry for tools capable of analyzing documents for performance insights.
I identified workspace_performance_pdf_analyzer as the most appropriate llm, based on its ability to extract leadership metrics from internal HR PDFs.
The phrase "our internal model" and mention of a Q2 performance PDF provide clear evidence of the intended task.
This llm is marked as a workspace default, which aligns with the user’s preference for internal/private processing.
The query provides enough detail to proceed, including both the document type and target metric.
I am 95% confident in this selection, given the domain alignment and explicit mention of internal processing.
I confirm the selection of workspace_performance_pdf_analyzer as the correct LLM and it is ready for execution.

-----
5. Suggested payload
- The generated query should be appended within the suggested_payload field as shown below:
  "suggested_payload": {
    "query": "Here's a screenshot of a slide from Quantum Dynamics' Q3 earnings call. Please pull the full table of operating expenses and calculate the year-over-year change."
    },


## Diverse User Queries + Conversation Memory
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
| `output`       | `copilot_id`                    | **Keep original copilot ID**         |
| `output`       | `missing_fields`                | **Must not be altered and should be empty**              |
| `output`       | `optional_suggestions`          | **Do not modify or remove* and should be empty*          |
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

