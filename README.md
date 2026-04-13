# Chronos -- Voice-Controlled Local AI Agent 

## Overview
A local AI agent that accepts voice input, converts speech to text, detects user intent, and executes local tools like file creation, code execution, and summarization.

## Project Structure
Chronos/
- (all inside chronos folder)
  - app.py # Streamlit UI
  - agent.py # Intent routing & orchestration
  - tools.py # Tool execution (files, code, etc.)
  - stt.py # Speech-to-text logic
  - output/ # Safe execution directory
  - requirements.txt
  - README.md

# Chronos — Voice Controlled Local AI Agent
A fully offline, voice-controlled AI agent that transcribes speech, detects intent, and executes local actions — built with Whisper, qwen2.5-coder, Ollama, and Streamlit.

<img width="1919" height="919" alt="Screenshot 2026-04-13 224813" src="https://github.com/user-attachments/assets/87843333-75c8-4161-b8c4-94d33d7d5dc1" />
<img width="1919" height="920" alt="Screenshot 2026-04-13 224823" src="https://github.com/user-attachments/assets/f176e861-75f7-45b1-b03f-7faac549f5a2" />
<img width="1919" height="910" alt="Screenshot 2026-04-13 224838" src="https://github.com/user-attachments/assets/61dd3f25-edcf-48a6-91e0-63403a4c1352" />
<img width="1919" height="916" alt="Screenshot 2026-04-13 224847" src="https://github.com/user-attachments/assets/f8dc0571-4556-4555-96ea-8072aa78ca52" />

## Live Demo
Due to local model dependencies (Ollama, Whisper), this project runs locally.
Watch the demo here: https://youtu.be/UmMykbFlc6k

## Architecture
Audio Input --> Speech-to-Text (Whisper) --> Intent Detection (qwen2.5-coder via Ollama) --> Command Routing (Agent Logic)--> Tool Execution (File / Code / System Actions) --> Output Display (Streamlit UI)

## Features
- Voice or file audio input
- Speech to text via OpenAI Whisper (medium model)
- Intent detection via qwen2.5-coder:7b (GPU via Ollama)
- Create files, write code, summarize text, run code, launch files, general chat
- Human-in-the-loop confirmation for file operations
- Session memory — full conversation history
- Direct text summarizer
- 100% offline — no data leaves your machine
- Compound commands supported
- Graceful error handling
- Output folder safety

## Tech Stack
| Component        |             Tool           | 
|------------------|----------------------------|
| Speech to Text   | OpenAI Whisper (medium)    |
| Intent Detection | qwen2.5-coder:7b via Ollama|
| UI               | Streamlit                  |
| Runtime          | Python 3.10                |

## Hardware Used
- NVIDIA RTX 4050 6GB (qwen2.5 inference)
- Intel i7-12650HX
- 12GB DDR5 RAM

## Why this architecture?
The two models never compete for GPU memory. Ollama exposes an Anthropic-compatible API so the Anthropic Python SDK talks to local models with zero code changes.

### Explanation of Each Component

### 1. Audio Input
- Accepts voice input via microphone or uploaded audio file
- Designed to simulate real-world human interaction with AI

---

### 2. Speech-to-Text (STT)
- Implemented using **OpenAI Whisper (medium model)**
- Converts raw audio into accurate textual transcription
- Chosen for its robustness across accents and noisy input

---

### 3. Intent Detection
- Powered by **qwen2.5-coder:7b** running locally via Ollama
- Converts natural language into structured intent

Example:
"Run the calculator file"
↓
{
"intent": "run_code",
"filename": "calculator.py"
}
---

### 4. Agent Logic
- Central decision-making layer
- Maps detected intent to appropriate tool functions
- Handles:
  - Validation
  - Error handling
  - Input normalization

---

### 5. Tool Execution Layer
Responsible for executing real system-level actions:

- File creation and modification
- Code generation and saving
- Running Python scripts in terminal
- Opening files in VS Code
- Text summarization

All operations are modular and extendable.

---

### 6. Streamlit UI
- Provides an interactive interface
- Displays:
  - Transcribed text
  - Detected intent
  - Execution output
- Enables both voice and manual text input

---

## Key Features

### Voice Interaction
- Accepts real-time voice commands
- Enables natural human-AI interaction

### Intelligent Intent Parsing
- Uses LLM reasoning to convert language → structured commands

### Code Generation & Execution
- Automatically writes and executes Python scripts

### File Management
- Create, open, and manage files dynamically

### Text Summarization
- Extracts key information from large text inputs

### Compound Commands
- Handles multi-step instructions logically

### Human-in-the-Loop Safety
- Confirms sensitive actions before execution

### Session Memory
- Maintains conversation context within a session

### Secure Execution Environment
- All operations are sandboxed inside `/output` directory

### Fully Offline
- No external API calls
- Ensures complete privacy

---

## Tech Stack

| Component        | Technology Used              |
|------------------|------------------------------|
|Speech Recognition| OpenAI Whisper (medium)      |
| LLM (Intent)     | qwen2.5-coder:7b via Ollama  |
| Interface        | Streamlit                    |
| Backend Logic    | Python                       |

---

## Hardware Configuration

- GPU: NVIDIA RTX 4050 (6GB VRAM)
- CPU: Intel i7-12650HX
- RAM: 12GB DDR5

This setup enables efficient local inference for both Whisper and LLM models.

---

## Design Decisions

### 1. Local-First Approach
- Eliminates dependency on cloud APIs
- Reduces latency and improves privacy

### 2. Model Separation
- Whisper and LLM run independently
- Prevents GPU memory conflicts

### 3. Modular Tool System
- Each function is isolated and reusable
- Easy to extend with new capabilities

### 4. Intent-Based Routing
- Converts unstructured input into structured commands
- Makes the system scalable and maintainable

---

## Setup

### Requirements
- Python 3.10+
- Ollama installed (ollama.com)
- NVIDIA GPU recommended

### Installation
```bash
git clone https://github.com/YOURUSERNAME/chronos-ai
cd chronos-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Pull Models
```bash
(if ollama not started then -- ollama serve) then
ollama pull qwen2.5-coder:7b
```

### Run
```bash
streamlit run app.py
```

## Supported Commands (Examples)
- "Create a file called notes.txt with my shopping list"
- "Write a Python file called calculator with add and subtract functions"
- "Summarize this: [text]"
- "Run the calculator file"
- "Open the shopping file"
- "What is machine learning?"

## Output Folder
- All file operations are sandboxed to the `/output` folder for safety.
- Prevents accidental modification of system files
- Controlled execution environment

## What I'd improve
- Model benchmarking between llama3 and qwen2.5
- Autonomous multi-step planning agent
- Cross-language execution support
- Persistent long-term memory
- GUI automation (mouse/keyboard control)
- Deployment as a desktop assistant

## Conclusion

Chronos demonstrates how modern local AI models can be combined into a cohesive system capable of understanding and executing real-world tasks. This project highlights the potential of offline AI agents as powerful, privacy-preserving alternatives to cloud-based assistants.

## Article
https://dev.to/parzivalz73/i-built-a-fully-offline-voice-controlled-ai-agent-using-whisper-and-qwen25-5ehk




