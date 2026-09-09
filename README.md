# Nova HR — AI-Powered HR Assistant

Gradio chatbot that answers HR questions by **calling tools** through LangChain. Runs are traced in LangSmith when you set an API key.

## What it can do

| User question | Tool |
|---|---|
| "Can you retrieve my employee details?" | `get_employee_details` |
| "What is my remaining leave balance?" | `check_leave_balance` |
| "Generate interview questions for a Data Scientist." | `generate_interview_questions` |
| "What is the remote work policy?" | `get_company_policy` |

Tools return **mocked HR data** only. Unknown employee IDs, invalid IDs, unknown tool names, and missing arguments are rejected instead of invented.

## Setup

```powershell
cd "c:\Users\MB\Desktop\HR Assistant with Nova HR"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set **one** LLM key:

- OpenAI: `OPENAI_API_KEY` (default model `gpt-4o`)
- Gemini: `GOOGLE_API_KEY` (default model `gemini-2.0-flash`)

Optional LangSmith tracing:

```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_PROJECT=hr-assistant-nova
```

Force a provider if both keys exist:

```
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
```

or

```
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash
```

## Run

```powershell
python app.py
```

Open the local Gradio URL (usually `http://127.0.0.1:7860`).

Pick a demo employee in the sidebar, then ask questions. The default ID `E12345` matches the assignment examples (12 remaining leave days for Amira Nasser).

## How tool calling works

1. The chat model is loaded with `bind_tools(...)`.
2. Nova HR decides whether a tool is needed.
3. Each tool call is validated: name must be in the registry, arguments must match the tool schema.
4. The mocked function runs and a `ToolMessage` is sent back to the model.
5. The model writes the final answer, streamed token-by-token in Gradio.
6. Conversation history is kept per browser session (clear chat starts a new thread).

Invalid tool names never execute. They return:

```json
{"error": "invalid_tool", "message": "...", "available_tools": [...]}
```

## Project layout

- `tools.py` — mocked HR functions and LangChain `@tool` wrappers
- `assistant.py` — LLM factory, validation loop, LangSmith tracing, streaming
- `app.py` — Gradio UI
- `.env.example` — keys and model settings

## Demo employees

| ID | Name | Role |
|---|---|---|
| E12345 | Amira Nasser | Software Engineer |
| E10001 | Omar Farouk | Engineering Manager |
| E20010 | Sara Adel | Data Scientist |
| E30022 | Youssef Kamal | HR Specialist |
| E40015 | Nour El-Sayed | Product Manager |
