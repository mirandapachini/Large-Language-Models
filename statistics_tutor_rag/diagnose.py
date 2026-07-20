"""Small diagnostic script for installation and Ollama connectivity."""

from __future__ import annotations

import importlib
import sys

import requests


REQUIRED_MODULES = {
    "streamlit": "streamlit",
    "numpy": "numpy",
    "pandas": "pandas",
    "pymupdf": "PyMuPDF",
    "docx": "python-docx",
    "pptx": "python-pptx",
    "openpyxl": "openpyxl",
    "requests": "requests",
}

OPTIONAL_MODULES = {"faiss": "faiss-cpu"}


def check_modules() -> bool:
    all_ok = True
    print(f"Python: {sys.version.split()[0]}")
    for module_name, package_name in REQUIRED_MODULES.items():
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "installed")
            print(f"[OK] {package_name}: {version}")
        except Exception as exc:
            all_ok = False
            print(f"[MISSING] {package_name}: {exc}")

    for module_name, package_name in OPTIONAL_MODULES.items():
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "installed")
            print(f"[OPTIONAL OK] {package_name}: {version}")
        except Exception:
            print(f"[OPTIONAL] {package_name} not installed; NumPy retrieval will be used.")
    return all_ok


def check_ollama() -> bool:
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=4)
        response.raise_for_status()
        models = [model.get("name") for model in response.json().get("models", [])]
        print("[OK] Ollama is reachable.")
        print("Installed models:", ", ".join(models) if models else "none")
        required = {"llama3.2:latest", "all-minilm:latest"}
        missing = sorted(required.difference(models))
        if missing:
            print("[NOT READY] Missing Ollama models:", ", ".join(missing))
            print("Run: ollama pull llama3.2")
            print("Run: ollama pull all-minilm")
            return False
        return True
    except Exception as exc:
        print(f"[NOT READY] Ollama: {exc}")
        return False


if __name__ == "__main__":
    modules_ok = check_modules()
    ollama_ok = check_ollama()
    print("\nResult:")
    if modules_ok and ollama_ok:
        print("The installation is ready. Run: streamlit run app.py")
    else:
        print("Resolve the items marked MISSING or NOT READY, then run this script again.")
