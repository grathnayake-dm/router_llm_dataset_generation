
RAG_PROMPT = """

You are a **system architect** specializing in the design of Retrieval-Augmented Generation (RAG) pipelines.

Your task is to define **modular RAG handler components** that fulfill clearly scoped and realistic roles in the following selected domain:

**`{domain}`**.

## Thought Process & Mental Model

You must follow this multi-step reasoning process to ensure each handler is grounded in real-world needs, highly specific, and structurally unique:

      1. **Understand the Given Domain**  
        Carefully analyze the domain  to understand its workflows, data sources, and operational pain points.

      2. **Identify 70 Distinct Sub-Areas or Use Cases**  
        Derive realistic retrieval scenarios that map to specific knowledge or decision-support functions. Each use case should represent a unique retrieval, augmentation, or generation challenge.
        Each handler contributes to different stages of the RAG workflow, such as:
        - Chunking
        - Embedding & Indexing
        - Filtering or Ranking
        - Context Compression or Expansion
        - Retrieval Response Validation
        - Prompt Assembly
        - User Personalization or Query Rewriting

      3. **Design Unique RAG Handlers**  
        For every use case, define a handler with:
        - A unique `name` (snake_case)
        - A concise but informative `description`

      4. **Ensure Global Uniqueness**  
        No duplicate names, payloads, or overlapping functionality. Each handler should solve a clearly distinct problem.

      5. **Validate Realism and Applicability**  
        All handlers must sound realistic and domain-grounded. Avoid generic tasks — instead, reflect real enterprise RAG needs.

      6. **Iterate and Refine Internally**  
        Think through whether your naming, configuration, and functional scope make sense before outputting the final JSON.

---

Only once this reasoning is done, output exactly 70 RAG handlers in the specified JSON structure.


## Instructions
- Generate **70** RAG modules.
- Focus on practical, well-scoped functionalities relevant to real RAG systems.
- Output a list of JSON objects. Each object must include:
  - `"name"`: A short, descriptive handler name in snake_case (must be unique and clearly reflect its purpose).
  - `"description"`: 1–2 sentences explaining what the handler does and how it contributes to the RAG process.
  - `"handler_payload"`: An object containing `"copilot_id"` as a placeholder string in UUID format (e.g., `"c9a2d84e-37ea-4117-89f0-9a488a94897c"`).

## Parameter Reference Table

| **Field**                        | **Type**       | **Description**                                                                 |
|----------------------------------|----------------|---------------------------------------------------------------------------------|
| `name`                           | string         | A unique, descriptive identifier for the RAG copilet (lowercase, underscores).   |
| `description`                    | string         | A clear summary of the RAG handler’s function and parameters, formatted as a single string. |
| `handler_payload`                | object         | Contains the `copilot_id` field.                                                |
| `handler_payload.copilot_id`     | string         | A UUID-like string for the handler payload.This ID indicates which copilot should be invoked to retrieve information from the RAG database.                                    |

## Output Format

```json
[
  
  
  {{
    "name": "<unique_rag_copilet_name>",
    "description": "<Describing the RAG  system's specific function>",
    "handler_payload": {{
      "copilot_id": "<UUID-like string>"
    }}
  }}
  
]
```


 ## Field Design Rules
  -name

 ## Field Design Rules
  -name
    -Must be written in snake_case.
    -Must reflect the copilet's function clearly and be domain-relevant.
    -Must be unique across all generated handlers.
    -Do not duplicate acroos all the rag handlers.
    -*Enforce Naming Diversity**: Avoid repetitive use of common suffixes or prefixes such as Instead, use varied, descriptive terms that capture the specific functionality . Ensure each name is contextually distinct and avoids formulaic patterns while remaining concise and precise.
    - ex: copilot_ella, fraud_pattern_analysis, nova_quize_assist
    -you must all copilot name as the suffexe or prefixes. names should be different from each other

  -description
    -Must be a single string.
    -Should describe the handler’s retrieval scope, functionality, and output.
    -Avoid vague wording. Stay precise and technical.
    -Do not duplicate acroos all the rag handlers.

  -handler_payload
    -Include a copilot_id with a valid UUID format.
    -Do not duplicate payload content across handlers unless necessary for design.


## Output Format and Quality Criteria
  -Return exactly 70 JSON objects as a well-formed JSON array.
  -Ensure no duplicates across any of the fields.
  -Each handler must represent a distinct role in a RAG pipeline within the given domain.
  -Keep the JSON strictly structured — no extra explanations or markdown in the final output.

## Example of What You’ll Get from This Prompt

Do Not Reuse or Copy
You may see examples in your system memory — do not reuse their content. Learn their structure, but create entirely new handlers based on the current domain.


```json
[
   {{
    "name": "fraud_pattern_analysis",
    "description": "Searches historical fraud patterns, risk rules, and transaction logs to identify suspicious activities and provide justification.",
    "handler_payload": {{
      "copilot_id": "a92346d4-a02a-4bbf-8a1b-ae449e8bd17a"
    }}
  }},
    {{
    "name": "quiz_question_generator_copilet",
    "description": "Generates quiz questions (multiple choice, short answer) by extracting relevant concepts and facts from course materials, tagged by difficulty.",
    "handler_payload": {{
      "copilot_id": "9017e296-ac98-4990-98ae-189419ca696f"
    }}
  }},
]


## Final Output Requirement
Your response must be a valid JSON array of 70 handler objects tailored to the given domain.
No extra formatting, no markdown — just clean JSON.

---

"""
