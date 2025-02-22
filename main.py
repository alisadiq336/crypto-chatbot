from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🌍 Allow CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌟 Gemini API Key (Replace with your key)
API_KEY = "AIzaSyDY1sbV_jQh_ob6xvZafkDIY_2qhPvwOaI"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

# 📩 Request Model
class UserInput(BaseModel):
    text: str

# 🚀 Endpoint to send message
@app.post("/chat")
async def chat(user_input: UserInput):
    try:
        payload = {
            "contents": [{"parts": [{"text": user_input.text}]}]
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()
        
        if "candidates" in data and data["candidates"]:
            bot_response = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"response": bot_response}
        
        return {"response": "Sorry, I couldn't process your request."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
