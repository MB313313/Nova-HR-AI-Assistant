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
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  min-width: 0;
  display: flex !important;
  flex-direction: column !important;
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

#sidebar-fixed {
  position: sticky;
  top: 0;
  z-index: 20;
  background: #171717 !important;
  padding-bottom: 8px;
  flex-shrink: 0;
}

#new-chat-btn {
  position: sticky;
  top: 0;
  z-index: 21;
  margin: 0 0 10px 0;
  padding: 0;
  background: #171717 !important;
}

#new-chat-btn button {
  background: #212121 !important;
  color: #ececec !important;
  border: 1px solid #3f3f3f !important;
  border-radius: 10px !important;
  font-weight: 500 !important;
  width: 100% !important;
  height: 40px !important;
  justify-content: flex-start !important;
  box-shadow: none !important;
}

#new-chat-btn button:hover {
  background: #2a2a2a !important;
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

#chats-section {
  gap: 0 !important;
  row-gap: 0 !important;
}

#chats-heading,
#chats-heading .prose,
#chats-heading .prose p,
#chats-heading .prose * {
  margin: 0 !important;
  padding: 0 !important;
}

#no-chats-yet,
#no-chats-yet .prose,
#no-chats-yet .prose p {
  margin: 0 !important;
  padding: 2px 4px 0 !important;
  color: #8e8ea0 !important;
  font-size: 0.86rem !important;
}

#chat-list,
#chat-list.block,
#sidebar #chat-list {
  --block-background-fill: transparent !important;
  --input-background-fill: transparent !important;
  --border-color-primary: transparent !important;
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
  max-height: none !important;
  overflow: visible !important;
  overflow-x: hidden !important;
  scrollbar-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

#chat-list::-webkit-scrollbar,
#chat-list *::-webkit-scrollbar {
  display: none !important;
  height: 0 !important;
  width: 0 !important;
}

#chat-list *,
#chat-list .wrap,
#chat-list .container,
#chat-list .block,
#chat-list .form,
#chat-list fieldset {
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
  overflow-x: hidden !important;
  scrollbar-width: none !important;
}

#chat-list .wrap,
#chat-list .form,
#chat-list fieldset,
#chat-list [class*="options"] {
  display: flex !important;
  flex-direction: column !important;
  flex-wrap: nowrap !important;
  gap: 2px !important;
  overflow: visible !important;
  overflow-x: hidden !important;
  padding: 0 !important;
}

#chat-list label,
#chat-list .form {
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
  background: transparent !important;
}

#chat-list input[type="radio"] {
  display: none !important;
}

#chat-list span,
#chat-list label > span,
#chat-list .wrap label,
#chat-list label {
  display: block !important;
  width: 100% !important;
  max-width: 100% !important;
  background: transparent !important;
  color: #cfcfcf !important;
  border: none !important;
  border-radius: 0 !important;
  font-size: 0.86rem !important;
  font-weight: 400 !important;
  padding: 2px 4px !important;
  cursor: pointer !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}

#chat-list label:hover span,
#chat-list .wrap label:hover,
#chat-list label:hover {
  background: transparent !important;
}

#chat-list input:checked + span,
#chat-list label:has(input:checked) span,
#chat-list label:has(input:checked) {
  background: transparent !important;
  color: #ececec !important;
  font-weight: 500 !important;
}

#main-col {
  background: #212121 !important;
  padding: 0 !important;
  min-height: 100vh;
  height: 100vh;
  display: flex !important;
  flex-direction: column !important;
}

#nova-chat {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  flex: 1 1 auto !important;
  min-height: 0 !important;
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
  flex-shrink: 0;
  position: sticky;
  bottom: 0;
  z-index: 15;
  width: 100%;
  max-width: 768px;
  margin: 0 auto;
  padding: 8px 16px 14px;
  background: #212121 !important;
}

#composer-box {
  align-items: flex-end !important;
  gap: 8px !important;
  background: #2f2f2f !important;
  border: 1px solid #444 !important;
  border-radius: 28px !important;
  padding: 6px 6px 6px 16px !important;
  box-shadow: none !important;
}

#composer-box .form,
#composer-box .block,
#chat-input,
#chat-input .wrap,
#chat-input textarea,
#chat-input input {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

#chat-input textarea,
#chat-input input {
  color: #ececec !important;
  padding: 10px 4px !important;
  min-height: 36px !important;
  resize: none !important;
}

#send-btn {
  min-width: 36px !important;
  max-width: 36px !important;
  flex: 0 0 36px !important;
}

#send-btn button {
  width: 36px !important;
  height: 36px !important;
  min-width: 36px !important;
  padding: 0 !important;
  border-radius: 50% !important;
  background: #10a37f !important;
  color: #fff !important;
  border: none !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  justify-content: center !important;
  box-shadow: none !important;
}

#send-btn button:hover {
  background: #0e8f6e !important;
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

#demo-directory,
#demo-directory .wrap,
#demo-directory .styler {
  max-width: 100%;
  min-width: 0;
}

#demo-directory-table,
#demo-directory-table .prose,
#demo-directory .prose {
  overflow-x: auto !important;
  overflow-y: hidden !important;
  max-width: 100% !important;
  overscroll-behavior-x: contain;
  scrollbar-width: thin;
  scrollbar-color: #555 #1f1f1f;
}

#demo-directory-table .prose::-webkit-scrollbar,
#demo-directory .prose::-webkit-scrollbar {
  height: 8px;
}

#demo-directory-table .prose::-webkit-scrollbar-track,
#demo-directory .prose::-webkit-scrollbar-track {
  background: #1f1f1f;
  border-radius: 8px;
}

#demo-directory-table .prose::-webkit-scrollbar-thumb,
#demo-directory .prose::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 8px;
}

#demo-directory table {
  font-size: 0.72rem !important;
  color: #cfcfcf !important;
  width: max-content !important;
  min-width: 100%;
  border-collapse: collapse;
  table-layout: auto;
}

#demo-directory th,
#demo-directory td {
  white-space: nowrap !important;
  padding: 6px 10px !important;
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


def _init_store() -> dict[str, Any]:
    return {
        "chats": {},
        "order": [],
        "current": None,
    }


def _title_from(content: Any) -> str:
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or ""))
        text = "".join(parts)
    else:
        text = str(content or "")
    text = " ".join(text.split())
    if not text:
        return "New chat"
    if len(text) > 36:
        return text[:36].rstrip() + "…"
    return text


def _named_choices(store: dict[str, Any]) -> list[tuple[str, str]]:
    order = store.get("order") or []
    chats = store.get("chats") or {}
    choices: list[tuple[str, str]] = []
    for chat_id in order:
        chat = chats.get(chat_id)
        if not chat:
            continue
        title = chat.get("title") or "New chat"
        history = chat.get("history") or []
        if title == "New chat" and not history:
            continue
        choices.append((title, chat_id))
    return choices


def _radio_from_store(store: dict[str, Any]):
    choices = _named_choices(store)
    current = store.get("current")
    ids = {chat_id for _, chat_id in choices}
    value = current if current in ids else None
    return gr.Radio(
        choices=choices,
        value=value,
        container=False,
        show_label=False,
        elem_id="chat-list",
        visible=bool(choices),
    )


def _empty_hint(store: dict[str, Any]):
    return gr.update(visible=not _named_choices(store))


def _list_ui(store: dict[str, Any]):
    return _radio_from_store(store), _empty_hint(store)


def ensure_active_chat(store: dict[str, Any]) -> dict[str, Any]:
    store = _copy_store(store)
    current = store.get("current")
    chats = store["chats"]
    if current and current in chats:
        return store
    chat_id = ASSISTANT.new_session()
    chats[chat_id] = {"title": "New chat", "history": []}
    store["current"] = chat_id
    if chat_id not in store["order"]:
        store["order"] = store["order"] + [chat_id]
    return store


def _copy_store(store: dict[str, Any]) -> dict[str, Any]:
    chats = {
        chat_id: {
            "title": data.get("title", "New chat"),
            "history": list(data.get("history") or []),
        }
        for chat_id, data in (store.get("chats") or {}).items()
    }
    return {
        "chats": chats,
        "order": list(store.get("order") or []),
        "current": store.get("current"),
    }


def persist_chat(history: list[dict[str, Any]], store: dict[str, Any]):
    store = ensure_active_chat(store)
    current = store["current"]
    chats = store["chats"]
    chats[current]["history"] = list(history or [])
    if chats[current]["title"] == "New chat":
        for message in history or []:
            if message.get("role") == "user":
                chats[current]["title"] = _title_from(message.get("content"))
                break
    if current not in store["order"]:
        store["order"] = store["order"] + [current]
    return store, *_list_ui(store)


def new_chat(history: list[dict[str, Any]], store: dict[str, Any]):
    store = _copy_store(store)
    current = store["current"]
    chats = store["chats"]
    if current in chats:
        chats[current]["history"] = list(history or [])
    if current in chats and not history and chats[current]["title"] == "New chat":
        return [], store, *_list_ui(store), ""

    chat_id = ASSISTANT.new_session()
    chats[chat_id] = {"title": "New chat", "history": []}
    store["current"] = chat_id
    store["order"] = [item for item in store["order"] if item != chat_id] + [chat_id]
    return [], store, *_list_ui(store), ""


def start_turn(
    message: str, history: list[dict[str, str]], store: dict[str, Any]
):
    store = ensure_active_chat(store)
    cleared, history = user_submit(message, history)
    return cleared, history, store


def start_example(
    evt: gr.SelectData, history: list[dict[str, str]], store: dict[str, Any]
):
    store = ensure_active_chat(store)
    cleared, history = example_selected(evt, history)
    return cleared, history, store


def select_chat(
    selected_id: str, history: list[dict[str, Any]], store: dict[str, Any]
):
    store = _copy_store(store)
    if not selected_id or selected_id == store.get("current"):
        return history, store, ""
    current = store["current"]
    chats = store["chats"]
    if current in chats:
        chats[current]["history"] = list(history or [])
    if selected_id not in chats:
        return history, store, ""
    store["current"] = selected_id
    loaded = list(chats[selected_id].get("history") or [])
    return loaded, store, ""


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
    store: dict[str, Any],
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
    session_id = (store or {}).get("current") or ""
    history = history + [{"role": "assistant", "content": ""}]
    for partial in ASSISTANT.stream_reply(user_text, session_id, employee_id or ""):
        history[-1]["content"] = partial
        yield history


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
    store = gr.State(_init_store)
    employee_id = gr.State(parse_employee_choice(EMPLOYEE_CHOICES[0]))

    with gr.Row(elem_id="app-row", equal_height=True):
        with gr.Column(elem_id="sidebar", scale=0, min_width=268):
            with gr.Column(elem_id="sidebar-fixed"):
                gr.Markdown("# Nova HR", elem_id="brand-title")
                gr.Markdown(
                    f"HR assistant · {ASSISTANT.model_label}",
                    elem_id="brand-sub",
                )
                new_chat_btn = gr.Button("＋  New chat", elem_id="new-chat-btn")
                employee_dropdown = gr.Dropdown(
                    label="Signed in as",
                    choices=EMPLOYEE_CHOICES,
                    value=EMPLOYEE_CHOICES[0],
                    container=True,
                )
            with gr.Column(elem_id="chats-section"):
                gr.Markdown("**Chats**", elem_id="chats-heading")
                no_chats = gr.Markdown("No chat yet", elem_id="no-chats-yet")
                chat_list = gr.Radio(
                    choices=[],
                    value=None,
                    show_label=False,
                    container=False,
                    elem_id="chat-list",
                    visible=False,
                )
            with gr.Accordion("Demo directory", open=False, elem_id="demo-directory"):
                gr.Markdown(get_directory_markdown(), elem_id="demo-directory-table")

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
                with gr.Row(elem_id="composer-box"):
                    message = gr.Textbox(
                        show_label=False,
                        placeholder="Message Nova HR…",
                        container=False,
                        lines=1,
                        max_lines=6,
                        autofocus=True,
                        scale=1,
                        elem_id="chat-input",
                    )
                    send_btn = gr.Button("↑", elem_id="send-btn", scale=0, min_width=36)
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

    demo.load(lambda store: _list_ui(store), inputs=store, outputs=[chat_list, no_chats])

    send_event = message.submit(
        start_turn,
        inputs=[message, chatbot, store],
        outputs=[message, chatbot, store],
        **submit_kwargs,
    ).then(
        bot_respond,
        inputs=[chatbot, employee_id, store],
        outputs=chatbot,
        **submit_kwargs,
    ).then(
        persist_chat,
        inputs=[chatbot, store],
        outputs=[store, chat_list, no_chats],
        **submit_kwargs,
    )

    send_btn.click(
        start_turn,
        inputs=[message, chatbot, store],
        outputs=[message, chatbot, store],
        **submit_kwargs,
    ).then(
        bot_respond,
        inputs=[chatbot, employee_id, store],
        outputs=chatbot,
        **submit_kwargs,
    ).then(
        persist_chat,
        inputs=[chatbot, store],
        outputs=[store, chat_list, no_chats],
        **submit_kwargs,
    )

    chatbot.example_select(
        start_example,
        inputs=[chatbot, store],
        outputs=[message, chatbot, store],
        **submit_kwargs,
    ).then(
        bot_respond,
        inputs=[chatbot, employee_id, store],
        outputs=chatbot,
        **submit_kwargs,
    ).then(
        persist_chat,
        inputs=[chatbot, store],
        outputs=[store, chat_list, no_chats],
        **submit_kwargs,
    )

    new_chat_btn.click(
        new_chat,
        inputs=[chatbot, store],
        outputs=[chatbot, store, chat_list, no_chats, message],
        **submit_kwargs,
    )

    chat_list.change(
        select_chat,
        inputs=[chat_list, chatbot, store],
        outputs=[chatbot, store, message],
        **submit_kwargs,
    )

if __name__ == "__main__":
    demo.launch(
        theme=theme,
        css=CUSTOM_CSS,
        footer_links=[],
        css_paths=None,
    )
