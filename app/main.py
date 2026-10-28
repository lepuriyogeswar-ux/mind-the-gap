from pathlib import Path
from typing import Literal
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.analyzer import analyze_zip
from app.simulator import demo_graph, simulate
BASE=Path(__file__).resolve().parent
app=FastAPI(title="MIND THE GAP",version="0.1.0",description="Dependency risk analysis and safe failure simulation.")
app.mount("/static",StaticFiles(directory=BASE/"static"),name="static")
class SimulationRequest(BaseModel):
 scenario: Literal["database_down","model_api_down","config_missing","high_latency"]
@app.get("/")
def home(): return FileResponse(BASE/"static"/"index.html")
@app.get("/api/health")
def health(): return {"status":"ok","name":"MIND THE GAP","version":"0.1.0"}
@app.get("/api/demo-graph")
def get_demo_graph(): return demo_graph()
@app.post("/api/simulate")
def run_simulation(request: SimulationRequest): return simulate(request.scenario)
@app.post("/api/analyze")
async def analyze(file: UploadFile=File(...)):
 if not file.filename or not file.filename.lower().endswith(".zip"): raise HTTPException(status_code=415,detail="Upload a .zip file.")
 data=await file.read(8*1024*1024+1)
 if len(data)>8*1024*1024: raise HTTPException(status_code=413,detail="ZIP upload exceeds 8 MiB.")
 try: return analyze_zip(data)
 except ValueError as exc: raise HTTPException(status_code=400,detail=str(exc))
