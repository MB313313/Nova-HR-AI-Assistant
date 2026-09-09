"""LangChain HR assistant with validated tool calling and LangSmith tracing."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool
from langsmith import traceable

from tools import ALLOWED_TOOL_NAMES, HR_TOOLS, TOOL_REGISTRY, list_employee_directory

load_dotenv()

MAX_TOOL_ROUNDS = 5

SYSTEM_PROMPT = """You are Nova HR, a careful AI HR assistant for Nova Labs.

You help employees with HR questions. You must use tools for employee records,
leave balances, interview question packs, and company policies. Never invent
those facts.

Tool rules:
- Only call these tools: get_employee_details, check_leave_balance,
  generate_interview_questions, get_company_policy.
- Never invent a tool name, employee ID, leave balance, policy, or interview pack.
- If a required argument is missing, ask the user instead of guessing.
- Employee IDs look like E12345. If the user says "my" or "I" and a logged-in
  employee ID is provided below, use that ID.
- If a tool returns an error, explain it clearly. Do not fabricate a replacement.
- For general chit-chat or process explanations that do not need private data,
  answer directly without tools.
- Keep answers concise, warm, and professional.

Logged-in employee ID: {employee_id}
"""


def _content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or ""))
            elif hasattr(item, "text"):
                parts.append(str(item.text))
        return "".join(parts)
    return str(content)


def _configure_langsmith() -> None:
    api_key = (
        os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY") or ""
    ).strip()
    explicit = (
        os.getenv("LANGSMITH_TRACING") or os.getenv("LANGCHAIN_TRACING_V2") or ""
    ).strip().lower()
    tracing_on = bool(api_key) and explicit in {"true", "1", "yes"}
    tracing = "true" if tracing_on else "false"
    os.environ["LANGSMITH_TRACING"] = tracing
    os.environ["LANGCHAIN_TRACING_V2"] = tracing

    project = (
        os.getenv("LANGSMITH_PROJECT")
        or os.getenv("LANGCHAIN_PROJECT")
        or "hr-assistant-nova"
    )
    os.environ["LANGSMITH_PROJECT"] = project
    os.environ["LANGCHAIN_PROJECT"] = project

    if api_key:
        os.environ["LANGSMITH_API_KEY"] = api_key
        os.environ["LANGCHAIN_API_KEY"] = api_key


_configure_langsmith()


def detect_provider() -> str:
    explicit = (os.getenv("LLM_PROVIDER") or "").strip().lower()
    if explicit:
        return explicit
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
        return "gemini"
    raise RuntimeError(
        "No LLM API key found. Set OPENAI_API_KEY or GOOGLE_API_KEY in a .env file."
    )


def build_llm():
    """Load GPT-4o or Gemini based on environment configuration."""
    _configure_langsmith()
    provider = detect_provider()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    if provider in {"openai", "gpt", "gpt-4", "gpt4"}:
        from langchain_openai import ChatOpenAI

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is missing.")
        model = os.getenv("LLM_MODEL") or "gpt-4o"
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            streaming=True,
            api_key=os.getenv("OPENAI_API_KEY"),
        ), f"OpenAI / {model}"

    if provider in {"gemini", "google", "google_genai"}:
        from langchain_google_genai import ChatGoogleGenerativeAI

        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is missing.")
        model = os.getenv("LLM_MODEL") or "gemini-2.0-flash"
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=api_key,
        ), f"Gemini / {model}"

    raise RuntimeError(
        f"Unsupported LLM_PROVIDER '{provider}'. Use 'openai' or 'gemini'."
    )


@traceable(name="execute_hr_tool", run_type="tool")
def execute_hr_tool(name: str, arguments: dict[str, Any]) -> str:
    """Run a known HR tool only. Reject hallucinated names or bad arguments."""
    if name not in ALLOWED_TOOL_NAMES:
        return json.dumps(
            {
                "error": "invalid_tool",
                "message": f"'{name}' is not a valid HR tool.",
                "available_tools": sorted(ALLOWED_TOOL_NAMES),
            }
        )

    if not isinstance(arguments, dict):
        return json.dumps(
            {
                "error": "invalid_arguments",
                "message": "Tool arguments must be an object.",
            }
        )

    tool_fn: BaseTool = TOOL_REGISTRY[name]
    try:
        result = tool_fn.invoke(arguments)
    except Exception as exc:  # noqa: BLE001 - feed validation errors back to the model
        return json.dumps(
            {
                "error": "invalid_arguments",
                "message": f"Could not run {name}: {exc}",
            }
        )

    if isinstance(result, str):
        return result
    return json.dumps(result, ensure_ascii=False)


class HRAssistant:
    """Multi-turn HR assistant that binds tools, validates calls, and streams replies."""

    def __init__(self) -> None:
        llm, self.model_label = build_llm()
        self.llm_with_tools = llm.bind_tools(HR_TOOLS)
        self._sessions: dict[str, list[BaseMessage]] = {}

    def new_session(self) -> str:
        session_id = str(uuid4())
        self._sessions[session_id] = []
        return session_id

    def clear_session(self, session_id: str) -> str:
        self._sessions.pop(session_id, None)
        return self.new_session()

    def _history(self, session_id: str) -> list[BaseMessage]:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        return self._sessions[session_id]

    def _system_message(self, employee_id: str) -> SystemMessage:
        logged_in = employee_id.strip() if employee_id else "not provided"
        return SystemMessage(content=SYSTEM_PROMPT.format(employee_id=logged_in))

    @traceable(name="nova_hr_turn", run_type="chain")
    def stream_reply(
        self,
        user_text: str,
        session_id: str,
        employee_id: str = "",
    ) -> Iterator[str]:
        history = self._history(session_id)
        history.append(HumanMessage(content=_content_to_text(user_text).strip()))

        for _round in range(MAX_TOOL_ROUNDS):
            messages = [self._system_message(employee_id), *history]
            assembled: AIMessage | None = None
            visible = ""

            for chunk in self.llm_with_tools.stream(messages):
                assembled = chunk if assembled is None else assembled + chunk
                if assembled.tool_calls:
                    continue
                piece = _content_to_text(chunk.content)
                if piece:
                    visible += piece
                    yield visible

            if assembled is None:
                fallback = "I could not generate a response. Please try again."
                history.append(AIMessage(content=fallback))
                yield fallback
                return

            history.append(assembled)

            if not assembled.tool_calls:
                if not visible:
                    visible = _content_to_text(assembled.content) or (
                        "I do not have a complete answer for that yet."
                    )
                    yield visible
                return

            tool_names = ", ".join(
                call.get("name", "unknown") for call in assembled.tool_calls
            )
            yield f"🔧 *Using HR tools: {tool_names}...*"

            for call in assembled.tool_calls:
                name = call.get("name") or ""
                args = call.get("args") or {}
                tool_call_id = call.get("id") or f"call_{uuid4().hex[:8]}"
                result = execute_hr_tool(name, args)
                history.append(
                    ToolMessage(
                        content=result,
                        tool_call_id=tool_call_id,
                        name=name or "invalid_tool",
                    )
                )

        limit_msg = (
            "I needed too many tool calls to finish that request. "
            "Please rephrase or split the question."
        )
        history.append(AIMessage(content=limit_msg))
        yield limit_msg


def get_directory_markdown() -> str:
    rows = [
        f"| {row['employee_id']} | {row['name']} | {row['department']} | {row['role']} |"
        for row in list_employee_directory()
    ]
    header = (
        "| ID | Name | Department | Role |\n"
        "|---|---|---|---|\n"
    )
    return header + "\n".join(rows)
