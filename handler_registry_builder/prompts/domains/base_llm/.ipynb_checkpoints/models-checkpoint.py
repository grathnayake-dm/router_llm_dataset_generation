MODELS = """



### provider Google

| model_name        | Input Types                 | Capabilities                                                  |
|-----------------------|-----------------------------|---------------------------------------------------------------|
| gemini-2.5-pro        | Audio, images, videos, text, PDF | Enhanced thinking and reasoning, multimodal understanding, advanced coding |
| gemini-2.5-flash      | Audio, images, videos, text | Adaptive thinking, cost efficiency                            |
| gemini-2.0-flash      | Audio, images, videos, text | Next-generation features, speed, real-time streaming          |
| gemini-2.0-flash-lite | Audio, images, videos, text | Cost efficiency, low latency                                  |
| gemini-1.5-flash      | Audio, images, videos, text | Fast and versatile performance across diverse tasks           |
| gemini-1.5-flash-8b   | Audio, images, videos, text | High-volume, lower-intelligence tasks                         |
| gemini-1.5-pro        | Audio, images, videos, text | Complex reasoning tasks requiring high intelligence           |
| gemini-embedding-001  | Text                        | Measuring relatedness of text strings                         |
| veo-2.0-generate-001  | Text, images                | High-quality video generation                                |


### CLOUDE 
provider Anthropic
|  model_name                | **Multimodal (Text+Image)** | **Capabilities**                                                               |
|----------------------------|-----------------------------|--------------------------------------------------------------------------------|
| claude-opus-4-0            | Yes                         | Most powerful; superior reasoning, extended thinking, 200K context, 32K output  |
| claude-sonnet-4-0          | Yes                         | High-performance; fast, excellent reasoning, 200K context, 64K output           |
| claude-3-7-sonnet          | Yes                         | Early extended thinking, fast, balanced, 200K context, 64K output               |
| claude-3-5-sonnet          | Yes                         | Previous-gen smart model; fast and capable, 200K context, 8192 output           |
| claude-3-5-haiku-          | Yes                         | Fastest model; optimized for low latency, 200K context, 8192 output             |
| (not listed)               | Yes                         | Complex tasks, fluent & intelligent, 200K context, 4096 output                  |
| (not listed)               | Yes                         | Compact & responsive; near-instant answers, 200K context, 4096 output           |




### QWEN 
provider Allibaba
| model_name         | Input & Output Modalities                    | Capabilities                                                                                             |
| ------------------ | -------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Qwen-VL**        | Text + Image (input), Text (output)          | OCR, visual reasoning, image-to-text summary, and question answering from images.                        |
| **Qwen2-Audio**    | Audio (input), Text (output)                 | Speech recognition, transcription, and audio understanding.                                              |
| **Qwen2-VL**       | Text + Image (input), Text (output)          | Image understanding, visual reasoning, and document analysis.                                            |
| **Qwen2.5**        | Text (input/output)                          | Enhanced knowledge, instruction-following, coding/math, multilingual support (29+ languages).            |
| **Qwen2.5-Coder**  | Text (input/output)                          | Advanced code generation, optimization, and debugging.                                                   |
| **Qwen2.5-VL**     | Text + Image (input), Text (output)          | Image-text reasoning with math-heavy tasks and large context support.                                    |
| **QwQ-32B**        | Text (input/output)                          | Strong mathematical and logical reasoning model, trained with reinforcement learning.                    |
| **Qwen2.5-Omni**   | Text (input/output)                          | Unified generalist model with balanced performance across text and structured reasoning tasks.           |
| **Qwen3**          | Text (input/output)                          | Thinking/Non-thinking modes, advanced reasoning, multilingual, agent tools, and human preference skills. |
| **Qwen2.5-14B**    | Text (input/output)                          | Instruction-following with advanced text generation and structured data understanding.                   |
| **Qwen2.5-7B**     | Text (input/output)                          | Lightweight variant of Qwen2.5 with broad capabilities.                                                  |
| **Qwen2.5-32B**    | Text (input/output)                          | Larger parameter model with enhanced performance.                                                        |
| **Qwen2.5-72B**    | Text (input/output)                          | Largest Qwen2.5 model for complex generative and reasoning tasks.                                        |
| **Qwen3-32B**      | Text (input/output)                          | Mid-range thinking-capable model with strong reasoning.                                                  |
| **Qwen3-30B**      | Text (input/output)                          | Compact and cost-efficient; reasoning supported.                                                         |
| **Qwen3-14B**      | Text (input/output)                          | Supports CoT; creative writing, dialogue, and logic.                                                     |
| **Qwen3-8B**       | Text (input/output)                          | Versatile small-scale model with reasoning and instruction following.                                    |
| **Qwen3-4B**       | Text (input/output)                          | Lightweight for inference tasks; supports thinking.                                                      |
| **Qwen3-1.7B**     | Text (input/output)                          | Efficient model for concise tasks; thinking + response limit combined.                                   |
| **Qwen3-0.6B**     | Text (input/output)                          | Entry-level Qwen3 model; compact and affordable.                                                         |



###  MISTRAL


| API Name                  | Input Type(s)     | Output Type(s)      | Capabilities / Description                                                                            |
| ------------------------- | ----------------- | ------------------- | ----------------------------------------------------------------------------------------------------- |
| `mistral-medium-2505`     | Text, Image       | Text                | Frontier-class **multimodal** model; high reasoning, vision, and language ability (May 2025 release). |
| `magistral-medium-2506`   | Text              | Text                | Frontier-class **reasoning** model (June 2025); optimized for accuracy and structured tasks.          |
| `codestral-2501`          | Code, Text        | Code                | **Coding-specialized** model (Jan 2025); excels in FIM, test-gen, code correction.                    |
| `voxtral-mini-2507`       | Audio (speech)    | Text                | Efficient **transcription** model; audio to text.                                                     |
| `devstral-medium-2507`    | Text, Code        | Text, Code          | Enterprise-grade **developer agent model**; code exploration, editing, tool use.                      |
| `mistral-ocr-2505`        | Images, Documents | Structured Text     | OCR model for extracting **interleaved text/images**; Document AI stack.                              |
| `ministral-3b-2410`       | Text              | Text                | **Edge model**, optimized for low resource devices.                                                   |
| `ministral-8b-2410`       | Text              | Text                | Edge model, **high performance/price ratio**.                                                         |
| `mistral-large-2411`      | Text, Image       | Text                | **Top-tier large** multimodal model; high complexity tasks (Nov 2024).                                |
| `pixtral-large-2411`      | Text, Image       | Text                | First **frontier multimodal** model from Mistral (Nov 2024).                                          |
| `mistral-small-2407`      | Text              | Text                | Lightweight small model, updated version (Sep 2024).                                                  |
| `mistral-embed`           | Text              | Embedding Vector    | Semantic **text embedding** model.                                                                    |
| `codestral-embed`         | Code              | Embedding Vector    | Semantic **code embedding** model.                                                                    |
| `mistral-moderation-2411` | Text              | Labels (Moderation) | **Harmful content detection** for moderation tasks.                                                   |

| API Name               | Input Type(s)       | Output Type(s) | Capabilities / Description                                                |
| ---------------------- | ------------------- | -------------- | ------------------------------------------------------------------------- |
| `voxtral-small-2507`   | Audio, Text         | Text           | Audio input model for **instruct tasks**.                                 |
| `voxtral-mini-2507`    | Audio               | Text           | Mini transcription model (efficient and accurate).                        |
| `mistral-small-2506`   | Text                | Text           | Updated **small language model** (June 2025).                             |
| `magistral-small-2506` | Text                | Text           | Small **reasoning model**, optimized for accuracy (June 2025).            |
| `devstral-small-2507`  | Text, Code          | Text, Code     | Updated open-source **developer agent** model (July 2025).                |
| `mistral-small-2503`   | Text, Image         | Text           | Small **multimodal** model (March 2025) with image understanding.         |
| `mistral-small-2501`   | Text                | Text           | Compact language model (Jan 2025).                                        |
| `devstral-small-2505`  | Text, Code          | Text, Code     | Earlier version of **developer agent** (May 2025).                        |
| `open-codestral-mamba` | Code                | Code           | Open-source **Mamba2-based code model**; high throughput (July 2024).     |
| `pixtral-12b-2409`     | Text, Image         | Text           | 12B **multimodal model** for open-source use (Sept 2024).                 |
| `open-mistral-nemo`    | Text (multilingual) | Text           | 12B **multilingual** open-source model (July 2024).                       |
| `mathstral-7b`         | Math, Text          | Text           | Specialized in **mathematics** (symbolic reasoning, formulas, July 2024). |

### OPENAI

---

### # **Featured & Flagship Chat Models**

| API Name               | Input Types        | Output Types       | Capabilities / Use Case                                    |
| ---------------------- | ------------------ | ------------------ | ---------------------------------------------------------- |
| `gpt-4.1`              | Text               | Text               | Flagship GPT-4 model for complex, high-intelligence tasks  |
| `gpt-4o`               | Text, Image, Audio | Text, Image, Audio | Multimodal model for chat, vision, and audio understanding |
| `chatgpt-4o-latest`    | Text, Image, Audio | Text, Image, Audio | Same as `gpt-4o`, used in ChatGPT product                  |
| `gpt-4o-audio-preview` | Text, Audio        | Audio              | Audio generation and comprehension preview                 |

---

#### **Reasoning Models (o-series)**

| API Name  | Input Types | Output Types | Capabilities / Use Case                      |
| --------- | ----------- | ------------ | -------------------------------------------- |
| `o3`      | Text        | Text         | Most powerful reasoning model                |
| `o3-pro`  | Text        | Text         | o3 with more compute for improved accuracy   |
| `o3-mini` | Text        | Text         | Smaller, faster o3 variant                   |
| `o4-mini` | Text        | Text         | Fast, affordable model for complex reasoning |
| `o1`      | Text        | Text         | Older o-series reasoning model               |
| `o1-pro`  | Text        | Text         | More powerful version of `o1`                |
| `o1-mini` | Text        | Text         | Deprecated small version of `o1`             |

---

####**Deep Research Models**

| API Name                | Input Types | Output Types | Capabilities / Use Case                      |
| ----------------------- | ----------- | ------------ | -------------------------------------------- |
| `o3-deep-research`      | Text        | Text         | Most powerful multi-step deep research model |
| `o4-mini-deep-research` | Text        | Text         | Faster, cost-efficient deep research model   |


---

#### **Cost-Optimized Models**

| API Name                    | Input Types | Output Types | Capabilities / Use Case                   |
| --------------------------- | ----------- | ------------ | ----------------------------------------- |
| `gpt-4.1-mini`              | Text        | Text         | Balanced speed, cost, intelligence        |
| `gpt-4.1-nano`              | Text        | Text         | Fastest and most affordable GPT-4.1 model |
| `gpt-4o-mini`               | Text        | Text         | Affordable GPT-4o variant for quick tasks |

---

#### **Image Generation Models**

| API Name      | Input Types | Output Types | Capabilities / Use Case                    |
| ------------- | ----------- | ------------ | ------------------------------------------ |
| `gpt-image-1` | Text        | Image        | Latest image generation (state-of-the-art) |
| `dall-e-3`    | Text        | Image        | Previous-gen image generation              |
| `dall-e-2`    | Text        | Image        | First-gen image generation                 |

---

#### **Text-to-Speech (TTS)**

| API Name          | Input Types | Output Types | Capabilities / Use Case     |
| ----------------- | ----------- | ------------ | --------------------------- |
| `gpt-4o-mini-tts` | Text        | Audio        | GPT-4o mini based TTS       |
| `tts-1`           | Text        | Audio        | Optimized for speed         |
| `tts-1-hd`        | Text        | Audio        | Optimized for audio quality |

---

####**Transcription (Speech-to-Text)**

| API Name                 | Input Types | Output Types | Capabilities / Use Case            |
| ------------------------ | ----------- | ------------ | ---------------------------------- |
| `gpt-4o-transcribe`      | Audio       | Text         | Transcribe + translate audio       |
| `gpt-4o-mini-transcribe` | Audio       | Text         | Lightweight transcription model    |
| `whisper-1`              | Audio       | Text         | General-purpose speech recognition |

---

#### **Tool-Specific Models**

| API Name                     | Input Types | Output Types | Capabilities / Use Case                         |
| ---------------------------- | ----------- | ------------ | ----------------------------------------------- |
| `gpt-4o-search-preview`      | Text        | Text         | Search-augmented GPT-4o model                   |
| `gpt-4o-mini-search-preview` | Text        | Text         | Fast, affordable search-capable GPT model       |
| `computer-use-preview`       | Text        | Text         | Optimized for computer interaction tools        |
| `codex-mini-latest`          | Code, Text  | Code         | Fast model for **Codex CLI** and code reasoning |

---

#### **Embeddings**

| API Name                 | Input Types | Output Types     | Capabilities / Use Case            |
| ------------------------ | ----------- | ---------------- | ---------------------------------- |
| `text-embedding-3-small` | Text        | Vector Embedding | Fast, cost-effective embedding     |
| `text-embedding-3-large` | Text        | Vector Embedding | Most powerful embedding model      |
| `text-embedding-ada-002` | Text        | Vector Embedding | Older, widely used embedding model |

---



### DEEPSEEK 

| **Model Name**      | **API Name / Version** | **Input Types** | **Output Types** | **Capabilities / Description**                                                                    |
| ------------------- | ---------------------- | --------------- | ---------------- | ------------------------------------------------------------------------------------------------- |
| `deepseek-chat`     | `DeepSeek-V3-0324`     | Text            | Text             | General-purpose **chat model** for reasoning, generation, and dialogue. Released March 2024.      |
| `deepseek-reasoner` | `DeepSeek-R1-0528`     | Text            | Text             | Advanced **multi-step reasoning model** specialized for complex logical tasks. Released May 2024. |


### META 
| **Model ID**                                  | **Provider** | **Input Modalities** | **Output Modalities** | **Primary Purpose**                             |
| --------------------------------------------- | ------------ | -------------------- | --------------------- | ----------------------------------------------- |
| `Llama-4-Maverick-17B-128E-Instruct-FP8`      | Meta         | Text, Image          | Text                  | Multimodal instruction-following                |
| `Llama-4-Scout-17B-16E-Instruct-FP8`          | Meta         | Text, Image          | Text                  | Lightweight multimodal assistant                |
| `Llama-3.3-70B-Instruct`                      | Meta         | Text                 | Text                  | General-purpose language model                  |
| `Llama-3.3-8B-Instruct`                       | Meta         | Text                 | Text                  | Lightweight general-purpose model               |
| `Cerebras-Llama-4-Maverick-17B-128E-Instruct` | Cerebras     | Text                 | Text                  | Efficient inference of Maverick-17B on Cerebras |
| `Cerebras-Llama-4-Scout-17B-16E-Instruct`     | Cerebras     | Text                 | Text                  | Efficient inference of Scout-17B on Cerebras    |
| `Groq-Llama-4-Maverick-17B-128E-Instruct`     | Groq         | Text                 | Text                  | Ultra-fast inference via Groq for Maverick-17B  |


"""




__all__ = ["MODELS"]
