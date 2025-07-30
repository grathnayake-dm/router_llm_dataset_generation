LLM_PROMPT = """

You are a system designer specializing in building structured catalogs of LLM-powered tools.

Your task is to generate a JSON catalog with 50 jsons of llm for LLM-based systems, specifically designed for ** text, image, video, or audio** use cases **within specifically tailored to:

---

## Domain:
"{domain}"

## Model List:
{model_list}

Each model has specific capabilities (text, audio, image, video). Match the use case to an appropriate model that supports the needed modalities.

---

## Thought Process & Mental Model

You must follow this multi-step reasoning process to ensure each catalog is grounded in real-world needs, highly specific, and structurally unique:

1. **Understand the Given Domain**  
   Carefully analyze the domain to understand its workflows, data sources, and operational pain points, focusing on how LLMs can support organizational tasks.

2. **Identify  Distinct Sub-Areas or Use Cases**  
   Derive realistic scenarios that map to specific knowledge, decision-support, or generation functions within the domain. Each use case should represent a unique LLM challenge
   
3. **Design Unique LLM catalog**  
   Get the model details from the provided model list, define a catalog entry with:
 
4. **Ensure Global Uniqueness**  
   No duplicate names, descriptions, or overlapping functionality. Each llm tool should solve a clearly distinct problem and reflect the organization/workspace context.

5. **Validate Realism and Applicability**  
   All llms must be realistic and domain-grounded, tailored to enterprise or organizational needs in the specified domain. Avoid generic tasks — reflect real-world LLM use cases.

6. **Iterate and Refine Internally**  
   Think through whether your naming, configuration, and functional scope make sense before outputting the final JSON.

---


## Understanding `is_workspace_default`

The `is_workspace_default` field determines whether an LLM tool is the **default model setup for a specific organization’s workspace**.

### Possible Values
- **`true`**  
  -  an enterprise-level environment or organizational workspace in which large language models (LLMs) are deployed as default assistants, internal tools, or workflow automators, are tightly integrated with the organization's operations and are tailored to the needs, structure, and identity of that organization.
  - The `name` must include a **workspace or organization identifier** (e.g., `policy_bot_kaiser`, `legal_qa_deloitte`).
  - Reflects **ownership**, **deployment context**, and **workspace usage**.

- **`false`**  
  - Indicates that the llm  is **not tied to a specific organization**.
  - These are **general-purpose**, standalone tools that can be used across domains.

---
### Distribution Rule

You must generate:
- **75%** llms with `"is_workspace_default": false`  
  ➤ Generic tools, neutral names, broad applicability.

- **25%** llms with `"is_workspace_default": true`  
  ➤ Workspace-specific tools, with names that reflect the **organization or ecosystem identity**.

This ensures a balanced and traceable catalog of both general and specialized LLM systems.

---

### Model Selection Rules

You are given a list of available LLM models under **Model List**. These models may vary across runs and are not fixed.

For each JSON catalog generation:
- **Dynamically analyze the models** provided and choose exactly best match the needs of the domain and sub-use-cases.
- The selection must be based on the **input/output modalities** and the **functional diversity** needed within the domain 
- Ensure **diversity across multiple catalogs** — avoid repeating the same  models for every catalog run.


## Instructions
- Generate **5** LLM tools.
- Focus on practical, well-scoped functionalities relevant to real LLM systems in the given domain.
- Output a list of JSON objects. Each object must include:
  - `"name"`: A short, descriptive  name in snake_case, reflecting  its purpose.
  - `"description"`: 1–2 sentences explaining what the llm tool does and how it contributes to the organization's workflow.
  - `"model_provider"`: The LLM provider (e.g., OpenAI, Google, Anthropic, Alibaba).
  - `"model_name"`: The specific model name (e.g., GPT-4o, Gemini 2.5 Pro, Claude 3.5 Sonnet, Qwen-Max).
  - `"is_workspace_default"`: A boolean indicating if the llm is the default for the workspace.

## Parameter Reference Table

| **Field**              | **Type**   | **Description**                                                                 |
|------------------------|------------|---------------------------------------------------------------------------------|
| name                   | string | A creative, functional identifier in snake_case, combining the LLM model name with a branded or purpose-driven suffix. Avoid generic templates; enforce naming diversity and personality. Examples: gemini_scopebot, claude_thought_mapper, mistral_narrative_scribe, gpt_insight_hub. || `description`          | string     | A clear summary of the llm's function and output, formatted as a single string. |
| `model_provider`       | string     | The provider of the LLM (e.g., OpenAI, Google, Anthropic, Alibaba).              |
| `model_name`           | string     | The specific model used (e.g., gemini-2.5-pro).       |
| `is_workspace_default` | boolean    | Indicates if the llm is the default model setup for the organization’s workspace. |


## Output Format

```json
[
  {{
    "name": "<unique_llm_tool_name>",
    "description": "<Describing the LLM tool's specific function>",
    "model_provider": "<LLM provider>",
    "model_name": "<Specific model name>",
    "is_workspace_default": <true or false>
  }}
]


## Field Design Rules
- **name**
  - Must combine the LLM model name (e.g., gemini, claude, gpt, etc.) with a creative and/or functional suffix.
  - The name should be in snake_case, concise, unique, and expressive.
  - Blend task + creativity + model awareness — avoid overly formulaic names
  - Must reflect the functionality of the llm  .
  - Must be unique across all generated tools.
  - example:  gemini_docs_reader, code_complexity_analyzer, elitehr_employee_benefit_infographic_gen
      -If `is_workspace_default = false` (Generic/Public LLM)
        - Must combine the LLM model name (e.g., gemini, claude, gpt, mistral) with a creative and/or functional suffix.
        - Name should evoke the LLM’s role or character while staying general-purpose.
        - Examples:
          - `claude_oracle`
          - `gemini_insight_forge`
          - `codecraft_gpt`
          - `mistral_quickscribe`

      - If `is_workspace_default = true` (Company/Workspace-specific LLM)
        - Must begin/ end with a **workspace, product, or ecosystem name** (e.g., elitehr, acme, visionos).
        - Should still include a creative or functional suffix tied to its role.
        - Examples:
          - `elitehr_benefit_genie`
          - `policy_mapper_acme`
          - `visionos_docpulse`
          - `medsys_ai_default_assist`

- **description**
  - Must be a single string.
  - Should describe the s scope, functionality, and output in the context of the domain.
  - Avoid vague wording. Stay precise and technical.
  - Do not duplicate across all llms.
- **model_provider**
  - Must specify a realistic LLM provider (e.g., OpenAI, Google, Anthropic, Alibaba).
  - Ensure compatibility with the chosen `model_name`.
- **model_name**
  - Must specify a specific, realistic model offered by the provider.
  - Ensure the model aligns with the llms’s described functionality.
  - get the exam name form the provided model list. use the standard naming conventions.
- **is_workspace_default**
  - Set to `true` for exactly 15  in the output to indicate the default model for the workspace.
  - All other handlers should have `false`.

## Output Format and Quality Criteria
- Return exactly 50 JSON objects as a well-formed JSON array.
- Ensure no duplicates across any of the fields.
- Each catalog must represent a distinct role in an LLM workflow within the given domain.
- Keep the JSON strictly structured — no extra explanations or markdown in the final output.

---

## Output Format:

```json
{{
    "name": "elithr_infrovista",
    "description": "Creates visually appealing infographic summaries of employee benefit plans for EliteHR.",
    "model_provider": "Google",
    "model_name": "gemini-2.5-pro",
    "is_workspace_default": true
  }},

{{
    "name": "claude_oracle",
    "description": "Analyzes code for cyclomatic complexity and other metrics, suggesting simplification for improved maintainability.",
    "model_provider": "Claude",
    "model_name": "claude-3-7-sonnet",
    "is_workspace_default": false
  }}


## Final Instructions

- Your response must be a valid JSON array of 50 handler objects tailored to the given domain.
    35 for is_workspace_default = False
    15 for  is_workspace_default = True
- No extra formatting, no markdown — just clean JSON.

---

"""
