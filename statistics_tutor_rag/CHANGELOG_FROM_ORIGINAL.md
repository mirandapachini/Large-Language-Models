# Conversion Summary: Stock Advisor to Statistics Tutor

## Removed
- Stock-specific system prompt and interface wording.
- Bundled stock-market PDFs.
- Duplicate/conflicting `fitz` package entry.

## Added
- MSBA statistics tutoring behavior and response modes.
- Source-aware chunks with page, slide, sheet, and row locators.
- Overlapping compact chunks to match the embedding model's short input limit.
- Chat interface and limited conversation history.
- PDF, DOCX, PPTX, TXT, Markdown, CSV, and XLSX ingestion.
- File upload, knowledge-base rebuild, Ollama status, model status, and diagnostics.
- Ollama `all-minilm` embeddings, NumPy cosine-search fallback, and optional FAISS acceleration.
- No PyTorch or SentenceTransformers installation is required.
- Student installation scripts and sample statistics notes.

## Reliability improvements
- Timeouts and readable Ollama errors.
- Safe uploaded filenames.
- Deterministic file ordering and cache invalidation when files change.
- Normalized embeddings with inner-product cosine search.
- Clear warning that table retrieval is not exact statistical computation.
