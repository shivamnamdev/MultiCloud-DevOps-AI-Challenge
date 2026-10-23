# SOP: Ollama link

## Goal
Confirm the app can reach a local Ollama server and that the required models answer a prompt. Everything LLM-related in the app goes through `tools/ollama_client.py`.

## Inputs
- `OLLAMA_URL` (default `http://localhost:11434`), `INTERVIEWER_MODEL` (default `llama3.2:latest`), `CODE_MODEL` (default `codellama:latest`). Read from environment / `.env`.

## Logic
1. `GET {url}/api/tags` -> `{"models":[{"name":"llama3.2:latest"}, ...]}`. Failure = Ollama not running or wrong URL.
2. Compare required model names to installed names. A required name without a tag (e.g. `llama3.2`) matches `llama3.2:latest`.
3. For each installed required model, `POST {url}/api/generate` with `{"model", "prompt", "stream": false}`; reply text is in `response`.
4. Print a pass/fail line per step. Exit code 0 only if every step passes.

## Edge cases
- Ollama absent: the app must keep working without LLM features; callers catch `OllamaError`.
- Model missing: report the exact fix, `ollama pull <model>`.
- Slow first call (model load): generous timeout (120 s) for generate, 5 s for tags.
- Network is stdlib `urllib` only, no extra dependencies.

## Testing
`tests/test_ollama_client.py` runs the client against a fake HTTP server that imitates `/api/tags` and `/api/generate`. Real verification: run `python3 tools/ollama_handshake.py` on a machine with Ollama.

## Learnings
- Always send the exact installed model name (from `/api/tags`) to `/api/generate`, not the name the user typed. Found by test `test_handshake_passes_when_all_present`.
