"""Deterministic modeled scenarios; no real services are stopped."""
from collections import deque

BASE_NODES = [
 {"id":"browser","label":"Browser UI","kind":"client","tier":"edge"},
 {"id":"web","label":"Web frontend","kind":"service","tier":"app"},
 {"id":"api","label":"Application API","kind":"service","tier":"app"},
 {"id":"auth","label":"Authentication","kind":"service","tier":"app"},
 {"id":"database","label":"Primary database","kind":"data","tier":"data"},
 {"id":"cache","label":"Session cache","kind":"data","tier":"data"},
 {"id":"model_api","label":"AI model API","kind":"external","tier":"external"},
 {"id":"object_store","label":"File storage","kind":"data","tier":"data"},
 {"id":"config","label":"Runtime configuration","kind":"config","tier":"config"},
]
BASE_EDGES = [
 {"source":"browser","target":"web","label":"loads"},
 {"source":"web","target":"api","label":"HTTP requests"},
 {"source":"api","target":"auth","label":"validates identity"},
 {"source":"auth","target":"database","label":"user records"},
 {"source":"auth","target":"cache","label":"sessions"},
 {"source":"api","target":"database","label":"reads/writes"},
 {"source":"api","target":"model_api","label":"inference calls"},
 {"source":"api","target":"object_store","label":"file operations"},
 {"source":"api","target":"config","label":"loads settings"},
]
SCENARIOS = {
 "database_down": {"name":"Database unavailable","target":"database","severity":"critical","description":"The primary database cannot accept connections.","observed":["Database-backed reads and writes fail in this modeled scenario.","Authentication cannot verify accounts if user records are database-backed.","The browser and static frontend remain reachable, but dependent actions degrade."],"fixes":["Add bounded connection timeouts and clear user-facing degraded states.","Review backup/restore objectives and test recovery procedures.","Cache only safe, explicitly stale-tolerant reads; never treat cache as the source of truth."]},
 "model_api_down": {"name":"AI model API unavailable","target":"model_api","severity":"high","description":"The external inference provider times out or returns an outage.","observed":["AI-powered requests fail or time out if no fallback path exists.","Core non-AI pages can remain available if request handling is isolated."],"fixes":["Set strict request timeouts and bounded retries with jitter.","Use a circuit breaker and a clear fallback response.","Keep non-AI endpoints independent from model-provider availability."]},
 "config_missing": {"name":"Required configuration missing","target":"config","severity":"high","description":"A required runtime setting is absent.","observed":["Application startup or a dependent API operation may fail.","The impact depends on whether configuration is validated at startup or read lazily."],"fixes":["Validate required settings at startup and fail with a safe, actionable message.","Document environment variables in .env.example without real secrets.","Add configuration validation to CI."]},
 "high_latency": {"name":"High database latency","target":"database","severity":"high","description":"Database responses exceed the application's latency budget.","observed":["Requests waiting on database calls may accumulate and slow down.","If timeouts and concurrency limits are absent, saturation can spread to the API."],"fixes":["Set query and request deadlines; propagate cancellation.","Measure connection-pool saturation and p95/p99 latency.","Use load tests to validate backpressure and concurrency limits."]}
}
def demo_graph():
 return {"project_name":"Demo commerce + AI service","nodes":BASE_NODES,"edges":BASE_EDGES,"scenarios":[{"id":k,"name":v["name"],"severity":v["severity"]} for k,v in SCENARIOS.items()],"notice":"Illustrative modeled system. Results are not live infrastructure measurements."}
def simulate(scenario: str):
 if scenario not in SCENARIOS: raise ValueError("Unknown scenario.")
 cfg=SCENARIOS[scenario]; target=cfg["target"]
 dependents={}
 for edge in BASE_EDGES: dependents.setdefault(edge["target"],[]).append(edge["source"])
 seen,queue={target},deque([target])
 while queue:
  current=queue.popleft()
  for dependent in dependents.get(current,[]):
   if dependent not in seen: seen.add(dependent); queue.append(dependent)
 affected=[n["id"] for n in BASE_NODES if n["id"] in seen]
 return {"scenario":scenario,"name":cfg["name"],"target":target,"severity":cfg["severity"],"description":cfg["description"],"predicted_affected":affected,"observed_simulation":cfg["observed"],"evidence":[f"Modeled dependency edge: {e['source']} depends on {e['target']}." for e in BASE_EDGES if e["target"]==target],"recommendations":cfg["fixes"],"method":"Deterministic graph traversal plus scenario-specific observations.","is_live_experiment":False,"caveat":"Predictions are illustrative and depend on the modeled graph; validate against real tests and telemetry."}
