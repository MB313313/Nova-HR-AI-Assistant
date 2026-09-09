"""Gradio chatbot for Nova HR — ChatGPT-style UI."""

from __future__ import annotations

from typing import Any

import gradio as gr

from assistant import HRAssistant, get_directory_markdown
from tools import EMPLOYEES

EXAMPLES = [
    "What is my remaining leave balance?",
    "What are the company policies on remote work?",
    "Can you retrieve my employee details?",
    "Generate some interview questions for a Data Scientist.",
    "What is the salary review process?",
    "What is the dress code in the office?",
]

EXAMPLE_CARDS = [
    {
        "text": "What is my remaining leave balance?",
        "display_text": "Check my leave balance",
    },
    {
        "text": "What are the company policies on remote work?",
        "display_text": "Remote work policy",
    },
    {
        "text": "Can you retrieve my employee details?",
        "display_text": "My employee details",
    },
    {
        "text": "Generate some interview questions for a Data Scientist.",
        "display_text": "Data Scientist interviews",
    },
]

SIDEBAR_PROMPTS = [
    ("Leave balance", EXAMPLES[0]),
    ("Remote work", EXAMPLES[1]),
    ("My details", EXAMPLES[2]),
    ("Interview pack", EXAMPLES[3]),
    ("Salary review", EXAMPLES[4]),
    ("Dress code", EXAMPLES[5]),
]

CUSTOM_CSS = """
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");

:root, .dark, body, gradio-app {
  color-scheme: dark;
}

html, body {
  height: 100%;
  background: #212121 !important;
}

.gradio-container {
  max-width: 100% !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif !important;
  background: #212121 !important;
  min-height: 100vh;
}

.gradio-container .contain,
.gradio-container .main,
.fillable {
  padding: 0 !important;
  max-width: 100% !important;
}

footer, .footer, .svelte-1ipelgc {
  display: none !important;
}

#app-row {
  min-height: 100vh;
  align-items: stretch !important;
  gap: 0 !important;
}

#sidebar {
  background: #171717 !important;
  border-right: 1px solid #2e2e2e !important;
  padding: 14px 12px 18px !important;
  min-height: 100vh;
}

#sidebar .prose,
#sidebar .prose * {
  color: #ececec !important;
}

#sidebar .prose h1,
#brand-title h1,
#brand-title .prose h1 {
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  letter-spacing: -0.02em;
  margin: 0 !important;
}

#brand-sub .prose,
#brand-sub .prose p {
  color: #8e8ea0 !important;
  font-size: 0.78rem !important;
  margin: 2px 0 12px !important;
}

#sidebar .gr-button,
#sidebar button {
  border-radius: 10px !important;
  justify-content: flex-start !important;
  text-align: left !important;
}

#new-chat-btn {
  margin-bottom: 8px;
}

#new-chat-btn button {
  background: #2f2f2f !important;
  color: #ececec !important;
  border: 1px solid #3f3f3f !important;
  font-weight: 500 !important;
  width: 100%;
  height: 40px !important;
}

#new-chat-btn button:hover {
  background: #3a3a3a !important;
}

#sidebar .prompt-btn button {
  background: transparent !important;
  color: #cfcfcf !important;
  border: none !important;
  box-shadow: none !important;
  font-size: 0.86rem !important;
  padding: 8px 10px !important;
  width: 100%;
}

#sidebar .prompt-btn button:hover {
  background: #2a2a2a !important;
}

#main-col {
  background: #212121 !important;
  padding: 0 0 12px !important;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

#nova-chat {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

#nova-chat .wrapper,
#nova-chat .bubble-wrap,
#nova-chat [class*="bubble-wrap"] {
  background: transparent !important;
}

#nova-chat .message,
#nova-chat [class*="message"] {
  font-size: 0.98rem !important;
  line-height: 1.7 !important;
}

#composer {
  max-width: 768px;
  margin: 0 auto;
  width: 100%;
  padding: 0 16px;
}

#composer textarea,
#composer input {
  background: #2f2f2f !important;
  color: #ececec !important;
  border: 1px solid #444 !important;
  border-radius: 26px !important;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.02) !important;
}

#disclaimer .prose,
#disclaimer .prose p {
  color: #8e8ea0 !important;
  font-size: 0.72rem !important;
  text-align: center !important;
  margin: 8px 0 0 !important;
}

.nova-empty {
  text-align: center;
  padding: 24px 16px 8px;
}

.nova-orb {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: 700;
  font-size: 1.35rem;
  color: #fff;
  background: linear-gradient(180deg, #10a37f 0%, #0e8c6d 100%);
  box-shadow: 0 8px 24px rgba(16, 163, 127, 0.28);
}

.nova-empty h1 {
  font-size: 1.85rem !important;
  font-weight: 600 !important;
  color: #ececec !important;
  margin: 0 !important;
}

#nova-chat .placeholder,
#nova-chat .empty,
#nova-chat [class*="placeholder"] {
  color: #ececec !important;
}

label, .block-label, .label-wrap {
  color: #a1a1aa !important;
  font-size: 0.75rem !important;
}

.accordion {
  background: transparent !important;
  border: 1px solid #2e2e2e !important;
  border-radius: 10px !important;
}

#sidebar table {
  font-size: 0.72rem !important;
  color: #cfcfcf !important;
}
"""

EMPTY_PLACEHOLDER = """
<div class="nova-empty">
  <div class="nova-orb">N</div>
  <h1>How can I help you today?</h1>
</div>
"""


def _build_assistant() -> HRAssistant:
    try:
        return HRAssistant()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"{exc}\n\nCopy .env.example to .env and add OPENAI_API_KEY or GOOGLE_API_KEY."
        ) from exc


ASSISTANT = _build_assistant()


def _init_session() -> str:
    return ASSISTANT.new_session()


def user_submit(
    message: str, history: list[dict[str, str]]
) -> tuple[str, list[dict[str, str]]]:
    text = (message or "").strip()
    if not text:
        return "", history
    history = history + [{"role": "user", "content": text}]
    return "", history


def bot_respond(
    history: list[dict[str, Any]],
    employee_id: str,
    session_id: str,
):
    if not history:
        yield history
        return

    user_text = history[-1]["content"]
    if isinstance(user_text, list):
        parts = []
        for item in user_text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or ""))
        user_text = "".join(parts)
    history = history + [{"role": "assistant", "content": ""}]
    for partial in ASSISTANT.stream_reply(user_text, session_id, employee_id or ""):
        history[-1]["content"] = partial
        yield history


def clear_chat(session_id: str) -> tuple[list, str, str]:
    return [], ASSISTANT.clear_session(session_id), ""


def example_selected(
    evt: gr.SelectData, history: list[dict[str, str]]
) -> tuple[str, list[dict[str, str]]]:
    value = evt.value
    if isinstance(value, dict):
        text = str(value.get("text") or value.get("display_text") or "")
    else:
        text = str(value or "")
    return user_submit(text, history)


EMPLOYEE_CHOICES = [
    f"{emp['employee_id']} — {emp['name']}" for emp in EMPLOYEES.values()
]


def parse_employee_choice(choice: str) -> str:
    if not choice:
        return ""
    return choice.split(" — ", 1)[0].strip()


theme = gr.themes.Default(
    primary_hue="emerald",
    secondary_hue="zinc",
    neutral_hue="zinc",
    font=gr.themes.GoogleFont("Inter"),
    radius_size=gr.themes.sizes.radius_lg,
).set(
    body_background_fill="#212121",
    body_background_fill_dark="#212121",
    body_text_color="#ececec",
    body_text_color_dark="#ececec",
    background_fill_primary="#212121",
    background_fill_primary_dark="#212121",
    background_fill_secondary="#171717",
    background_fill_secondary_dark="#171717",
    block_background_fill="#212121",
    block_background_fill_dark="#212121",
    block_border_width="0px",
    block_shadow="none",
    border_color_primary="#2e2e2e",
    border_color_accent="#10a37f",
    input_background_fill="#2f2f2f",
    input_background_fill_dark="#2f2f2f",
    input_border_color="#444444",
    input_border_color_dark="#444444",
    input_placeholder_color="#8e8ea0",
    button_primary_background_fill="#10a37f",
    button_primary_background_fill_hover="#0e8f6e",
    button_primary_text_color="#ffffff",
    button_secondary_background_fill="#2f2f2f",
    button_secondary_background_fill_hover="#3d3d3d",
    button_secondary_text_color="#ececec",
    button_secondary_text_color_dark="#ececec",
    link_text_color="#10a37f",
)

with gr.Blocks(title="Nova HR", fill_height=True, fill_width=True) as demo:
    session_id = gr.State(_init_session)
    employee_id = gr.State(parse_employee_choice(EMPLOYEE_CHOICES[0]))

    with gr.Row(elem_id="app-row", equal_height=True):
        with gr.Column(elem_id="sidebar", scale=0, min_width=268):
            gr.Markdown("# Nova HR", elem_id="brand-title")
            gr.Markdown(
                f"HR assistant · {ASSISTANT.model_label}",
                elem_id="brand-sub",
            )
            new_chat = gr.Button("＋  New chat", elem_id="new-chat-btn")
            employee_dropdown = gr.Dropdown(
                label="Signed in as",
                choices=EMPLOYEE_CHOICES,
                value=EMPLOYEE_CHOICES[0],
                container=True,
            )
            gr.Markdown("**Chats**")
            sidebar_buttons = []
            for label, _prompt in SIDEBAR_PROMPTS:
                sidebar_buttons.append(
                    gr.Button(label, elem_classes=["prompt-btn"], size="sm")
                )
            with gr.Accordion("Demo directory", open=False):
                gr.Markdown(get_directory_markdown())

        with gr.Column(elem_id="main-col", scale=1):
            chatbot = gr.Chatbot(
                elem_id="nova-chat",
                show_label=False,
                container=False,
                scale=1,
                layout="bubble",
                buttons=["copy"],
                feedback_options=[],
                placeholder=EMPTY_PLACEHOLDER,
                examples=EXAMPLE_CARDS,
                sanitize_html=False,
            )
            with gr.Column(elem_id="composer"):
                message = gr.Textbox(
                    show_label=False,
                    placeholder="Message Nova HR…",
                    submit_btn=True,
                    container=False,
                    lines=1,
                    max_lines=6,
                    autofocus=True,
                )
                gr.Markdown(
                    "Nova HR can make mistakes. Check leave and policy answers against HR.",
                    elem_id="disclaimer",
                )

    def on_employee_change(choice: str) -> str:
        return parse_employee_choice(choice)

    employee_dropdown.change(
        on_employee_change,
        inputs=employee_dropdown,
        outputs=employee_id,
    )

    submit_kwargs = dict(show_progress="hidden")

    message.submit(
        user_submit,
        inputs=[message, chatbot],
        outputs=[message, chatbot],
        **submit_kwargs,
    ).then(
        bot_respond,
        inputs=[chatbot, employee_id, session_id],
        outputs=chatbot,
        **submit_kwargs,
    )

    chatbot.example_select(
        example_selected,
        inputs=chatbot,
        outputs=[message, chatbot],
        **submit_kwargs,
    ).then(
        bot_respond,
        inputs=[chatbot, employee_id, session_id],
        outputs=chatbot,
        **submit_kwargs,
    )

    new_chat.click(
        clear_chat,
        inputs=session_id,
        outputs=[chatbot, session_id, message],
        **submit_kwargs,
    )

    for button, (_label, prompt) in zip(sidebar_buttons, SIDEBAR_PROMPTS):

        def _make_handler(text: str):
            def _handler(history):
                return user_submit(text, history)

            return _handler

        button.click(
            _make_handler(prompt),
            inputs=chatbot,
            outputs=[message, chatbot],
            **submit_kwargs,
        ).then(
            bot_respond,
            inputs=[chatbot, employee_id, session_id],
            outputs=chatbot,
            **submit_kwargs,
        )

if __name__ == "__main__":
    demo.launch(
        theme=theme,
        css=CUSTOM_CSS,
        footer_links=[],
        css_paths=None,
    )
