# Claude Chatbot

A terminal chatbot that talks to Claude through the Anthropic API. It acts as a patient tutor for learning Python and AI engineering, streams its replies as they're written, and saves every conversation so you can pick it up later.

## Requirements

- Python 3.10 or newer (check with `python3 --version`)
- An Anthropic API key, which you can create in the [Claude Console](https://platform.claude.com/)

## Setup

**1. Get the code** and open a terminal in the project folder.

**2. Create a virtual environment and install the dependencies.** A virtual environment keeps this project's packages separate from the rest of your computer.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**3. Create your own `.env` file.** This file holds your API key. It is **not** included in the project, because every person needs to use their own key.

Copy the example file:

```bash
cp .env.example .env             # Windows: copy .env.example .env
```

Then open `.env` and replace `your-api-key-here` with your key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

The program reads the key from this file when it starts.

> ⚠️ **Keep your key secret.** Never commit `.env` to git, paste it into code, or share it. `.env` is already listed in `.gitignore`, so git ignores it. If a key ever leaks, delete it in the Claude Console and create a new one.

**4. Check that it works:**

```bash
python hello.py
```

You should see a short greeting from Claude.

## Usage

Start a new chat:

```bash
python chat.py
```

Continue your most recent chat:

```bash
python chat.py --continue
```

While chatting, you can type these commands. They are handled by the program and are never sent to Claude:

| Command   | What it does                                                  |
| --------- | ------------------------------------------------------------- |
| `/reset`  | Start a fresh conversation                                    |
| `/system` | Set a new system prompt and start a fresh conversation        |
| `quit`    | Exit (Ctrl+C or Ctrl+D also work)                             |

Each conversation is saved as a JSON file in the `chats/` folder, which git ignores. A chat is saved after each of Claude's replies.

## Running the tests

```bash
python -m pytest
```

## Project files

| File               | Purpose                                         |
| ------------------ | ----------------------------------------------- |
| `chat.py`          | The chatbot                                     |
| `hello.py`         | A minimal example: one message to Claude        |
| `test_chat.py`     | Tests for saving and loading chats              |
| `requirements.txt` | The Python packages this project needs          |
