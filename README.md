---

# 🔧 Router LLM Data Generation Pipeline

This project automates the full data processing pipeline for different handler types (`rag`, `base_llm`, `mcp_tool`, `worker_agent`). It builds registries, generates static and contextual fields, validates them.

## 📁 Project Structure

```
.
├── main.py
├── handler_registry_builder/
├── static_fields_builder/
├── contextual_fields_builder/
├── data_validation/
├── add_handlers/
├── utils/
├── dataset/
└── README.md
```

---

## 🚀 How It Works

### The pipeline consists of 5 steps for each handler type:

1. **Registry Building**
   Builds the initial handler registry using `RegistryBuilder`.

2. **Static Field Generation**
   Generates structured static fields from registry entries.

3. **Contextual Field Generation**
   Calls an LLM API (e.g., Gemini) to generate contextual fields in batches.

4. **Validation**
   Validates the structured data output using a LLM-.

5. **Handler Appending**
   Appends validated entries back to a handler registry JSONL.
   
6. **Final data**
    After all handlers are processed, the final outputs are merged together.

---

## 🧪 Supported Handler Types

* `rag`
* `base_llm`
* `worker_agent`
* `mcp_tool`
* *(Optional)* Add more by extending the code and API keys in `API_KEYS`.

---

## 🛠️ Requirements

* Python 3.8+
* Google GenAI SDK (`google.generativeai`)
* `click`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧾 Usage

Run the full pipeline for all handler types with a given version:

```bash
python main.py --version <version_id>
```

Example:

```bash
python main.py --version v5
```

---

## ⚙️ Configuration

Update your API keys in `main.py`:

```python
API_KEYS = {
    "rag": "YOUR_RAG_KEY",
    "base_llm": "YOUR_LLM_KEY",
    "worker_agent": "YOUR_AGENT_KEY",
}
```

---

## 📤 Output Structure

Each step generates output in a versioned directory structure:

```
.
├── handler_registry_builder/
│   └── handler_registries/v5/rag/
├── static_fields_builder/
│   └── static_output/v5/rag/
├── contextual_fields_builder/
│   └── contextual_output/v5/rag/
├── data_validation/
│   └── validated_output/v5/rag/
├── add_handlers/
│   └── final_output/v5/rag/
├── merge/
│   └── dataset
│     └── batches
│     └── final_dataset
```

```

---

## 📌 Notes

* Each step includes a `time.sleep(30)` to reduce load and respect rate limits for LLM API usage.
* The script is multi-threaded to process all handler types concurrently.
* All final outputs are merged using `merge_files()`.

---



Here's a list of **sample CLI commands** for each function  defined 
---

## ✅ 1. Run the **Full Pipeline**

```bash
python main.py --version v1

```
