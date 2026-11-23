import os
import anthropic
from app import Reply


class RealExpert:
    """Calls the provider through its official SDK. Timeout, retry and max_tokens are set here."""

    def __init__(self, model: str):
        self.model = model
        self.client = anthropic.Anthropic(            # reads ANTHROPIC_API_KEY from the environment
            base_url=os.getenv("ANTHROPIC_BASE_URL") or None,
            timeout=float(os.getenv("EXPERT_TIMEOUT", "20")),   # seconds, per attempt
            max_retries=int(os.getenv("EXPERT_RETRIES", "2")),  # SDK retries 408/409/429/5xx with backoff
        )

    def summarize(self, prompt: str) -> Reply:
        try:
            msg = self.client.messages.create(
                model=self.model,
                max_tokens=200,                       # cap on the answer: protects cost
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.APITimeoutError as e:
            raise TimeoutError(str(e)) from e
        text = "".join(b.text for b in msg.content if b.type == "text")
        return Reply(text, msg.usage.input_tokens, msg.usage.output_tokens)
