#!/usr/bin/env python3
"""Download a large Hugging Face file with resumable HTTP range chunks."""
from __future__ import annotations

import argparse
import math
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from huggingface_hub import hf_hub_url


def resolve_url(repo_id: str, filename: str) -> tuple[str, int]:
    url = hf_hub_url(repo_id, filename)
    response = requests.head(url, allow_redirects=True, timeout=60)
    response.raise_for_status()
    size = int(response.headers["content-length"])
    return response.url, size


def completed_size(ranges: list[tuple[int, int, int, Path]]) -> int:
    total = 0
    for _, _start, _end, path in ranges:
        if path.exists():
            total += path.stat().st_size
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        if tmp_path.exists():
            total += tmp_path.stat().st_size
    return total


def download_chunk(
    repo_id: str,
    filename: str,
    part_path: Path,
    start: int,
    end: int,
    timeout_s: float,
    attempts: int,
) -> int:
    expected = end - start + 1
    if part_path.exists() and part_path.stat().st_size == expected:
        return expected
    tmp_path = part_path.with_suffix(part_path.suffix + ".tmp")
    last_error: Exception | None = None
    for _ in range(attempts):
        existing = tmp_path.stat().st_size if tmp_path.exists() else 0
        if existing > expected:
            tmp_path.unlink(missing_ok=True)
            existing = 0
        if existing == expected:
            tmp_path.replace(part_path)
            return expected

        try:
            signed_url, _ = resolve_url(repo_id, filename)
            range_start = start + existing
            headers = {"Range": f"bytes={range_start}-{end}"}
            with requests.get(signed_url, headers=headers, stream=True, timeout=timeout_s) as response:
                if response.status_code != 206:
                    raise RuntimeError(f"expected HTTP 206, got {response.status_code}")
                with tmp_path.open("ab") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
            actual = tmp_path.stat().st_size
            if actual == expected:
                tmp_path.replace(part_path)
                return actual
            last_error = RuntimeError(f"{part_path.name}: expected {expected} bytes, got {actual}")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"{part_path.name}: failed after {attempts} attempts: {last_error}")


def assemble(parts: list[Path], output: Path, expected_size: int) -> None:
    tmp_output = output.with_suffix(output.suffix + ".tmp")
    with tmp_output.open("wb") as out:
        for part in parts:
            with part.open("rb") as handle:
                while data := handle.read(16 * 1024 * 1024):
                    out.write(data)
    actual = tmp_output.stat().st_size
    if actual != expected_size:
        tmp_output.unlink(missing_ok=True)
        raise RuntimeError(f"assembled file expected {expected_size} bytes, got {actual}")
    tmp_output.replace(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--chunk-mib", type=int, default=64)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout-s", type=float, default=300)
    parser.add_argument("--attempts", type=int, default=5)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    part_dir = args.output.with_suffix(args.output.suffix + ".parts")
    part_dir.mkdir(parents=True, exist_ok=True)

    _, total_size = resolve_url(args.repo_id, args.filename)
    if args.output.exists() and args.output.stat().st_size == total_size:
        print(f"already complete: {args.output}")
        return 0

    chunk_size = args.chunk_mib * 1024 * 1024
    ranges = []
    for index in range(math.ceil(total_size / chunk_size)):
        start = index * chunk_size
        end = min(total_size - 1, start + chunk_size - 1)
        ranges.append((index, start, end, part_dir / f"{index:06d}.part"))

    completed_before = sum(1 for _, start, end, path in ranges if path.exists() and path.stat().st_size == end - start + 1)
    print(f"file: {args.filename}", flush=True)
    print(f"size: {total_size}", flush=True)
    print(f"chunks: {len(ranges)} ({completed_before} already complete)", flush=True)
    print(f"output: {args.output}", flush=True)

    started = time.time()
    done = completed_before
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                download_chunk,
                args.repo_id,
                args.filename,
                path,
                start,
                end,
                args.timeout_s,
                args.attempts,
            ): (index, start, end, path)
            for index, start, end, path in ranges
            if not (path.exists() and path.stat().st_size == end - start + 1)
        }
        for future in as_completed(futures):
            index, _, _, _ = futures[future]
            future.result()
            done += 1
            elapsed = max(0.001, time.time() - started)
            downloaded = completed_size(ranges)
            mib_s = downloaded / 1024 / 1024 / elapsed
            print(f"chunk {index} complete; {done}/{len(ranges)} chunks; {mib_s:.2f} MiB/s", flush=True)

    parts = [path for _, _, _, path in ranges]
    assemble(parts, args.output, total_size)
    print(f"complete: {args.output}", flush=True)
    print(f"bytes: {os.path.getsize(args.output)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
