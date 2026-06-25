#!/usr/bin/env python3
"""OpenAI-compatible proxy that strips empty leading Qwen think wrappers.

This is a Hermes integration helper. It preserves strict benchmark semantics:
the benchmark still scores raw model output, while this proxy normalizes only
empty leading ``<think></think>`` wrappers before an application parser sees the
assistant message.
"""
from __future__ import annotations

import argparse
import json
import threading
import urllib.error
import urllib.request
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urljoin

import requests

from normalize_tool_response import strip_empty_think_prefix


HOP_BY_HOP_HEADERS = {
    "connection",
    "content-encoding",
    "content-length",
    "host",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}


def normalize_chat_completion_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Normalize assistant message content in a chat completion payload."""
    normalized_count = 0
    choices = payload.get("choices")
    if not isinstance(choices, list):
        return payload, normalized_count

    for choice in choices:
        if not isinstance(choice, dict):
            continue
        message = choice.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if not isinstance(content, str):
            continue
        normalized = strip_empty_think_prefix(content)
        if normalized != content.strip():
            message["content"] = normalized
            normalized_count += 1
    return payload, normalized_count


def extract_first_tool_call_block(text: str) -> str:
    """Return the first complete tool-call XML block from text, or an empty string."""
    start = text.find("<tool_call>")
    if start < 0:
        return ""
    end = text.find("</tool_call>", start)
    if end < 0:
        return ""
    end += len("</tool_call>")
    return text[start:end].strip()


def promote_chat_reasoning_tool_call_content(payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Promote a tool call from chat reasoning_content into scored message content."""
    promoted_count = 0
    choices = payload.get("choices")
    if not isinstance(choices, list):
        return payload, promoted_count

    for choice in choices:
        if not isinstance(choice, dict):
            continue
        message = choice.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if isinstance(content, str) and "<tool_call>" in content:
            continue
        reasoning = message.get("reasoning_content")
        if not isinstance(reasoning, str):
            continue
        tool_call = extract_first_tool_call_block(reasoning)
        if not tool_call:
            continue
        message["content"] = tool_call
        promoted_count += 1
    return payload, promoted_count


def coerce_mlx_logprobs_request(payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Coerce OpenAI-style integer logprobs to mlx_lm.server's boolean shape."""
    if "logprobs" not in payload or isinstance(payload.get("logprobs"), bool):
        return payload, 0
    if isinstance(payload.get("logprobs"), int):
        updated = dict(payload)
        updated["logprobs"] = bool(payload["logprobs"])
        return updated, 1
    return payload, 0


def override_request_model(payload: dict[str, Any], model_override: str) -> tuple[dict[str, Any], int]:
    """Replace the request model id before forwarding to a local runtime."""
    if not model_override or not isinstance(payload.get("model"), str):
        return payload, 0
    if payload["model"] == model_override:
        return payload, 0
    updated = dict(payload)
    updated["model"] = model_override
    return updated, 1


def add_completions_prompt_suffix(payload: dict[str, Any], suffix: str) -> tuple[dict[str, Any], int]:
    """Append a generation-only suffix to OpenAI completions prompts."""
    if not suffix or "prompt" not in payload:
        return payload, 0

    def update_prompt(prompt: Any) -> tuple[Any, int]:
        if isinstance(prompt, str) and not prompt.endswith(suffix):
            return prompt + suffix, 1
        if isinstance(prompt, list):
            changed = 0
            updated: list[Any] = []
            for item in prompt:
                if isinstance(item, str) and not item.endswith(suffix):
                    updated.append(item + suffix)
                    changed += 1
                else:
                    updated.append(item)
            return updated, changed
        return prompt, 0

    updated_prompt, changed_count = update_prompt(payload.get("prompt"))
    if not changed_count:
        return payload, 0
    updated = dict(payload)
    updated["prompt"] = updated_prompt
    return updated, changed_count


def cap_completions_max_tokens(payload: dict[str, Any], max_tokens_cap: int) -> tuple[dict[str, Any], int]:
    """Cap runaway completion requests for local runtimes when explicitly enabled."""
    if max_tokens_cap <= 0:
        return payload, 0
    max_tokens = payload.get("max_tokens")
    if not isinstance(max_tokens, int) or max_tokens <= max_tokens_cap:
        return payload, 0
    updated = dict(payload)
    updated["max_tokens"] = max_tokens_cap
    return updated, 1


def normalize_completions_reasoning_content(payload: dict[str, Any], prefix: str) -> tuple[dict[str, Any], int]:
    """Move non-empty reasoning_content into blank completions text fields."""
    choices = payload.get("choices")
    if not isinstance(choices, list):
        return payload, 0
    updated_count = 0
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        text = choice.get("text")
        reasoning = choice.get("reasoning_content")
        if isinstance(text, str) and text.strip():
            continue
        if not isinstance(reasoning, str) or not reasoning.strip():
            continue
        choice["text"] = prefix + reasoning
        updated_count += 1
    return payload, updated_count


def promote_completions_reasoning_tool_call_text(payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Promote a complete completions reasoning_content tool call into scored text."""
    choices = payload.get("choices")
    if not isinstance(choices, list):
        return payload, 0
    updated_count = 0
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        text = choice.get("text")
        if isinstance(text, str) and "<tool_call>" in text and "</tool_call>" in text:
            continue
        reasoning = choice.get("reasoning_content")
        if not isinstance(reasoning, str):
            continue
        tool_call = extract_first_tool_call_block(reasoning)
        if not tool_call:
            continue
        choice["text"] = tool_call
        updated_count += 1
    return payload, updated_count


def prefix_completions_text(payload: dict[str, Any], prefix: str) -> tuple[dict[str, Any], int]:
    """Prepend a prefix to non-empty completions text fields when missing."""
    if not prefix:
        return payload, 0
    choices = payload.get("choices")
    if not isinstance(choices, list):
        return payload, 0
    updated_count = 0
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        text = choice.get("text")
        if not isinstance(text, str) or not text.strip() or text.startswith(prefix):
            continue
        choice["text"] = prefix + text
        updated_count += 1
    return payload, updated_count


def upstream_url(upstream_base: str, request_path: str) -> str:
    """Map incoming OpenAI-compatible paths onto the upstream base URL."""
    route = request_path.split("?", 1)[0]
    if route.startswith("/v1/"):
        route = route[len("/v1/") :]
    else:
        route = route.lstrip("/")
    return urljoin(upstream_base.rstrip("/") + "/", route)


class NormalizingProxyHandler(BaseHTTPRequestHandler):
    server: "NormalizingProxyServer"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        if self.server.quiet:
            return
        super().log_message(format, *args)

    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] not in {"/v1/models", "/models", "/healthz"}:
            self.send_error(HTTPStatus.NOT_FOUND, "unsupported route")
            return
        if self.path.split("?", 1)[0] == "/healthz":
            self.send_json(HTTPStatus.OK, {"ok": True, "upstream": self.server.upstream_base})
            return
        self.proxy_request("GET")

    def do_POST(self) -> None:  # noqa: N802
        route = self.path.split("?", 1)[0]
        if route not in {"/v1/chat/completions", "/chat/completions", "/v1/completions", "/completions"}:
            self.send_error(HTTPStatus.NOT_FOUND, "unsupported route")
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b""
        try:
            request_payload = json.loads(body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "request body was not valid JSON")
            return
        if request_payload.get("stream") is True:
            self.send_error(HTTPStatus.BAD_REQUEST, "streaming responses are not normalized by this proxy")
            return
        request_payload, overridden_count = override_request_model(request_payload, self.server.model_override)
        body = json.dumps(request_payload).encode("utf-8")
        coerced_count = 0
        capped_max_tokens_count = 0
        if route in {"/v1/completions", "/completions"}:
            request_payload, coerced_count = coerce_mlx_logprobs_request(request_payload)
            request_payload, capped_max_tokens_count = cap_completions_max_tokens(
                request_payload,
                self.server.completion_max_tokens_cap,
            )
            request_payload, suffixed_count = add_completions_prompt_suffix(
                request_payload,
                self.server.completion_prompt_suffix,
            )
            self.server.last_completion_prompt_suffix_count += suffixed_count
            body = json.dumps(request_payload).encode("utf-8")
        self.proxy_request(
            "POST",
            body,
            coerced_logprobs_count=coerced_count,
            overridden_model_count=overridden_count,
            capped_max_tokens_count=capped_max_tokens_count,
        )

    def proxy_request(
        self,
        method: str,
        body: bytes | None = None,
        coerced_logprobs_count: int = 0,
        overridden_model_count: int = 0,
        capped_max_tokens_count: int = 0,
    ) -> None:
        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in HOP_BY_HOP_HEADERS
        }
        target = upstream_url(self.server.upstream_base, self.path)
        try:
            response = requests.request(
                method,
                target,
                data=body,
                headers=headers,
                timeout=self.server.timeout_s,
            )
        except requests.RequestException as exc:
            self.send_error(HTTPStatus.BAD_GATEWAY, f"upstream request failed: {exc}")
            return

        content = response.content
        normalized_count = 0
        chat_reasoning_tool_call_count = 0
        reasoning_text_count = 0
        completion_reasoning_tool_call_count = 0
        text_prefix_count = 0
        content_type = response.headers.get("Content-Type", "")
        if (
            self.path.split("?", 1)[0] in {"/v1/chat/completions", "/chat/completions"}
            and "json" in content_type.lower()
            and content
        ):
            try:
                payload = response.json()
                if isinstance(payload, dict):
                    payload, normalized_count = normalize_chat_completion_payload(payload)
                    if self.server.chat_reasoning_tool_call_content:
                        payload, chat_reasoning_tool_call_count = promote_chat_reasoning_tool_call_content(payload)
                    content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            except ValueError:
                pass
        if (
            self.path.split("?", 1)[0] in {"/v1/completions", "/completions"}
            and (self.server.completion_reasoning_prefix or self.server.completion_text_prefix)
            and "json" in content_type.lower()
            and content
        ):
            try:
                payload = response.json()
                if isinstance(payload, dict):
                    payload, reasoning_text_count = normalize_completions_reasoning_content(
                        payload,
                        self.server.completion_reasoning_prefix,
                    )
                    if self.server.completion_reasoning_tool_call_text:
                        payload, completion_reasoning_tool_call_count = promote_completions_reasoning_tool_call_text(
                            payload
                        )
                    payload, text_prefix_count = prefix_completions_text(
                        payload,
                        self.server.completion_text_prefix,
                    )
                    content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            except ValueError:
                pass

        self.send_response(response.status_code)
        for key, value in response.headers.items():
            if key.lower() not in HOP_BY_HOP_HEADERS:
                self.send_header(key, value)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Hermes-Normalized-Empty-Think-Count", str(normalized_count))
        self.send_header("X-Hermes-Chat-Reasoning-Tool-Call-Content-Count", str(chat_reasoning_tool_call_count))
        self.send_header("X-Hermes-Coerced-Logprobs-Count", str(coerced_logprobs_count))
        self.send_header("X-Hermes-Overridden-Model-Count", str(overridden_model_count))
        self.send_header("X-Hermes-Capped-Max-Tokens-Count", str(capped_max_tokens_count))
        self.send_header("X-Hermes-Completion-Prompt-Suffix-Count", str(self.server.last_completion_prompt_suffix_count))
        self.send_header("X-Hermes-Completion-Reasoning-Text-Count", str(reasoning_text_count))
        self.send_header(
            "X-Hermes-Completion-Reasoning-Tool-Call-Text-Count",
            str(completion_reasoning_tool_call_count),
        )
        self.send_header("X-Hermes-Completion-Text-Prefix-Count", str(text_prefix_count))
        self.server.last_completion_prompt_suffix_count = 0
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        content = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


class NormalizingProxyServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        upstream_base: str,
        timeout_s: float,
        quiet: bool,
        model_override: str = "",
        completion_prompt_suffix: str = "",
        completion_reasoning_prefix: str = "",
        completion_text_prefix: str = "",
        completion_max_tokens_cap: int = 0,
        completion_reasoning_tool_call_text: bool = False,
        chat_reasoning_tool_call_content: bool = False,
    ) -> None:
        super().__init__(server_address, NormalizingProxyHandler)
        self.upstream_base = upstream_base
        self.timeout_s = timeout_s
        self.quiet = quiet
        self.model_override = model_override
        self.completion_prompt_suffix = completion_prompt_suffix
        self.completion_reasoning_prefix = completion_reasoning_prefix
        self.completion_text_prefix = completion_text_prefix
        self.completion_max_tokens_cap = completion_max_tokens_cap
        self.completion_reasoning_tool_call_text = completion_reasoning_tool_call_text
        self.chat_reasoning_tool_call_content = chat_reasoning_tool_call_content
        self.last_completion_prompt_suffix_count = 0


class SelfTestUpstreamHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/v1/models":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.send_payload({"data": [{"id": "qwen-test"}]})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/v1/completions":
            length = int(self.headers.get("Content-Length", "0"))
            request_payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(request_payload.get("logprobs"), bool):
                self.send_payload({"error": "logprobs must be boolean"}, status=HTTPStatus.BAD_REQUEST)
                return
            if isinstance(request_payload.get("prompt"), str) and "blank reasoning" in str(request_payload["prompt"]):
                self.send_payload(
                    {
                        "choices": [
                            {
                                "text": "",
                                "reasoning_content": "{\"name\":\"demo.tool\",\"arguments\":{}}\n</tool_call>",
                            }
                        ]
                    }
                )
                return
            if isinstance(request_payload.get("prompt"), str) and "prose reasoning tool call" in str(
                request_payload["prompt"]
            ):
                self.send_payload(
                    {
                        "choices": [
                            {
                                "text": "The requested action is complete.",
                                "reasoning_content": '<tool_call>\n{"name":"demo.tool","arguments":{}}\n</tool_call>',
                            }
                        ]
                    }
                )
                return
            self.send_payload(
                {
                    "choices": [
                        {
                            "text": " Paris",
                            "logprobs": {
                                "tokens": [" Paris"],
                                "token_logprobs": [-0.01],
                                "top_logprobs": [{" Paris": -0.01}],
                                "text_offset": [0],
                            },
                        }
                    ]
                }
            )
            return
        if self.path != "/v1/chat/completions":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length", "0"))
        request_payload = json.loads(self.rfile.read(length).decode("utf-8"))
        if request_payload.get("stream") is True:
            self.send_payload({"error": "unexpected stream"}, status=HTTPStatus.BAD_REQUEST)
            return
        self.send_payload(
            {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "<think>\n\n</think>\n<tool_call>{}</tool_call>",
                        }
                    },
                    {
                        "message": {
                            "role": "assistant",
                            "content": "The answer is ready.",
                            "reasoning_content": "<tool_call>\n{\"name\":\"demo.tool\",\"arguments\":{}}\n</tool_call>\nDone.",
                        }
                    }
                ]
            }
        )

    def send_payload(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def start_threaded_server(server: ThreadingHTTPServer) -> threading.Thread:
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return thread


def run_self_test() -> None:
    upstream = ThreadingHTTPServer(("127.0.0.1", 0), SelfTestUpstreamHandler)
    upstream_thread = start_threaded_server(upstream)
    upstream_base = f"http://127.0.0.1:{upstream.server_port}/v1"

    proxy = NormalizingProxyServer(
        ("127.0.0.1", 0),
        upstream_base,
        timeout_s=5.0,
        quiet=True,
        model_override="qwen-override",
        completion_prompt_suffix="<think>\n\n</think>\n\n",
        completion_reasoning_prefix="<tool_call>\n",
        completion_text_prefix="",
        completion_max_tokens_cap=512,
        completion_reasoning_tool_call_text=True,
        chat_reasoning_tool_call_content=True,
    )
    proxy_thread = start_threaded_server(proxy)
    proxy_base = f"http://127.0.0.1:{proxy.server_port}/v1"

    try:
        with urllib.request.urlopen(f"{proxy_base}/models", timeout=5) as response:
            models = json.loads(response.read().decode("utf-8"))
        if models != {"data": [{"id": "qwen-test"}]}:
            raise AssertionError(f"unexpected models response: {models!r}")

        request = urllib.request.Request(
            f"{proxy_base}/chat/completions",
            data=json.dumps({"model": "qwen-test", "messages": [], "temperature": 0}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            chat = json.loads(response.read().decode("utf-8"))
            normalized_header = response.headers["X-Hermes-Normalized-Empty-Think-Count"]
            promoted_header = response.headers["X-Hermes-Chat-Reasoning-Tool-Call-Content-Count"]
            override_header = response.headers["X-Hermes-Overridden-Model-Count"]
        content = chat["choices"][0]["message"]["content"]
        if content != "<tool_call>{}</tool_call>":
            raise AssertionError(f"unexpected normalized content: {content!r}")
        promoted_content = chat["choices"][1]["message"]["content"]
        if promoted_content != '<tool_call>\n{"name":"demo.tool","arguments":{}}\n</tool_call>':
            raise AssertionError(f"unexpected promoted content: {promoted_content!r}")
        if normalized_header != "1":
            raise AssertionError(f"unexpected normalization count: {normalized_header!r}")
        if promoted_header != "1":
            raise AssertionError(f"unexpected reasoning tool-call promotion count: {promoted_header!r}")
        if override_header != "1":
            raise AssertionError(f"unexpected model override count: {override_header!r}")

        completions_request = urllib.request.Request(
            f"{proxy_base}/completions",
            data=json.dumps({"model": "qwen-test", "prompt": "The capital of France is", "logprobs": 5}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(completions_request, timeout=5) as response:
            completion = json.loads(response.read().decode("utf-8"))
            coerced_header = response.headers["X-Hermes-Coerced-Logprobs-Count"]
            suffix_header = response.headers["X-Hermes-Completion-Prompt-Suffix-Count"]
            cap_header = response.headers["X-Hermes-Capped-Max-Tokens-Count"]
        if completion["choices"][0]["text"] != " Paris":
            raise AssertionError(f"unexpected completions response: {completion!r}")
        if coerced_header != "1":
            raise AssertionError(f"unexpected logprobs coercion count: {coerced_header!r}")
        if suffix_header != "1":
            raise AssertionError(f"unexpected prompt suffix count: {suffix_header!r}")
        if cap_header != "0":
            raise AssertionError(f"unexpected max token cap count: {cap_header!r}")

        capped_request = urllib.request.Request(
            f"{proxy_base}/completions",
            data=json.dumps(
                {"model": "qwen-test", "prompt": "The capital of France is", "max_tokens": 4096, "logprobs": False}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(capped_request, timeout=5) as response:
            cap_header = response.headers["X-Hermes-Capped-Max-Tokens-Count"]
        if cap_header != "1":
            raise AssertionError(f"unexpected max token cap count: {cap_header!r}")

        reasoning_request = urllib.request.Request(
            f"{proxy_base}/completions",
            data=json.dumps({"model": "qwen-test", "prompt": "blank reasoning", "logprobs": 0}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(reasoning_request, timeout=5) as response:
            reasoning_completion = json.loads(response.read().decode("utf-8"))
            reasoning_header = response.headers["X-Hermes-Completion-Reasoning-Text-Count"]
        if not reasoning_completion["choices"][0]["text"].startswith("<tool_call>"):
            raise AssertionError(f"unexpected reasoning completion: {reasoning_completion!r}")
        if reasoning_header != "1":
            raise AssertionError(f"unexpected reasoning text count: {reasoning_header!r}")

        reasoning_tool_call_request = urllib.request.Request(
            f"{proxy_base}/completions",
            data=json.dumps({"model": "qwen-test", "prompt": "prose reasoning tool call", "logprobs": 0}).encode(
                "utf-8"
            ),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(reasoning_tool_call_request, timeout=5) as response:
            reasoning_tool_call_completion = json.loads(response.read().decode("utf-8"))
            reasoning_tool_call_header = response.headers["X-Hermes-Completion-Reasoning-Tool-Call-Text-Count"]
        if reasoning_tool_call_completion["choices"][0]["text"] != '<tool_call>\n{"name":"demo.tool","arguments":{}}\n</tool_call>':
            raise AssertionError(f"unexpected reasoning tool-call completion: {reasoning_tool_call_completion!r}")
        if reasoning_tool_call_header != "1":
            raise AssertionError(f"unexpected reasoning tool-call text count: {reasoning_tool_call_header!r}")

        prefixed_proxy = NormalizingProxyServer(
            ("127.0.0.1", 0),
            upstream_base,
            timeout_s=5.0,
            quiet=True,
            completion_text_prefix="<tool_call>\n",
        )
        prefixed_thread = start_threaded_server(prefixed_proxy)
        try:
            prefixed_base = f"http://127.0.0.1:{prefixed_proxy.server_port}/v1"
            prefixed_request = urllib.request.Request(
                f"{prefixed_base}/completions",
                data=json.dumps({"model": "qwen-test", "prompt": "The capital of France is", "logprobs": False}).encode(
                    "utf-8"
                ),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(prefixed_request, timeout=5) as response:
                prefixed_completion = json.loads(response.read().decode("utf-8"))
                text_prefix_header = response.headers["X-Hermes-Completion-Text-Prefix-Count"]
            if not prefixed_completion["choices"][0]["text"].startswith("<tool_call>"):
                raise AssertionError(f"unexpected prefixed completion: {prefixed_completion!r}")
            if text_prefix_header != "1":
                raise AssertionError(f"unexpected text prefix count: {text_prefix_header!r}")
        finally:
            prefixed_proxy.shutdown()
            prefixed_thread.join(timeout=5)

        stream_request = urllib.request.Request(
            f"{proxy_base}/chat/completions",
            data=json.dumps({"model": "qwen-test", "messages": [], "stream": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(stream_request, timeout=5)
        except urllib.error.HTTPError as exc:
            if exc.code != HTTPStatus.BAD_REQUEST:
                raise AssertionError(f"unexpected stream rejection status: {exc.code}") from exc
        else:
            raise AssertionError("streaming request should have been rejected")
    finally:
        proxy.shutdown()
        upstream.shutdown()
        proxy_thread.join(timeout=5)
        upstream_thread.join(timeout=5)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", default="http://127.0.0.1:11434/v1", help="Upstream OpenAI-compatible base URL.")
    parser.add_argument("--listen-host", default="127.0.0.1", help="Proxy listen host.")
    parser.add_argument("--listen-port", type=int, default=8099, help="Proxy listen port.")
    parser.add_argument("--timeout-s", type=float, default=120.0, help="Upstream request timeout.")
    parser.add_argument("--model-override", default="", help="Optional model id to forward to the upstream runtime.")
    parser.add_argument(
        "--completion-prompt-suffix",
        default="",
        help="Optional suffix appended to /v1/completions prompts before forwarding, e.g. a Qwen assistant prefill.",
    )
    parser.add_argument(
        "--completion-reasoning-prefix",
        default="",
        help="Optional prefix used when moving non-empty completions reasoning_content into a blank text field.",
    )
    parser.add_argument(
        "--completion-text-prefix",
        default="",
        help="Optional prefix prepended to non-empty /v1/completions text when the runtime consumed it as prompt prefill.",
    )
    parser.add_argument(
        "--completion-max-tokens-cap",
        type=int,
        default=0,
        help="Optional cap for /v1/completions max_tokens before forwarding. Disabled when 0.",
    )
    parser.add_argument(
        "--completion-reasoning-tool-call-text",
        action="store_true",
        help=(
            "For /v1/completions, promote a complete tool_call block from reasoning_content into text "
            "when text is blank or prose."
        ),
    )
    parser.add_argument(
        "--chat-reasoning-tool-call-content",
        action="store_true",
        help="For /v1/chat/completions, promote a complete tool_call block from reasoning_content into message.content.",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress request logs.")
    parser.add_argument("--self-test", action="store_true", help="Run proxy self-tests and exit.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        run_self_test()
        print("openai_normalizing_proxy self-test passed")
        return 0

    server = NormalizingProxyServer(
        (args.listen_host, args.listen_port),
        upstream_base=args.upstream,
        timeout_s=args.timeout_s,
        quiet=args.quiet,
        model_override=args.model_override,
        completion_prompt_suffix=args.completion_prompt_suffix,
        completion_reasoning_prefix=args.completion_reasoning_prefix,
        completion_text_prefix=args.completion_text_prefix,
        completion_max_tokens_cap=args.completion_max_tokens_cap,
        completion_reasoning_tool_call_text=args.completion_reasoning_tool_call_text,
        chat_reasoning_tool_call_content=args.chat_reasoning_tool_call_content,
    )
    print(f"proxy listening on http://{args.listen_host}:{args.listen_port}/v1")
    print(f"upstream: {args.upstream}")
    print("streaming chat completions are rejected because SSE normalization is not implemented")
    print("integer completions logprobs are coerced to boolean for mlx_lm.server compatibility")
    if args.completion_max_tokens_cap > 0:
        print(f"completion max_tokens are capped at {args.completion_max_tokens_cap}")
    if args.completion_reasoning_tool_call_text:
        print("completion reasoning_content tool-call blocks are promoted into text")
    if args.chat_reasoning_tool_call_content:
        print("chat reasoning_content tool-call blocks are promoted into message.content")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
