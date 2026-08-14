import json
import re
import sys
from pathlib import Path
from typing import TypedDict, List, Optional

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from langgraph.graph import StateGraph, END
from app.config import MOCK_LLM, GROQ_API_KEY
from app.db import query_vectorstore
from app.schemas import AskResponse
from app.prompts import SUPPORT_ASSISTANT_SYSTEM_PROMPT

# State definition
class SupportState(TypedDict):
    query: str
    intent: Optional[str]
    retrieved_docs: Optional[List[str]]
    retrieved_ids: Optional[List[str]]
    final_response: Optional[AskResponse]

POLICY_KEYWORDS = [
    "delivery", "return", "refund", "membership",
    "tracking", "cancel", "gift card", "support hours"
]

def classify_intent_node(state: SupportState) -> SupportState:
    query = state["query"]
    if MOCK_LLM:
        # Keyword-based deterministic classification
        lower_q = query.lower()
        if any(keyword in lower_q for keyword in POLICY_KEYWORDS):
            intent = "policy_question"
        else:
            intent = "general_question"
    else:
        # Optional real LLM classification via Groq
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Classify the query into 'policy_question' (Zepto order, refund, delivery, pass, support) or 'general_question'. Respond with ONLY the label."},
                {"role": "user", "content": query}
            ],
            temperature=0.0
        )
        pred = completion.choices[0].message.content.strip().lower()
        intent = "policy_question" if "policy_question" in pred else "general_question"

    return {"intent": intent}

def route_intent(state: SupportState) -> str:
    return "retrieve_and_answer" if state.get("intent") == "policy_question" else "direct_answer"

def retrieve_and_answer_node(state: SupportState) -> SupportState:
    query = state["query"]
    
    # Real Vector Retrieval from ChromaDB
    retrieval_results = query_vectorstore(query, top_k=3)
    retrieved_docs = retrieval_results["documents"][0] if retrieval_results["documents"] else []
    retrieved_ids = retrieval_results["ids"][0] if retrieval_results["ids"] else []

    if MOCK_LLM:
        # Mock mode: deterministic template extraction from top-1 chunk
        top_snippet = retrieved_docs[0][:200] if retrieved_docs else ""
        canned_answer = f"Based on the retrieved context: {top_snippet}"
        response = AskResponse(
            answer=canned_answer,
            sources=retrieved_ids,
            confidence=1.0
        )
        return {
            "retrieved_docs": retrieved_docs,
            "retrieved_ids": retrieved_ids,
            "final_response": response
        }
    
    # Optional Real LLM path with structured JSON retry loop
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    
    context_text = "\n\n".join([f"[{doc_id}] {doc}" for doc_id, doc in zip(retrieved_ids, retrieved_docs)])
    system_prompt = SUPPORT_ASSISTANT_SYSTEM_PROMPT.format(context=context_text)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    
    validated_response = None
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            raw_text = completion.choices[0].message.content
            parsed = json.loads(raw_text)
            validated_response = AskResponse(**parsed)
            break
        except Exception as e:
            if attempt < max_retries:
                messages.append({"role": "assistant", "content": raw_text if 'raw_text' in locals() else "{}"})
                messages.append({"role": "user", "content": f"Formatting error: {str(e)}. Return strictly valid JSON conforming to the AskResponse schema."})
            else:
                validated_response = AskResponse(
                    answer="An error occurred while generating a schema-compliant response.",
                    sources=retrieved_ids,
                    confidence=0.0
                )

    return {
        "retrieved_docs": retrieved_docs,
        "retrieved_ids": retrieved_ids,
        "final_response": validated_response
    }

def direct_answer_node(state: SupportState) -> SupportState:
    query = state["query"]
    if MOCK_LLM:
        response = AskResponse(
            answer="I can only answer questions about Zepto policies right now.",
            sources=[],
            confidence=1.0
        )
        return {"final_response": response}
    
    # Optional Real LLM path
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Keep answers brief."},
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )
    raw_ans = completion.choices[0].message.content.strip()
    response = AskResponse(answer=raw_ans, sources=[], confidence=0.9)
    return {"final_response": response}

# Graph Construction
def build_support_graph():
    builder = StateGraph(SupportState)
    
    builder.add_node("classify_intent", classify_intent_node)
    builder.add_node("retrieve_and_answer", retrieve_and_answer_node)
    builder.add_node("direct_answer", direct_answer_node)

    builder.set_entry_point("classify_intent")
    
    builder.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "retrieve_and_answer": "retrieve_and_answer",
            "direct_answer": "direct_answer"
        }
    )
    
    builder.add_edge("retrieve_and_answer", END)
    builder.add_edge("direct_answer", END)
    
    return builder.compile()

app_graph = build_support_graph()