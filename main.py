from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.router import RouterAgent
from typing import List, Dict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="CloudWalk Agent")

class RequestPayload(BaseModel):
    message: str
    user_id: str


# --- Inicializa router / VectorStore ---
router = RouterAgent()  # router interno vai usar VectorStore

conversation_history: Dict[str, List[Dict[str, str]]] = {}

@app.get("/")
def root():
    return {"message": "CloudWalk Agent API Rodando!"}

@app.get("/health")
def health():
    return {"status": "ok"}

app_root = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=app_root), name="static")

@app.get("/chat")
def chat():
    return FileResponse(os.path.join(app_root, "index.html"))

@app.post("/process")
async def process(payload: RequestPayload):
    try:
        user_id = payload.user_id
        message = payload.message

        if user_id not in conversation_history:
            conversation_history[user_id] = []

        conversation_history[user_id].append({"role": "user", "message": message})

        agent_response = router.handle(message, user_id)

        reply_text = agent_response.get("reply") or agent_response.get("answer") or str(agent_response)

        conversation_history[user_id].append({"role": "agent", "message": reply_text})

        return {
            "response": reply_text,
            "sources": agent_response.get("sources", []),
            "meta": agent_response.get("meta", {}),
            "history": conversation_history[user_id]
        }

    except Exception as e:
        print("ERRO no /process:", e)
        raise HTTPException(status_code=500, detail=str(e))
