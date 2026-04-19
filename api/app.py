from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

from agent.engine import start_session, step

app = FastAPI(title="Deterministic Reflection Agent API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sessions = {}


class StepInput(BaseModel):
    session_id: str
    choice: int | None = None


# Routes

@app.get("/")
def home():
    return {"message": "Reflection Agent API is running"}


@app.post("/start")
def start():
    session_id = str(uuid.uuid4())

    session = start_session()
    sessions[session_id] = session

    first_step = step(session)

    return {
        "session_id": session_id,
        "data": first_step
    }


@app.post("/step")
def next_step(input: StepInput):
    session_id = input.session_id

    if session_id not in sessions:
        return {"error": "Invalid session_id"}

    session = sessions[session_id]

    result = step(session, input.choice)

    return {
        "session_id": session_id,
        "data": result
    }


@app.get("/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        return {"error": "Invalid session_id"}

    return sessions[session_id]


@app.delete("/session/{session_id}")
def reset_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session deleted"}

    return {"error": "Session not found"}