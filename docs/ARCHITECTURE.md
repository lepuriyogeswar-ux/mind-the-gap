# Architecture

```text
Browser
  ├── Dashboard and scenario selector
  ├── ZIP upload
  └── Results JSON
          │
          ▼
      FastAPI app
       ├── /api/demo-graph
       ├── /api/simulate → modeled dependency traversal
       └── /api/analyze → ZIP validation → Python AST parser
```

## Trust boundaries

- Uploaded ZIPs are treated as untrusted input.
- ZIP paths, entry count, aggregate uncompressed size, and individual file size are checked.
- Python source is parsed as text and is never imported or executed.
- Static import edges are evidence of code-level imports, not proof of runtime calls.
- Simulation scenarios use an illustrative graph and do not operate on real infrastructure.
- Dependency risk labels are heuristics, not measured reliability.

## Future work

A future version could run generated integration checks in an isolated container with strict resource and network limits, then record observed results separately from predictions. This is not implemented in the current prototype.
