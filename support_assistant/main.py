from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.schemas import AskRequest, AskResponse
from app.db import initialize_vectorstore
from app.graph import app_graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize index on startup
    initialize_vectorstore(docs_dir="Docs")
    yield

app = FastAPI(
    title="Zepto Support Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(request: AskRequest):
    try:
        initial_state = {
            "query": request.query,
            "intent": None,
            "retrieved_docs": None,
            "retrieved_ids": None,
            "final_response": None
        }
        result = app_graph.invoke(initial_state)
        return result["final_response"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)