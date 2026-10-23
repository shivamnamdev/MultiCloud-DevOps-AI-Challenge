"""Verify Ollama is reachable and the required models answer. Run on a machine with Ollama.

    python3 tools/ollama_handshake.py [--url URL] [--model NAME ...]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ollama_client import (DEFAULT_CODE_MODEL, DEFAULT_INTERVIEWER_MODEL,  # noqa: E402
                           OllamaClient, OllamaError, load_env, model_matches)


def main(argv=None) -> int:
    load_env()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default=None)
    p.add_argument("--model", action="append", help="required model (repeatable)")
    args = p.parse_args(argv)

    required = args.model or [
        os.environ.get("INTERVIEWER_MODEL", DEFAULT_INTERVIEWER_MODEL),
        os.environ.get("CODE_MODEL", DEFAULT_CODE_MODEL),
    ]
    client = OllamaClient(args.url)
    ok = True

    try:
        installed = client.list_models()
    except OllamaError as e:
        print("FAIL  server: %s" % e)
        print("      Is Ollama running? Try: ollama serve")
        return 1
    print("PASS  server: %s (%d models installed)" % (client.base_url, len(installed)))

    for model in required:
        match = next((i for i in installed if model_matches(model, i)), None)
        if match is None:
            print("FAIL  model %s: not installed. Fix: ollama pull %s" % (model, model))
            ok = False
            continue
        try:
            reply = client.generate(match, "Reply with the single word: ready")
            print("PASS  model %s: replied %r" % (match, reply.strip()[:40]))
        except OllamaError as e:
            print("FAIL  model %s: %s" % (model, e))
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
