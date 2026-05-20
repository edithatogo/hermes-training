# Python Style Guide

- Keep scripts dependency-light and runnable from repo-relative paths.
- Use `pathlib.Path` for filesystem paths.
- Prefer structured parsers over ad hoc string parsing.
- Add CLI `--dry-run` where a command could download, train, publish, or write large artifacts.
- Keep generated artifacts outside Git unless explicitly promoted.
