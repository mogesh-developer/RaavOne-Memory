# RaavOne Memory
![Stars](https://img.shields.io/github/stars/mogesh-developer/RaavOne-Memory?style=social)
![Repo Size](https://img.shields.io/github/repo-size/mogesh-developer/RaavOne-Memory)
![Last Commit](https://img.shields.io/github/last-commit/mogesh-developer/RaavOne-Memory)
![License](https://img.shields.io/github/license/mogesh-developer/RaavOne-Memory)

An AI Memory Engine for Long-Term Conversational Intelligence — lightweight, modular, and easy to integrate with chatbots and conversational agents.

---

<!-- Demo (replace with an actual GIF or screenshot in /docs) -->
![demo](docs/demo.gif)

Quick links: [Getting Started](#quick-start) • [Features](#features) • [Usage](#usage) • [Configuration](#configuration) • [Contributing](#contributing)

---

## Why RaavOne Memory?

Modern conversational agents need to remember and recall context across long interactions. RaavOne Memory provides:

- Persistent, searchable memory stores
- Configurable memory scopes (short-term, long-term)
- Simple API to save & retrieve conversational facts
- Lightweight Python-first implementation designed for integration

---

## Features

- Save and retrieve contextual memories (text, metadata)
- Time-based and relevance-based recall
- Pluggable storage backends (file, SQLite, or external)
- Simple API that fits into existing chatbot flows
- Extensible for custom vector stores or embeddings

---

## Quick Start

Install (from PyPI or from source)

```bash
# pip (if published to PyPI)
pip install raavone-memory

# OR install from this repo
git clone https://github.com/mogesh-developer/RaavOne-Memory.git
cd RaavOne-Memory
pip install -e .
```

Minimal usage example:

```python
from raavone_memory import MemoryEngine

# Initialize engine (defaults to a simple local store)
engine = MemoryEngine(store_path="~/.raavone_memory/db.sqlite")

# Save a memory
engine.save(user_id="user_123", text="User likes sci-fi movies", tags=["preference"])

# Query for relevant memory
results = engine.recall(user_id="user_123", query="What does the user like?", top_k=3)
for r in results:
    print(r.text, r.timestamp)
```

See docs/ or examples/ for more in-depth guides.

---

## Configuration

Recommended config options (example dict):

```yaml
memory:
  store: sqlite
  store_path: ~/.raavone_memory/db.sqlite
  embedding_model: all-MiniLM-L6-v2
  recall:
    top_k: 5
    time_decay_days: 90
```

- store: backend type (sqlite, file, redis, vector)
- embedding_model: model used for semantic similarity (if enabled)
- recall.top_k: number of results returned during recall

---

## File Layout (example)

- raavone_memory/
  - core.py
  - store_sqlite.py
  - embeddings.py
  - api.py
- examples/
- docs/

---

## Best Practices

- Store only essential facts (avoid raw PII)
- Use tags/metadata to scope memory queries
- Regularly prune or summarize old memories to save space

---

## Contributing

Contributions welcome! A suggested workflow:

1. Fork the repo
2. Create a feature branch: git checkout -b feat/my-change
3. Add tests in tests/
4. Open a pull request with a clear description

Please follow the repo's coding style and add small, focused commits.

---

## Roadmap / Ideas

- Add vector DB integrations (Milvus, Pinecone)
- Memory summarization module for long histories
- Web UI to inspect and manage memories

---

## Troubleshooting / FAQ

Q: Where are memories stored?
A: Default is a local SQLite at ~/.raavone_memory; configurable via store_path.

Q: Can I use embeddings?
A: Yes — set an embedding_model and a compatible backend.

---

## License

MIT License — see LICENSE file.

---

If you want a generated demo GIF, image assets in docs/, or a rendered docs site (mkdocs), I can add those too.
