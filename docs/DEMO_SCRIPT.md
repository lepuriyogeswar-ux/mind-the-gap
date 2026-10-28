# Demo script (90 seconds)

## Opening (10s)
“Small software systems often fail because one dependency fails. MIND THE GAP helps teams identify possible blast radius before release.”

## Scenario simulation (25s)
Choose “Database unavailable” and run the modeled scenario. Show the affected components, evidence edges, and recommendations. Clarify that this is deterministic graph traversal, not a live outage.

## Static analyzer (25s)
Upload a ZIP containing Python files. Show the import graph summary, external imports, and high fan-in modules. Explain that source is parsed but never executed.

## API and limitations (15s)
Show the health endpoint and interactive `/docs`. Explain that dynamic imports may be missed and risk labels are heuristics.

## Close (15s)
“The next step is to validate predicted impact in an isolated integration environment and compare the prediction with actual test results. MIND THE GAP turns hidden dependencies into testable engineering questions.”
