"""A terminal chatbot that remembers the conversation. Type 'quit' to exit.

Each chat is saved to chats/. Run with --continue to pick up the latest one.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

MODEL = "claude-opus-5-5"
CHATS_DIR = Path(__file__).parent / "chats"
SYSTEM_PROMPT = """\
You are a patient tutor helping a beginner learn Python and AI engineering.

- Explain ideas in plain language and define jargon the first time you use it.
- Keep answers short: a few sentences, plus a small code example when it helps.
- When the user shares code with a bug, guide them to spot it before giving the fix.
- If you're not sure about something, say so instead of guessing.
"""


def stream_reply(client, history):
    """Send the conversation to Claude, print the reply as it arrives,
    and return the complete response once it's finished."""
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=history,
        # If Claude declines for safety reasons, retry on a fallback model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)  # flush = show it right away
        return stream.get_final_message()


def usage_summary(response):
    """Describe how many tokens this request used."""
    usage = response.usage
    return f"[tokens: {usage.input_tokens} in, {usage.output_tokens} out]"


def new_chat_path(chats_dir):
    """Return a fresh file path named after the current date and time."""
    return chats_dir / f"chat-{datetime.now():%Y-%m-%d_%H-%M-%S}.json"


def latest_chat_path(chats_dir):
    """Return the most recent saved chat, or None if there aren't any."""
    # The timestamp in each name sorts oldest to newest, so the last is newest.
    chats = sorted(chats_dir.glob("chat-*.json"))
    return chats[-1] if chats else None


def save_history(path, history):
    """Write the conversation to a JSON file."""
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(history, indent=2))


def load_history(path):
    """Read a conversation back from a JSON file."""
    return json.loads(path.read_text())


def pick_chat(continue_chat):
    """Return (path, history) for the latest chat, or for a new one."""
    if continue_chat:
        path = latest_chat_path(CHATS_DIR)
        if path:
            history = load_history(path)
            print(f"Continuing {path.name} ({len(history)} messages)\n")
            return path, history
        print("No saved chats yet, so starting a new one.\n")
    return new_chat_path(CHATS_DIR), []


def parse_args():
    parser = argparse.ArgumentParser(description="Chat with Claude.")
    parser.add_argument(
        "--continue",
        dest="continue_chat",  # "continue" is a Python keyword, so rename it
        action="store_true",
        help="pick up the most recent saved chat",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    load_dotenv()
    client = anthropic.Anthropic()
    chat_path, history = pick_chat(args.continue_chat)

    print("Chat with Claude! Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):  # Ctrl+D or Ctrl+C
            break

        if user_input.lower() == "quit":
            break
        if not user_input:
            continue  # ignore empty lines

        history.append({"role": "user", "content": user_input})
        print("Claude: ", end="", flush=True)
        response = stream_reply(client, history)
        print()  # end the streamed line

        if response.stop_reason == "refusal":
            history.pop()  # drop the declined message so the chat can go on
            print("(Claude declined to answer that one)\n")
            continue

        # Save Claude's full reply (not just the text) so the next request
        # sends the conversation back exactly as Claude wrote it. to_dict()
        # turns each SDK block into a plain dict that JSON can store.
        content = [block.to_dict() for block in response.content]
        history.append({"role": "assistant", "content": content})
        save_history(chat_path, history)
        print(f"{usage_summary(response)}\n")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
