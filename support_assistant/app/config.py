import os

# MOCK_LLM defaults to 1 (graded baseline)
MOCK_LLM = os.getenv("MOCK_LLM", "1").strip().lower() in ("1", "true", "yes")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = "zepto_policies"