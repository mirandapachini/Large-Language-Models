"""Streamlit interface for the local HR Onboarding RAG application."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from rag_engine import (
    DEFAULT_EMBEDDING_MODEL,
    SUPPORTED_EXTENSIONS,
    build_knowledge_base,
    build_tutor_messages,
    check_ollama,
    discover_documents,
    document_signature,
    query_ollama,
)


st.set_page_config(
    page_title="HR OnboardBot",
    page_icon="💼",
    layout="wide",
)

PROJECT_DIR = Path(__file__).resolve().parent
DOCS_DIR = PROJECT_DIR / "docs"
DOCS_DIR.mkdir(exist_ok=True)


@st.cache_resource(show_spinner=False)
def get_knowledge_base(
    signature: str,
    embedding_model: str,
    ollama_url: str,
    chunk_size: int,
    overlap: int,
    prefer_faiss: bool,
):
    # The signature is intentionally unused inside the function. Its presence in
    # the cache key forces a rebuild whenever a file changes.
    del signature
    return build_knowledge_base(
        DOCS_DIR,
        embedding_model_name=embedding_model,
        ollama_url=ollama_url,
        chunk_size=chunk_size,
        overlap=overlap,
        prefer_faiss=prefer_faiss,
    )


def save_uploaded_files(uploaded_files) -> tuple[int, list[str]]:
    saved = 0
    errors: list[str] = []
    for uploaded_file in uploaded_files:
        safe_name = Path(uploaded_file.name).name
        extension = Path(safe_name).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            errors.append(f"{safe_name}: unsupported file type")
            continue
        try:
            (DOCS_DIR / safe_name).write_bytes(uploaded_file.getbuffer())
            saved += 1
        except OSError as exc:
            errors.append(f"{safe_name}: {exc}")
    return saved, errors


def show_sources(sources: list[dict]) -> None:
    if not sources:
        return
    with st.expander("Retrieved HR sources", expanded=False):
        for source in sources:
            st.markdown(
                f"**{source['citation']}**  \n"
                f"Similarity: `{source['score']:.3f}`"
            )
            st.write(source["excerpt"])
            st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("Knowledge base")
    current_files = discover_documents(DOCS_DIR)
    st.caption(f"{len(current_files)} supported file(s) in the docs folder")

    uploaded_files = st.file_uploader(
        "Add HR files",
        type=[extension.lstrip(".") for extension in sorted(SUPPORTED_EXTENSIONS)],
        accept_multiple_files=True,
        help="Files are copied into the local docs folder and indexed after you click Save.",
    )
    if st.button("Save and index uploaded files", use_container_width=True):
        if not uploaded_files:
            st.warning("Choose at least one file first.")
        else:
            saved_count, upload_errors = save_uploaded_files(uploaded_files)
            get_knowledge_base.clear()
            if saved_count:
                st.success(f"Saved {saved_count} file(s). Rebuilding the index.")
            for error in upload_errors:
                st.error(error)
            st.rerun()

    with st.expander("Files currently indexed"):
        if current_files:
            for file_path in current_files:
                st.write(f"• {file_path.name}")
        else:
            st.write("No supported files found.")

    st.header("HR OnboardBot settings")
    ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")
    model_name = st.text_input("Chat model", value="llama3.2:latest")
    response_style = st.selectbox(
    "Response style",
        [
            "Explain in detail",
            "Quick answer",
            "Step-by-step process",
            "New hire FAQ",
        ],
    )
    top_k = st.slider("Retrieved chunks", min_value=2, max_value=8, value=5)

    with st.expander("Advanced retrieval settings"):
        embedding_model = st.text_input(
            "Ollama embedding model",
            value=DEFAULT_EMBEDDING_MODEL,
            help="Install it once with: ollama pull all-minilm",
        )
        chunk_size = st.slider("Words per chunk", 100, 240, 180, 10)
        overlap = st.slider("Overlapping words", 10, 70, 35, 5)
        prefer_faiss = st.checkbox("Use FAISS when installed", value=True)

    if st.button("Rebuild knowledge base", use_container_width=True):
        get_knowledge_base.clear()
        st.rerun()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    ollama_ok, installed_models, ollama_message = check_ollama(ollama_url)
    if ollama_ok:
        st.success("Ollama connected")
        if installed_models and model_name not in installed_models:
            st.warning(
                f"'{model_name}' was not found. Installed models: "
                + ", ".join(installed_models[:6])
            )
    else:
        st.error("Ollama not connected")
        st.caption(ollama_message)


st.title("💼 HR OnboardBot")
st.markdown(
  "Ask questions about company policies, benefits, IT setup, and onboarding procedures. "
    "Answers are grounded in the HR documents stored in `docs/`."
)
if not ollama_ok:
    st.warning(
        "Start Ollama before building the knowledge base. The app uses Ollama for both "
        "embeddings and the tutor response."
    )
    st.code("ollama pull llama3.2\nollama pull all-minilm")
    st.stop()

if installed_models and embedding_model not in installed_models:
    st.warning(
        f"The embedding model '{embedding_model}' is not installed. Run: "
        f"ollama pull {embedding_model.split(':')[0]}"
    )
    st.stop()

if installed_models and model_name not in installed_models:
    st.warning(
        f"The chat model '{model_name}' is not installed. Run: "
        f"ollama pull {model_name.split(':')[0]}"
    )
    st.stop()

if not current_files:
    st.info(
        "Add course notes, slides, PDFs, Word files, CSV files, or Excel files using the sidebar. "
        "A sample HR note is included in the distributed project."
    )
    st.stop()

try:
    with st.spinner("Loading the course knowledge base..."):
        knowledge_base, ingestion_errors = get_knowledge_base(
            document_signature(DOCS_DIR),
            embedding_model,
            ollama_url,
            chunk_size,
            overlap,
            prefer_faiss,
        )
except Exception as exc:
    st.error(f"The knowledge base could not be built: {type(exc).__name__}: {exc}")
    st.info(
        "Confirm that Ollama is running and that the selected embedding model is installed. "
        "Then rebuild the knowledge base."
    )
    st.stop()

summary_col1, summary_col2, summary_col3 = st.columns(3)
summary_col1.metric("Source files", len(current_files))
summary_col2.metric("Text chunks", len(knowledge_base.chunks))
summary_col3.metric("Search backend", knowledge_base.backend_name)

if ingestion_errors:
    with st.expander("Files that could not be read"):
        for error in ingestion_errors:
            st.warning(error)

if not st.session_state.messages:
    st.markdown("**Example questions**")
    examples = [
      "How many PTO days do new hires get in their first year?",
        "What is the deadline to enroll in benefits after starting?",
        "What password requirements do I need to set on Day 1?",
        "Does the company match 401(k) contributions?",
        "Who do I contact if I have a workplace conflict?"
    ]
    
    columns = st.columns(2)
    for index, example in enumerate(examples):
        if columns[index % 2].button(example, key=f"example_{index}", use_container_width=True):
            st.session_state.pending_question = example
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            show_sources(message.get("sources", []))

question = st.chat_input("Ask a HR onboarding question...")
if not question and st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not ollama_ok:
            answer = (
                "Ollama is not connected. Start Ollama, verify that the selected model is installed, "
                "and submit the question again."
            )
            sources: list[dict] = []
            st.error(answer)
        else:
            with st.spinner("Retrieving HR Onboarding information and generating an explanation..."):
                results = knowledge_base.search(question, k=top_k)
                messages = build_tutor_messages(
                    question,
                    results,
                    response_style=response_style,
                    recent_history=st.session_state.messages[:-1],
                )
                try:
                    answer = query_ollama(
                        messages,
                        model_name=model_name,
                        base_url=ollama_url,
                    )
                except RuntimeError as exc:
                    answer = f"I could not generate the answer: {exc}"

                sources = [
                    {
                        "citation": result.chunk.citation,
                        "score": result.score,
                        "excerpt": (
                            result.chunk.text[:700]
                            + ("..." if len(result.chunk.text) > 700 else "")
                        ),
                    }
                    for result in results
                ]
            st.markdown(answer)
            show_sources(sources)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
