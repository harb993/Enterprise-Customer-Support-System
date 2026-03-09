from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from support_system import initialize_support_agent
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="Enterprise Support API")

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
print("Initializing Agent for Web API...")
agent_executor = initialize_support_agent()

# Serve static files from React build
DIST_DIR = os.path.join(os.path.dirname(__file__), "frontend/dist")
app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(DIST_DIR, "index.html"))

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Empty message")
    
    try:
        print(f"Web User: {request.message}")
        response = agent_executor.invoke({"input": request.message})
        return JSONResponse(content={"response": response["output"]})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return JSONResponse(content={"response": "I encountered an error processing your request."}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
