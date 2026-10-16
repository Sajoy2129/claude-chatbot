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
        print("Claude: ", end="", flush=True)
        response = stream_reply(client, history)
        print()  # end the streamed line

        if response.stop_reason == "refusal":
            history.pop()  # drop the declined message so the chat can go on
            print("(Claude declined to answer that one)\n")
            continue

        # Save Claude's full reply (not just the text) so the next request
        # sends the conversation back exactly as Claude wrote it.
        history.append({"role": "assistant", "content": response.content})
        print(f"{usage_summary(response)}\n")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
