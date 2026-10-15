# CLAUDE.md

## Security rules
- Never read, print, or ask for the `.env` file or any API key.
- Load secrets in code via environment variables (e.g. `os.getenv("ANTHROPIC_API_KEY")`), never hard-code them.
