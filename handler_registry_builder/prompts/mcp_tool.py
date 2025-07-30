MCP_TOOL_PROMPT = """

You are an expert system designer tasked with designing realistic and logically sound MCP (Model Context Protocal) tools that perform a well-defined function in enterprise software.
Each tool must be **distinct, purpose-driven**, and adhere to a standardized JSON structure for enterprise AI systems.


Your task is to generate 75  JSON catalog for MCP based systems, specifically tailored to above given  domain.


### Thought Process / Thinking Steps
    1. Understand the Given Domain: Begin by analyzing the provided domain to deeply understand its workflows,  and operational challenges.

    2. you must study following Diverse sub areas on above selected domain and derive 75 distinct and realistic use cases to intergrate MPC tools that can logically occur within the scope of this  domain . 
    Ensure that each use case represents a different functionality or process.          

    3. Create Unique MCP Tools:   
        -**Identify the Domain and Use Case Scenario:**
            - Think of a realistic, useful scenario in the given domain.
            - The tool should perform a clear realistic function .
            - Identify a brief summary of this imagined scenario as the *function of the tool*.

        - Imagine the Function Internally
            - Ask yourself: “To perform this function, what parameters are logically needed?”
            - Think realistically. Do not make up fields that sound fake.
            - Ensure the parameters are well-scoped and appropriate for real production systems.

    -For each use case, design a separate MCP tool with a unique function.
    -Ensure that each tool has a distinctive and meaningful name, a clear and specific description, a unique server_name, and a well-structured input_schema.

    4. Design Input Schema Per Tool:
    - Define Parameters
        - Define all input parameters in the `properties` section.
        - For each parameter, provide:
        - `"title"`: A human-readable label
        - `"type"`: JSON schema type — e.g., `"string"`, `"integer"`, `"boolean"`, `"object"`, or `"array"`

    - Select Required Parameters
        - From the list of properties, **identify only the truly essential parameters** — the ones **required to invoke** the tool.
        - These go in the `"required"` list.
        - Be logical — if a parameter is critical to function execution, include it.
        - If it is helpful but not essential, **do not include it in the `required` list**, but still define it under `properties`.

    5. Ensure Global Uniqueness: Across all 75 tools, confirm that names, descriptions, server names, and schema definitions are not reused or overlapping. Each tool must stand on its own in purpose and structure.

    6. Validate Realism and Relevance: Verify that each tool feels realistic and grounded in domain-specific language, challenges, and input expectations.

    7. Refine and Finalize: Perform iterative reviews to enhance clarity, correctness, and usability of each MCP tool, ensuring JSON validity and enterprise-grade quality throughout.
---

## Output Format for Each MCP Tool

```json
{
  "name": "<unique_tool_name>",
  "server_name":"< A unique name of the backend server that handles the logic >"
  "description": "<Describing the tool's specific function>",
  ""
  "input_schema": {
    "type": "object",
    "properties": {
      "<field_name>": {
        "title": "<Human-readable name for display "
        "type": "<Data type of the field>",
      }

      # ----------  include more fiels_names ----------
    },
    "required": ["<Mandatory field in invoke a tool>"]
  }
}
```

---

## Parameter Reference Table

| **Field**                                | **Type**   | **Description**                                                                                                 |
|------------------------------------------|------------|-----------------------------------------------------------------------------------------------------------------|
| `name`                                   | string     | A unique, descriptive identifier for the tool.                                                                  |
| `server_name`                            | string     | Indicates a unique name for the backend server, service, or plugin that is responsible for handling the execution of this tool.   |
| `description`                            | string     | A clear summary of the tool’s enterprise function.                                |
| `input_schema`                           | object     | Defines the structured unique input arguments the tool expects for validation and execution.                           |
| `input_schema.type`                      | string     | Must always be `"object"` for structured input.                                                                 |
| `input_schema.properties`                | object     | A dictionary where each key is an input parameter name, and the value is a description of that parameter’s type and purpose. |
| `input_schema.properties.title      `    | string     | Human-readable display name that clearly represents the meaning of the field.                                                            |
| `input_schema.properties.type`           | string     | The data type of the input field (title).  
| `input_schema.required`                  | list       | A list of mandatory fields that must be present in the input. Every field listed in `input_schema.required` must BE  exist in `input_schema.properties`. |



MCP_Tool (Object)
│
├── name (String)
│
├── server_name (String)
│
├── description (String)
│
├── input_schema (Object)
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
    │      │
    │      
    │
    ├── required (list)

---

## Key Instructions

###  Tool Name and Server Name Format:
- The MCP tool name must be in snake_case, clearly describing the tool’s specific function using domain-relevant terminology (e.g., patient_intake_tool for healthcare). It must be unique across all tools, distinct from the PascalCase server_name (e.g., PatientIntakeMCP), and avoid repetitive or unrelated names like edu_analytics_tool in non-education domains.
- tool name must convince its is a mcp_tool
- The server_name must follow PascalCase and typically ends in MCP, with a name that reflects the external platform or internal domain (e.g., GithubMCP, GoogleCalendarMCP). 
- Both name and the server name should be unique across the all 75 tools.
- avoiding unrelated or repetitive names like EDuAnaltic, EduAssessMCP use differnt names sticking to the context of the domain.
-

### Description Field Formatting
The description field must be a single valid  string, formatted as follows:
    -The description field must be a single-line valid string. It should:
    - Begin with a concise summary describing the tool’s enterprise function.
    - Optionally mention key inputs and output briefly in plain language.
    - End with the server name in parentheses

---
### Input Schema Design Guidelines
* `input_schema.type` must always be "object".
* For each tool, dynamically identify a set of **semantically meaningful Unique input parameter fields** that align with the tool’s function.
* Define  these fields in `input_schema.properties`, ensuring field names are contextually appropriate. required field must never be defined inside input_schema.properties.
* It should always be placed outside properties but within the input_schema object—at the same level as type and properties.
* Use a diverse mix of types: `string`, `integer`, `boolean`, etc.
* **Do not use repetitive structures**—ensure that schemas vary naturally across tools.
* Optional fields 

---

### Required Field Structure

* Define `input_schema.required` as a separate list **at the same level as** `input_schema.properties`. `input_schema.required` is not a nested  field with in the `input_schema.properties
* This list must:

  * Contain **only strings that reference valid property keys** from `input_schema.properties`.
  * Never be embedded inside any individual field under `properties`.
  * Include only the **most critical** fields needed to perform the tool’s core function—not every field.
  * Never be a empty field.

---

### 🔹 Output Format and Diversity

* Generate **exactly 75 diverse mcp tools from a distinct domain.
* All tool attributes (`name`, `server_name`, `description`, input_schema) must be unique. 
* Do not reuse or repeat input schema structures across tools.
* Tool functionality and schema design must reflect realistic, domain-specific enterprise needs.

### Read & Learn from the Example — Do Not Copy It
Carefully study the example tools provided  to understand how each field is structured, including:
name, server_name, description, and input_schema . Do not reuse or adapt the scenario, use case, or textual content of the example (e.g., GitHub-related functionality or field names).
Instead, learn the structure and formatting principles illustrated in the example, then apply them to original, realistic use cases from new domains.


{
    "name": "repo_gen_tool",
    "server_name": "GithubMCP",
    "description": "Creates a new GitHub repository for the authenticated user. Requires parameters: name, optional description, and a private flag (defaults to false). Returns repository details or an error message. (Server: GithubMCP)"
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {
                "title": "Name",
                "type": "string"
            },
            "access_token": {
                "title": "Access Token",
                "type": "string"
            },
            "description": {
                "default": "",
                "title": "Description",
                "type": "string"
            },
            "private": {
                "default": false,
                "title": "Private",
                "type": "boolean"
            }
        },
        "required": [
            "name",
            "access_token"
        ]
    }
},
{
    "name": "get_branch_naming_tool",
    "server_name": "GithubMCP",
    "description": "Retrieves all branch names of a specific repository. Input parameters: `owner` (Owner of the repository), `repo` (Name of the repository). Output: Returns a list of branch names or an error message. Server: GithubMCP",
    "input_schema": {
        "type": "object",
        "properties": {
            "owner": {
                "title": "Owner",
                "type": "string"
            },
            "repo": {
                "title": "Repo",
                "type": "string"
            },
            "access_token": {
                "title": "Access Token",
                "type": "string"
            }
        },
        "required": [
            "owner",
            "repo",
            "access_token"
        ]
    }
},
{
    "name": "create_calendar_event_tool",
    "server_name": "GoogleCalendarMCP",
    "description": "Creates an event in a Google Calendar. Requires parameters: summary (title of the event), start_time and end_time (RFC3339 format), calendar_id (defaults to primary), description, and location. Returns created event details or an error. (Server: GoogleCalendarMCP)"
    "input_schema": {
        "type": "object",
        "properties": {
            "access_token": {
                "title": "Access Token",
                "type": "string"
            },
            "summary": {
                "title": "Summary",
                "type": "string"
            },
            "start_time": {
                "title": "Start Time",
                "type": "string"
            },
            "end_time": {
                "title": "End Time",
                "type": "string"
            },
            "calendar_id": {
                "default": "primary",
                "title": "Calendar Id",
                "type": "string"
            },
            "description": {
                "default": "",
                "title": "Description",
                "type": "string"
            },
            "location": {
                "default": "",
                "title": "Location",
                "type": "string"
            }
        },
        "required": [
            "access_token",
            "summary",
            "start_time",
            "end_time"
        ]
    }
},
{
    "name": "list_events_on_day",
    "server_name": "GoogleCalendarMCP",
    "description": "Lists all events on a specific day from a Google Calendar. Requires parameters: date (in YYYY-MM-DD format) and calendar_id (defaults to primary). Returns a list of events on that day. (Server: GoogleCalendarMCP)"
    "input_schema": {
        "type": "object",
        "properties": {
            "access_token": {
                "title": "Access Token",
                "type": "string"
            },
            "date": {
                "title": "Date",
                "type": "string"
            },
            "calendar_id": {
                "default": "primary",
                "title": "Calendar Id",
                "type": "string"
            }
        },
        "required": [
            "access_token",
            "date"
        ]
    }
},
{
    "name": "jira_create_issue",
    "server_name": "JiraMCP",
    "description": "Creates a new Jira issue. Requires parameters: project_id (e.g., 10000), summary (title of the issue), and issue_type_id (e.g., 10006 or 10007). Returns created issue details including key, ID, self URL, and a message. (Server: JiraMCP)"
    "input_schema": {
        "type": "object",
        "properties": {
            "project_id": {
                "title": "Project Id",
                "type": "integer"
            },
            "summary": {
                "title": "Summary",
                "type": "string"
            },
            "issue_type_id": {
                "title": "Issue Type Id",
                "type": "integer"
            },
            "api_token": {
                "title": "Api Token",
                "type": "string"
            },
            "service_base_url": {
                "title": "Service Base Url",
                "type": "string"
            },
            "service_email": {
                "title": "Service Email",
                "type": "string"
            }
        },
        "required": [
            "project_id",
            "summary",
            "issue_type_id",
            "api_token",
            "service_base_url",
            "service_email"
        ]
    }
},

---
## last check 
required field must never be defined inside input_schema.properties. It should always be placed outside properties but within the input_schema object—at the same level as type and properties.   

## Final Output Requirement

- Provide the output as a valid **JSON array** of **75 mpc tool objects** for the given domain).
- The JSON must be well-formed and adhere to the specified structure.
"""

