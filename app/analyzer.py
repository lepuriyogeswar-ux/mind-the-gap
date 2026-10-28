"""Static Python import analysis. Never executes uploaded code."""
import ast, io, zipfile, sys
from collections import Counter
from pathlib import PurePosixPath
MAX_FILES=500
MAX_TOTAL_UNCOMPRESSED=20*1024*1024
MAX_FILE_BYTES=1024*1024
IGNORED_PARTS={".git",".venv","venv","__pycache__","node_modules","dist","build"}
STDLIB=set(getattr(sys,"stdlib_module_names",()))
def _safe_python_files(blob: bytes):
 try: archive=zipfile.ZipFile(io.BytesIO(blob))
 except (zipfile.BadZipFile,OSError): raise ValueError("The upload is not a valid ZIP archive.")
 infos=archive.infolist()
 if len(infos)>MAX_FILES: raise ValueError(f"ZIP contains too many entries (maximum {MAX_FILES}).")
 if sum(i.file_size for i in infos if not i.is_dir())>MAX_TOTAL_UNCOMPRESSED: raise ValueError("Uncompressed ZIP content exceeds 20 MiB.")
 selected=[]
 for info in infos:
  path=PurePosixPath(info.filename)
  if path.is_absolute() or ".." in path.parts or "\\" in info.filename: raise ValueError("ZIP contains an unsafe path.")
  if info.is_dir() or path.suffix!=".py" or any(p in IGNORED_PARTS for p in path.parts): continue
  if info.file_size>MAX_FILE_BYTES: continue
  selected.append((str(path),archive.read(info)))
 return selected
def analyze_zip(blob: bytes):
 py_files=_safe_python_files(blob)
 if not py_files: raise ValueError("No eligible .py files found in the ZIP.")
 module_by_path={}
 for path,_ in py_files:
  parts=list(PurePosixPath(path).with_suffix("").parts)
  if parts[-1]=="__init__": parts=parts[:-1]
  module_by_path[path]=".".join(parts)
 known=set(module_by_path.values()); nodes={}; edges=[]; errors=[]; counts=Counter()
 for path,content in py_files:
  module=module_by_path[path] or path
  nodes[module]={"id":module,"label":module,"kind":"python_module","path":path}
  try: tree=ast.parse(content.decode("utf-8",errors="replace"),filename=path)
  except SyntaxError as exc:
   errors.append({"path":path,"line":exc.lineno,"message":"Syntax error; imports were not analyzed."}); continue
  for item in ast.walk(tree):
   imported=[]
   if isinstance(item,ast.Import): imported.extend(a.name for a in item.names)
   elif isinstance(item,ast.ImportFrom):
    if item.level==0 and item.module:
     imported.append(item.module); imported.extend(item.module+"."+a.name for a in item.names if a.name!="*")
    elif item.level>0:
     parent=module.rsplit(".",1)[0] if "." in module else ""
     base=".".join(x for x in [parent,item.module or ""] if x)
     imported.append(base); imported.extend(base+"."+a.name for a in item.names if a.name!="*")
   for target in imported:
    matches=[candidate for candidate in known if target==candidate or target.startswith(candidate+".")]
    local=max(matches,key=len) if matches else None; root=target.split(".")[0]
    if local: edges.append({"source":module,"target":local,"kind":"import"}); counts[local]+=1
    else:
     ext="external:"+root; nodes.setdefault(ext,{"id":ext,"label":root,"kind":"external_dependency"}); edges.append({"source":module,"target":ext,"kind":"external_import"}); counts[ext]+=1
 inbound=Counter(e["target"] for e in edges if e["target"] in known)
 for node_id,node in nodes.items():
  if node["kind"]=="python_module":
   node["inbound_imports"]=inbound[node_id]; node["risk"]="high" if inbound[node_id]>=3 else ("medium" if inbound[node_id]>=1 else "low")
  else: node["risk"]="unknown"
 return {"project_name":"Uploaded Python project","nodes":list(nodes.values()),"edges":edges,"summary":{"python_files":len(py_files),"modules":len(known),"edges":len(edges),"external_import_roots":sorted(n["label"] for n in nodes.values() if n["kind"]=="external_dependency"),"high_fan_in_modules":[n["id"] for n in nodes.values() if n.get("risk")=="high"],"parse_errors":errors,"limitations":["Static imports only; dynamic imports and runtime dependencies may be missed.","Risk labels are heuristics, not measured reliability."]}}
