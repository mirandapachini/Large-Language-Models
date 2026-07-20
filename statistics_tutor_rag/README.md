# MSBA Statistics Tutor: Local RAG with Ollama and Streamlit

This project converts the original stock-advisor prototype into a local, course-grounded statistics tutor. It is designed for MSBA students and keeps the RAG pipeline visible rather than hiding it behind a framework.

## What the application does

1. Reads course files from the `docs` folder.
2. Splits text into compact overlapping chunks.
3. Converts chunks into embeddings with Ollama's `all-minilm` model.
4. Retrieves the most relevant chunks using FAISS when available, or a NumPy cosine-search fallback.
5. Sends the retrieved evidence and the student's question to a local Ollama model.
6. Displays the answer together with the retrieved file and page/slide information.

Supported source files: PDF, DOCX, PPTX, TXT, Markdown, CSV, and XLSX.

## Recommended environment

- Windows 10 or 11, 64 bit
- Python 3.11, 64 bit
- 8 GB RAM minimum; 16 GB recommended
- Ollama with `llama3.2:latest`

## Windows installation

### Easy method

1. Install Python 3.11 and Ollama.
2. Double-click `setup_windows.bat`.
3. Open Command Prompt and run:

```bat
ollama pull llama3.2
ollama pull all-minilm
```

4. Double-click `run_windows.bat`.

### Manual method

```bat
cd path\to\statistics_tutor_rag
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
ollama pull llama3.2
ollama pull all-minilm
streamlit run app.py
```

Optional FAISS acceleration:

```bat
python -m pip install -r requirements-faiss.txt
```

The application runs without FAISS by using normalized NumPy dot products.

## Add course content

Copy course files into `docs`, or upload them through the application sidebar. Then click **Rebuild knowledge base**.

Do not place confidential, restricted, or personally identifiable data in the project folder. Everything is processed locally, but the files still remain on the computer.

## Diagnostic check

```bat
python diagnose.py
```

## Teaching notes

- The app demonstrates RAG; it is not a replacement for a statistical computing package.
- CSV and Excel files are converted into row-group text for retrieval. The tutor should not be trusted to compute exact statistics over a large dataset unless the values are separately analyzed in Python, R, or Excel.
- Scanned PDFs require OCR before this app can retrieve their content.
- Pull `all-minilm` once through Ollama before the first run. It is much smaller than installing a PyTorch-based embedding stack.

## Major changes from the stock-advisor version

- Replaced the financial-advisor prompt with an MSBA statistics tutoring prompt.
- Added chat history and tutoring modes.
- Added file, page, slide, sheet, and row metadata.
- Reduced chunk size and added overlap to prevent excessive embedding truncation.
- Replaced the PyTorch/SentenceTransformers dependency with Ollama embeddings for a much lighter student installation.
- Added DOCX, PPTX, TXT, Markdown, CSV, and XLSX support.
- Added upload, cache rebuild, diagnostics, model checking, and error handling.
- Corrected the PyMuPDF dependency: install `PyMuPDF` and import `pymupdf`; do not install the unrelated `fitz` package.
