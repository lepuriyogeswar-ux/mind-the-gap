import io, zipfile
import pytest
from app.analyzer import analyze_zip

def make_zip(entries):
 stream=io.BytesIO()
 with zipfile.ZipFile(stream,'w') as z:
  for name,content in entries.items(): z.writestr(name,content)
 return stream.getvalue()

def test_analyzes_local_python_imports():
 blob=make_zip({'sample/__init__.py':'','sample/main.py':'from sample import service\nimport json\n','sample/service.py':'def run(): return True\n'})
 result=analyze_zip(blob); assert result['summary']['python_files']==3; assert any(e['target']=='sample.service' for e in result['edges']); assert any(n['label']=='json' for n in result['nodes'])

def test_rejects_invalid_zip():
 with pytest.raises(ValueError): analyze_zip(b'not a zip')

def test_rejects_traversal_path():
 with pytest.raises(ValueError,match='unsafe path'): analyze_zip(make_zip({'../evil.py':"print('no')"}))

def test_no_python_files():
 with pytest.raises(ValueError,match='No eligible'): analyze_zip(make_zip({'README.md':'hello'}))
