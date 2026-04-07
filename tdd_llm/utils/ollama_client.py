"""
Ollama client — wraps the local Ollama HTTP API.
"""

import json
import re
import random
import urllib.request
import urllib.error
from typing import Optional


OLLAMA_BASE_URL = "http://localhost:11434"


class OllamaClient:
    def __init__(self, model: str, base_url: str = OLLAMA_BASE_URL, api_key: Optional[str] = None):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def generate(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.2,
        seed: Optional[int] = None,
    ) -> str:
        options = {
            "temperature": temperature,
            "seed": seed if seed is not None else random.randint(0, 99999),
        }
        if "qwen3" in self.model.lower():
            options["think"] = False
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }
        if system:
            payload["system"] = system

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=data,
            headers=self._headers(),
        )
        timeout = 1200 if "deepseek-r1" in self.model.lower() else 600
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return body.get("response", "")
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise ConnectionError(
                    f"Authentication failed (HTTP 401). "
                    f"Pass your API key with --api_key or set OLLAMA_API_KEY env var."
                )
            raise ConnectionError(
                f"HTTP Error {e.code}: {e.reason} — {self.base_url}"
            )
        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Cannot reach Ollama at {self.base_url}. "
                f"Is Ollama running? Error: {e}"
            )
        except TimeoutError:
            raise ConnectionError(
                f"Request timed out after {timeout}s — model took too long to respond."
            )

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(
                f"{self.base_url}/api/tags",
                headers=self._headers(),
            )
            with urllib.request.urlopen(req, timeout=5):
                return True
        except urllib.error.HTTPError as e:
            # 401 means the server is reachable but needs auth — treat as available
            # so we don't skip authenticated cloud models
            return e.code == 401
        except Exception:
            return False

    def list_models(self) -> list[str]:
        req = urllib.request.Request(f"{self.base_url}/api/tags")
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return [m["name"] for m in body.get("models", [])]


def extract_python_code(text: str) -> str:
    """Extract the first Python fenced block, or the first def/class block."""
    match = re.search(r"```python\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Model output plain text: strip any prose before the first def/class
    match = re.search(r"^(def |class |import |from )", text, re.MULTILINE)
    if match:
        return text[match.start():].strip()
    return text.strip()
