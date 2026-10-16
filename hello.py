"""Send one message to Claude and print the reply."""

import anthropic
from dotenv import load_dotenv

MODEL = "claude-opus-5-5"


def main():
    # Copy the variables from .env into this program's environment.
    load_dotenv()

    # The client finds ANTHROPIC_API_KEY in the environment on its own.
    client = anthropic.Anthropic()

    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": "Say hello in one short sentence."}],
        # If Claude declines for safety reasons, retry on a fallback model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )

    if response.stop_reason == "refusal":
        print("Claude declined to answer.")
        return

    # The reply is a list of blocks; print only the text ones.
    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
