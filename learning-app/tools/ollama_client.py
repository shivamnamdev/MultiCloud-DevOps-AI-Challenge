"""Minimal Ollama HTTP client (stdlib only). See architecture/ollama_link.md."""
import json
import os
import urllib.error
import urllib.request
from typing import List, Optional

DEFAULT_URL = "http://localhost:11434"
DEFAULT_INTERVIEWER_MODEL = "llama3.2:latest"
DEFAULT_CODE_MODEL = "codellama:latest"


class OllamaError(Exception):
    pass


def load_env(path: str = ".env") -> None:
    """Load KEY=VALUE lines into os.environ without overriding existing values."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def model_matches(required: str, installed: str) -> bool:
    """`llama3.2` matches `llama3.2:latest`; an explicit tag must match exactly."""
    if ":" not in required:
        required += ":latest"
    return required == installed


class OllamaClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("OLLAMA_URL") or DEFAULT_URL).rstrip("/")

    def _request(self, path: str, payload: Optional[dict], timeout: float) -> dict:
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            self.base_url + path,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST" if payload is not None else "GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise OllamaError("HTTP %s from %s%s: %s" % (e.code, self.base_url, path, e.read().decode(errors="replace")[:200]))
        except (urllib.error.URLError, OSError, ValueError) as e:
            raise OllamaError("Cannot reach Ollama at %s (%s)" % (self.base_url, e))

    def list_models(self) -> List[str]:
        return [m["name"] for m in self._request("/api/tags", None, 5).get("models", [])]

    def generate(self, model: str, prompt: str, timeout: float = 120) -> str:
        out = self._request("/api/generate", {"model": model, "prompt": prompt, "stream": False}, timeout)
        if "response" not in out:
            raise OllamaError("Unexpected reply from /api/generate: %r" % (out,))
        return out["response"]
