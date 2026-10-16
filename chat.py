"""A terminal chatbot that remembers the conversation. Type 'quit' to exit."""

import anthropic
from dotenv import load_dotenv

MODEL = "claude-opus-5-5"
SYSTEM_PROMPT = """\
You are a patient tutor helping a beginner learn Python and AI engineering.

- Explain ideas in plain language and define jargon the first time you use it.
- Keep answers short: a few sentences, plus a small code example when it helps.
- When the user shares code with a bug, guide them to spot it before giving the fix.
- If you're not sure about something, say so instead of guessing.
"""


def ask_claude(client, history):
    """Send the full conversation history to Claude and return the response."""
    return client.beta.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=history,
        # If Claude declines for safety reasons, retry on a fallback model.he
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )


def reply_text(response):
    """Join the text blocks of a response into one string."""
    return "".join(block.text for block in response.content if block.type == "text")


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    history = []  # every message so far, oldest first

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
        response = ask_claude(client, history)

        if response.stop_reason == "refusal":
            history.pop()  # drop the declined message so the chat can go on
            print("Claude: (declined to answer that one)\n")
            continue

        # Save Claude's full reply (not just the text) so the next request
        # sends the conversation back exactly as Claude wrote it.
        history.append({"role": "assistant", "content": response.content})
        print(f"Claude: {reply_text(response)}\n")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
