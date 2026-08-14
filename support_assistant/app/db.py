import os
import glob
import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

import chromadb
from chromadb.utils import embedding_functions
from app.config import CHROMA_PERSIST_DIR, COLLECTION_NAME

# Lazy-load the embedding model so importing the module does not trigger a download.
embedding_fn = None


def get_embedding_fn():
    global embedding_fn
    if embedding_fn is None:
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    return embedding_fn

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)


def resolve_docs_dir(docs_dir: str = "Docs") -> str:
    candidates = []
    if docs_dir:
        candidates.append(docs_dir)

    project_root = Path(__file__).resolve().parent.parent
    candidates.extend([
        str(project_root / "Docs"),
        str(project_root / "docs"),
        str(project_root / "support_assistant" / "Docs"),
    ])

    for candidate in candidates:
        if os.path.isdir(candidate):
            return candidate

    return docs_dir or str(project_root / "Docs")


def initialize_vectorstore(docs_dir: str = "Docs"):
    """Reads the policy files, chunks, embeds, and indexes them in ChromaDB."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_fn(),
        metadata={"hnsw:space": "cosine"}
    )

    # Check if collection is already populated
    if collection.count() >= 8:
        return collection

    resolved_docs_dir = resolve_docs_dir(docs_dir)
    doc_files = sorted({
        path
        for pattern in ("doc_*.txt", "Docs_*.txt", "*.txt")
        for path in glob.glob(os.path.join(resolved_docs_dir, pattern))
    })
    if not doc_files:
        return collection

    documents = []
    ids = []
    metadatas = []

    for file_path in doc_files:
        doc_id = os.path.splitext(os.path.basename(file_path))[0]
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except OSError:
            continue

        if content:
            documents.append(content)
            ids.append(doc_id)
            metadatas.append({"source": doc_id, "file_path": file_path})

    if not documents:
        return collection

    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    return collection

def query_vectorstore(query_text: str, top_k: int = 3):
    """Executes a real vector cosine similarity retrieval."""
    client = get_chroma_client()
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=get_embedding_fn())
    results = collection.query(query_texts=[query_text], n_results=top_k)
    return results