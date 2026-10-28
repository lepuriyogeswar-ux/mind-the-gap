# MIND THE GAP — The Hidden Dependency Detector

MIND THE GAP is a local-first dependency risk explorer for Python projects. It combines safe static import analysis with deterministic, hypothetical failure scenarios to help developers ask better questions about dependency blast radius.

## Features

- Responsive browser dashboard backed by FastAPI.
- Simulate four modeled scenarios: database unavailable, AI model API unavailable, missing configuration, and high database latency.
- Upload a ZIP archive of Python source for AST-based import analysis.
- Review module counts, import edges, external import roots, high fan-in heuristics, and parse errors in JSON results.
- Interactive API documentation at `/docs` and a health endpoint at `/api/health`.

## Safety and scope

Uploaded source code is parsed as text and is never imported or executed. ZIP paths, entry count, aggregate uncompressed size, and upload size are bounded. Scenario outcomes are modeled graph traversal, not real chaos-engineering experiments. Dynamic imports and runtime behavior may not be represented. Risk labels are heuristics, not production reliability guarantees.

## Run locally

Python 3.10+ recommended.

```bash
python -m venv .venv
```

Activate the environment, then install dependencies and run the app:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 in your browser. API documentation is available at http://127.0.0.1:8000/docs.

## Tests

```bash
python -m pytest -q
```

GitHub Actions runs the test suite on pushes to `main` and on pull requests.

## Project layout

- `app/main.py` — FastAPI application and API routes
- `app/analyzer.py` — safe Python AST import analyzer
- `app/simulator.py` — deterministic scenario simulations
- `app/static/index.html` — responsive browser dashboard
- `tests/` — analyzer and simulator tests
- `examples/sample_project/` — sample project for demonstrations
- `docs/ARCHITECTURE.md` — architecture and trust boundaries
- `docs/DEMO_SCRIPT.md` — short demo walkthrough

## Limitations

This is a prototype for dependency-risk exploration. It does not execute uploaded code, stop real services, or validate runtime failure behavior.