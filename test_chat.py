"""Tests for saving and loading chats. Run with: pytest"""

from chat import latest_chat_path, load_history, save_history


def test_save_then_load_gives_same_history(tmp_path):
    history = [
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": [{"type": "text", "text": "Hello!"}]},
    ]
    path = tmp_path / "chats" / "chat-2026-10-16_09-00-00.json"

    save_history(path, history)

    assert load_history(path) == history


def test_latest_chat_path_picks_newest(tmp_path):
    for name in ["chat-2026-10-15_09-00-00.json", "chat-2026-10-16_09-00-00.json"]:
        save_history(tmp_path / name, [])

    assert latest_chat_path(tmp_path).name == "chat-2026-10-16_09-00-00.json"


def test_latest_chat_path_is_none_when_no_chats(tmp_path):
    assert latest_chat_path(tmp_path) is None
