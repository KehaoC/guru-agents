# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI super employee for UA team, built with Claude Agent SDK as a CLI conversational agent.

## Development

```bash
# Install dependencies
uv sync

# Run the agent
uv run python src/main.py
```

## Architecture

- `src/main.py` - Main entry point, async REPL loop
- `src/prompt.py` - System prompt configuration
- `src/cli_tools.py` - Rich terminal formatting and message handling

Modify system prompt in `src/prompt.py`, change model in `src/main.py` `MODEL` variable.
