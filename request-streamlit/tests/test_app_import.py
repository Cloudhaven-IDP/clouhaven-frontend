import importlib.util
import pathlib

def test_app_imports():
    p = pathlib.Path(__file__).parent.parent / "src" / "app.py"
    spec = importlib.util.spec_from_file_location("app", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
