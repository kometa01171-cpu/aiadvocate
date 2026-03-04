from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

# React bilan bog'lanish uchun ruxsat berish
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini sozlamalari
os.environ["GOOGLE_API_KEY"] = "AIzaSyAcnhCmq5MJVL8bDgRJ7eADjDBUCsn7QEY"
client = genai.Client()

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        # Python SDK orqali so'rov yuborish
        response = client.models.generate_content(
            model="gemini-2.0-flash", # yoki gemini-2.5-flash-lite
            contents=req.message,
            config={'system_instruction': "You are a professional AI assistant."}
        )
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)