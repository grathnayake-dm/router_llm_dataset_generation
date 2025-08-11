from string import Template

WOKER_AGENT_PROMPT = Template("""

You are a seasoned systems architect and domain expert tasked with designing a catalog of realistic and logically consistent worker agents for enterprise AI automation.
you have to create `$count`  realistic worker agent catalog entries for the above given domain.

Each worker agent should represent an autonomous, specialized component that performs a well-defined operational task in the following given domain:

## Domain
**`$domain`**.

## Thought Process and Design Steps
  -Deeply Analyze the Domain:
    -Understand the domain’s workflows, typical operational tasks, and integration points for autonomous worker agents.

  -Identify Diverse Use Cases:
  -Select `$count` distinct and meaningful worker agent roles that naturally fit into the domain’s operational environment. Each must perform a unique function supporting automation, data processing, or system orchestration.

  -Agent Role Conceptualization:
    -For each agent:

      -Imagine its concrete function — what exact task it performs, how it is invoked, and what output or effect it produces.

      -Consider how the agent would realistically be triggered by external systems or workflows.

  -Determine Input Parameters:

    -Identify all logical input parameters the agent requires to function.

    - Parameters must be realistic and relevant to the domain task, reflecting true operational needs.

    -Define parameter data types (string, integer, boolean, enum, etc.) and provide clear descriptions.

  -Separate Required vs Optional Inputs:    
    
    -Mark as required only those parameters essential for invocation.

    -Include optional parameters if they add flexibility or tuning but are not mandatory.

  -Design a Realistic API Endpoint:    
    -Create a believable HTTP endpoint URL for the agent’s service, reflecting domain context, API versioning, and resource semantics.

    -The endpoint should be a real-world style URL, suitable for enterprise production environments.

  -Generate Workspace ID:

    -Assign a valid UUID v4 string to represent the agent’s workspace or operational context.

  -Produce a Clean, Valid JSON Catalog Entry:

## Output Format for Each  Worker Agent

```json
{
  "name": "<unique_worker_agent_name>",
  "description": "<Describing the  Worker Agent's specific function>",
  "http_endpoint": "<Realistic API endpoint URL>",
  "payload_schema": {
    "type": "object",
    "properties": {
      "<field_name>": {
        "title": "<Human-readable name for display>",
        "type": "<Data type of the field>"
      }

      # ----------  include more field_names ----------
    },
    "required": ["<Mandatory field to invoke the  Worker Agent>"]
  },
  "workspace_id": "<valid_uuid_v4_string>"
}
```
---

## Parameter Reference Table

| **Field**                       | **Type** | **Description**                                                                                                                                 |
| ------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                          | string   | A unique, descriptive identifier for the Worker Agent (lowercase, underscores).                                                                 |
| `description`                   | string   | A clear summary of the Worker Agent’s enterprise function and parameters, formatted as a single string.                                         |
| http_endpoint                    | string | A unique, reliable URL that the agent uses for invocation or service calls. |
| `payload_schema`                  | object   | Defines the structured unique input arguments the Worker Agent expects for a invocation.                                            |
| `payload_schema.type`             | string   | Must always be `"object"` for structured input.                                                                                                 |
| `payload_schema.properties`       | object   | A dictionary where each key is an input parameter name, and the value describes that parameter’s type and purpose.                              |
| `payload_schema.properties.title` | string   | Human-readable display name that clearly represents the meaning of the field.                                                                   |
| `payload_schema.properties.type`  | string   | The data type of the input field.                                                                                                               |
| `payload_schema.required`         | list     | A list of mandatory fields that must be present in the input. Each required field must exist in `properties`. The list must **never be empty**. |
|  `workspace_id`                   | string (UUID) | A unique UUID identifying the workspace associated with the Worker Agent. |

Woker_Agent (Object)
│
├── name (String)
│
├── description (String)
│
├── payload_schema (Object)
    │
    ├── type (String)
    │
    ├── properties (Object)
    │   │
    │   ├── <field_name> (Object)
    │      │
    │      ├── title (String)
    │      │
    │      ├── type (String)
    │      
    ├── required (list of strings)
    ├── workspace_id (UUID strings)


## Key Instructions

###  Worker Agent Name  Format:

- The name must clearly express the function in lowercase with underscores .
- name should be unique across the all generated worker agents.
- creative,  unique, never-before-heard names for AI agents.
    - ex: Azura, Aplex


### Description Field 
- The description field must be a single string, clearly describing the Worker Agent’s specialty, its inputs (parameters), and expected outputs or behavior.

---
### Endpoint Similarity Constraint
    - Avoid assigning multiple Worker Agents with HTTP endpoints that appear similar or follow the same structural pattern or rhyming scheme (e.g.,
        - "https://curriculum.ai/api/v1/topics/outline" and
        - "https://curriculum.ai/api/v1/assessments/propose").
    - Avoid using dummy terms such as example, test, or placeholder values in the http_endpoint (e.g., https://support.example.com/api/v1/tickets/triage). Use realistic, meaningful, and domain-relevant naming conventions in the URL path to reflect actual enterprise functionality.    - Each http_endpoint must be distinct and realistic, representing a unique function or service invocation path.
    - Overlapping or templated endpoint patterns reduce diversity and violate real-world plausibility.



### Payload Schema Design Guidelines

Got it! You want a corrected and clear **specification for the `payload_schema`** (not `input_schema`) section for Worker Agents, that fits the realistic usage and your requirements, based on your detailed guidelines but adjusted to **use `payload_schema`** instead of \`input\_schema\*\*.

Here’s the updated version for your **Worker Agent `payload_schema` design guidelines** and **description field**, aligned with your instructions and fixing the terminology:

---

### Description Field

* The `description` field must be a **single string**, clearly describing the Worker Agent’s specialty, its inputs (parameters), and expected outputs or behavior.

---

### Payload Schema Design Guidelines

* `payload_schema.type` must always be `"object"`.
* For each Worker Agent, **dynamically identify** a set of semantically meaningful and **unique input parameter fields** that align with the Worker Agent’s specific function.
* Define these fields under `payload_schema.properties` using **contextually appropriate field names**.
* The `payload_schema.required` field must **never be nested inside** `payload_schema.properties`. It should be a separate list at the same level as `type` and `properties`.
* Use a diverse mix of valid JSON Schema data types: `"string"`, `"integer"`, `"boolean"` etc.
* Avoid repetitive or redundant parameter structures — schemas should vary naturally across different Worker Agents to reflect their distinct roles.

---

  ###  Payload Schema Property Field Guidelines (`<field_name>` keys)

  Each property field must include:
  * `title`: a human-readable display name (e.g., `"Customer Name"`).
  * `type`: a valid JSON Schema data type (`"string"`, `"integer"`, `"boolean"`, etc.).
  * **No other attributes** (like `"default"`, max, min, depedencies, enum, ) are allowed.

---

### Required Field Structure

-Define payload_schema.required as a separate list at the same level as payload_schema.properties. It must never be nested inside individual property definitions.
- This list must:
    - Contain only strings that exactly match keys defined inside payload_schema.properties.
    - Include only the critical parameters essential to invoke the Worker Agent successfully — not necessarily every defined property.
    - The number of parameters listed in required must vary across Worker Agents ,it is valid to define:
        - All fields from properties as required.
        - Only a subset of fields as required.
        - The list must never be empty.

---

### Output Format and Diversity

* Generate exactly **`$count` diverse Worker Agents** for the given domain.
* All Worker Agent attributes (`name`, `description`, `input_schema`) must be unique.
* Avoid reusing or repeating payload schema structures across Worker Agents where possible, while respecting the field count strategy.
* Worker Agent functionality and schema design must reflect realistic, domain-specific enterprise needs for **Business Intelligence and Analytics** tasks.

---

### Read & Learn from the Example — Do Not Copy Its Content

* Study the example Worker Agent definitions carefully to understand field structure:
```json
{  
    "name": "Azzela",
    "description": "Performs statistical analysis on A/B test results to determine a winning variant based on a primary conversion metric. The agent requires the unique experiment ID and the name of the primary metric to calculate statistical significance and declare a winner.",
    "http_endpoint": "https://optimizer.prod-tools.net/api/v1/experiments/analyze",
    "payload_schema": {
        "type": "object",
        "properties": {
            "experiment_id": {
                "title": "Experiment ID",
                "type": "string"
            },
            "primary_metric": {
                "title": "Primary Metric",
                "type": "string"
            },
            "confidence_level": {
                "title": "Confidence Level",
                "type": "integer"
            }
        },
        "required": [
            "experiment_id",
            "primary_metric"
        ]
    },
    "workspace_id": "c5d6e7f8-a9b0-4c1d-8e2f-3a4b5c6d7e8f"
}
{
    "name": "accessibility_compliance_agent",
    "description": "Scans a UI design file or a live URL to ensure it meets specified accessibility standards (e.g., WCAG 2.1 AA). It identifies issues like insufficient color contrast, missing alt text, or improper ARIA roles. Requires the URL or design asset path and the target compliance level.",
    "http_endpoint": "https://a11y-checker.internal/api/v3/scan/webpage",
    "payload_schema": {
        "type": "object",
        "properties": {
            "scan_target_url": {
                "title": "Scan Target URL",
                "type": "string"
            },
            "wcag_level": {
                "title": "WCAG Compliance Level",
                "type": "string"
            }
        },
        "required": [
            "scan_target_url",
            "wcag_level"
        ]
    },
    "workspace_id": "d7e8f9a0-b1c2-4d3e-8f4a-5b6c7d8e9f0a"
}
{
    "name": "Ella",
    "description": "Collects and analyzes unstructured user feedback from multiple sources (e.g., app store reviews, support tickets, surveys) to identify and summarize key themes, sentiment, and feature requests. Requires a data source identifier and a date range for analysis.",
    "http_endpoint": "https://feedback-intel.io/api/v1/aggregate/themes",
    "payload_schema": {
        "type": "object",
        "properties": {
            "data_source_id": {
                "title": "Data Source Identifier",
                "type": "string"
            },
            "start_date": {
                "title": "Start Date",
                "type": "string"
            },
            "end_date": {
                "title": "End Date",
                "type": "string"
            },
            "product_area_filter": {
                "title": "Product Area Filter",
                "type": "string"
            }
        },
        "required": [
            "data_source_id",
            "start_date",
            "end_date"
        ]
    },
    "workspace_id": "e9f0a1b2-c3d4-4e5f-8a6b-7c8d9e0f1a2b"
}
```
---
### Output Schema Exclusion
- The output_schema field must not be included in any Worker Agent object.
- Omit this field entirely—even if the intended output is known.
- This design constraint ensures consistency with the simplified Worker Agent specification and prevents overly large or irrelevant structures in the final JSON.
        "output_schema": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Monitoring status (e.g., 'alert_triggered', 'normal')"
            },
            "details": {
                "type": "string",
                "description": "Details of the alert or status"
            }
        },
        "required": [
            "status"
        ]
    }

this is not a part of the worker agent specification and should not be included in the final output.. its a vialation of the given instrucitons

### Final Output Requirement

* Provide the output as a valid **JSON array** of **`$count` Worker Agent** objects for the Business Intelligence and Analytics domain.
* The JSON must be well-formed and strictly follow the specified structure.

---


""")
