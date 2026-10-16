"""Tests for saving and loading chats. Run with: pytest"""

import json

from chat import SYSTEM_PROMPT, latest_chat_path, load_chat, save_chat


def test_save_then_load_gives_same_chat(tmp_path):
    history = [
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": [{"type": "text", "text": "Hello!"}]},
    ]
    path = tmp_path / "chats" / "chat-2026-10-16_09-00-00.json"

    save_chat(path, "You are a pirate.", history)

    assert load_chat(path) == ("You are a pirate.", history)


def test_old_chat_files_load_with_default_prompt(tmp_path):
    # Before /system existed, files held only the list of messages.
    history = [{"role": "user", "content": "Hi!"}]
    path = tmp_path / "chat-2026-10-15_09-00-00.json"
    path.write_text(json.dumps(history))

    assert load_chat(path) == (SYSTEM_PROMPT, history)


def test_latest_chat_path_picks_newest(tmp_path):
    for name in ["chat-2026-10-15_09-00-00.json", "chat-2026-10-16_09-00-00.json"]:
        save_chat(tmp_path / name, SYSTEM_PROMPT, [])

    assert latest_chat_path(tmp_path).name == "chat-2026-10-16_09-00-00.json"


def test_latest_chat_path_is_none_when_no_chats(tmp_path):
    assert latest_chat_path(tmp_path) is None
