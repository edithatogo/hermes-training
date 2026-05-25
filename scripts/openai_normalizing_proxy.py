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


def coerce_mlx_logprobs_request(payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Coerce OpenAI-style integer logprobs to mlx_lm.server's boolean shape."""
    if "logprobs" not in payload or isinstance(payload.get("logprobs"), bool):
        return payload, 0
    if isinstance(payload.get("logprobs"), int):
        updated = dict(payload)
        updated["logprobs"] = bool(payload["logprobs"])
        return updated, 1
    return payload, 0


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
        coerced_count = 0
        if route in {"/v1/completions", "/completions"}:
            request_payload, coerced_count = coerce_mlx_logprobs_request(request_payload)
            body = json.dumps(request_payload).encode("utf-8")
        self.proxy_request("POST", body, coerced_logprobs_count=coerced_count)

    def proxy_request(self, method: str, body: bytes | None = None, coerced_logprobs_count: int = 0) -> None:
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
                    content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            except ValueError:
                pass

        self.send_response(response.status_code)
        for key, value in response.headers.items():
            if key.lower() not in HOP_BY_HOP_HEADERS:
                self.send_header(key, value)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Hermes-Normalized-Empty-Think-Count", str(normalized_count))
        self.send_header("X-Hermes-Coerced-Logprobs-Count", str(coerced_logprobs_count))
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
    ) -> None:
        super().__init__(server_address, NormalizingProxyHandler)
        self.upstream_base = upstream_base
        self.timeout_s = timeout_s
        self.quiet = quiet


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

    proxy = NormalizingProxyServer(("127.0.0.1", 0), upstream_base, timeout_s=5.0, quiet=True)
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
        content = chat["choices"][0]["message"]["content"]
        if content != "<tool_call>{}</tool_call>":
            raise AssertionError(f"unexpected normalized content: {content!r}")
        if normalized_header != "1":
            raise AssertionError(f"unexpected normalization count: {normalized_header!r}")

        completions_request = urllib.request.Request(
            f"{proxy_base}/completions",
            data=json.dumps({"model": "qwen-test", "prompt": "The capital of France is", "logprobs": 5}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(completions_request, timeout=5) as response:
            completion = json.loads(response.read().decode("utf-8"))
            coerced_header = response.headers["X-Hermes-Coerced-Logprobs-Count"]
        if completion["choices"][0]["text"] != " Paris":
            raise AssertionError(f"unexpected completions response: {completion!r}")
        if coerced_header != "1":
            raise AssertionError(f"unexpected logprobs coercion count: {coerced_header!r}")

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
    )
    print(f"proxy listening on http://{args.listen_host}:{args.listen_port}/v1")
    print(f"upstream: {args.upstream}")
    print("streaming chat completions are rejected because SSE normalization is not implemented")
    print("integer completions logprobs are coerced to boolean for mlx_lm.server compatibility")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
