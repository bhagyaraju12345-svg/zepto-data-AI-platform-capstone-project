| File               | Responsibility                             |
| ------------------ | ------------------------------------------ |
| `docs/*.txt`       | Zepto policy knowledge                     |
| `ingest.py`        | Load → chunk → embed → ChromaDB            |
| `prompt.py`        | Structured RAG prompt                      |
| `graph.py`         | LangGraph + routing + retrieval + mock/LLM |
| `main.py`          | FastAPI API                                |
| `requirements.txt` | Python dependencies                        |
| `Dockerfile`       | Container                                  |
| `README.md`        | Documentation/demo                         |



# Module 3 — Support Assistant (`/support_assistant`)

An offline-first, RAG-powered customer support service for Zepto policies orchestrated via LangGraph, ChromaDB, and FastAPI.

---

## 1. RAG Pipeline Architecture

```text
               +----------------------+
               |    Incoming Query    |
               +----------+-----------+
                          |
                          v
            +-------------+-------------+
            |  classify_intent (Node)   |
            +-------------+-------------+
                          |
            [Conditional Edge Router]
             /                         \
            / (policy_question)         \ (general_question)
           v                             v
+--------------------------+   +----------------------+
| retrieve_and_answer Node |   |  direct_answer Node  |
| - ChromaDB Vector Search |   | - Returns canned/LLM |
| - MiniLM-L6-v2 Top-3     |   |   fallback response  |
| - Grounded Generation    |   +----------+-----------+
+------------+-------------+              |
             |                            |
             \                            /
              \                          /
               v                        v
            +------------------------------+
            |   Validated JSON Schema      |
            | (answer, sources, confidence)|
            +------------------------------+


Stage Walkthrough
Ingestion & Embedding (app/db.py):

Reads 8 policy documents from docs/doc_01.txt ... docs/doc_08.txt.

Computes vector embeddings locally using the open-source sentence-transformers/all-MiniLM-L6-v2 model.

Stores vectors and document content in a local ChromaDB collection (zepto_policies) indexed with cosine distance.

Intent Classification (classify_intent Node in app/graph.py):

Inspects the input query to decide if domain context is required.

Mock Mode (Default): Runs a keyword matching check (delivery, return, refund, membership, tracking, cancel, gift card, support hours).

Real LLM Mode (MOCK_LLM=0): Calls Groq API to label the intent.

Retrieval (retrieve_and_answer Node in app/graph.py):

Runs locally for real in both modes.

Queries ChromaDB via cosine similarity to fetch the top-3 most relevant document chunks.

Generation & Schema Enforcement (app/graph.py):

Mock Mode (MOCK_LLM=1): retrieve_and_answer returns f"Based on the retrieved context: {top_chunk_snippet}", document IDs as sources, and 1.0 confidence. direct_answer returns the fixed string "I can only answer questions about Zepto policies right now." with empty sources.

Real LLM Mode (MOCK_LLM=0): Builds a structured prompt (Role–Context–Task–Negative Constraint–Format–Length–Few-shot) and queries Groq with up to 2 retry attempts on schema validation failures.

2. Running Locally
Direct Python Execution
Bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 7860
Docker Execution
Bash
docker build -t zepto-support-assistant .
docker run -p 7860:7860 zepto-support-assistant
3. Example Execution Transcripts (MOCK_LLM=1 Baseline)
Example 1: Policy Retrieval Query (POST /ask)
Request:

Bash
curl -X POST [http://127.0.0.1:7860/ask](http://127.0.0.1:7860/ask) \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the fee for priority delivery?"}'
Raw JSON Response:

JSON
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard deliv",
  "sources": [
    "doc_01",
    "doc_03",
    "doc_05"
  ],
  "confidence": 1.0
}
Example 2: General / Out-of-Scope Query (POST /ask)
Request:

Bash
curl -X POST [http://127.0.0.1:7860/ask](http://127.0.0.1:7860/ask) \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
Raw JSON Response:

JSON
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0

  



