# MIND THE GAP — The Hidden Dependency Detector

MIND THE GAP is a local-first dependency risk explorer for Python projects. It statically analyzes Python imports, visualizes dependency relationships, highlights potential single points of failure, and runs deterministic hypothetical failure scenarios.

## Features

- Upload a ZIP archive containing a Python project for static analysis.
- Explore an interactive dependency graph.
- Identify dependency hotspots and potential single points of failure.
- Simulate hypothetical scenarios such as database downtime, model API outage, missing configuration, and high latency.
- Review impact analysis and export results as JSON.

## Safety and scope

Uploaded source code is analyzed statically and is never executed. Scenario outcomes are modeled simulations, not real chaos-engineering experiments. Dynamic imports and runtime behavior may not be fully represented, so results should be treated as exploratory signals rather than production reliability guarantees.

## Run locally

Python 3.10+ recommended.

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## Tests

```bash
pytest -q
```

## Project layout

- `app/main.py` — FastAPI application and API routes
- `app/analyzer.py` — Python AST-based dependency analyzer
- `app/simulator.py` — deterministic scenario simulations
- `app/static/index.html` — browser dashboard
- `tests/` — analyzer and simulator tests
- `examples/sample_project/` — sample project for demonstrations
- `docs/ARCHITECTURE.md` — architecture overview
- `docs/DEMO_SCRIPT.md` — demo walkthrough

## Limitations

This prototype does not execute uploaded project code or validate actual runtime failure behavior.