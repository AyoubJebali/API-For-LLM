from fastapi import FastAPI,Depends,HTTPException,Header
import ollama
import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS_CREDITS = {os.getenv("API_KEY"):1}

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEYS_CREDITS.get(x_api_key,0)
    if credits <=0:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    
    return x_api_key

app= FastAPI()
@app.post("/generate")
def generate(promt: str , x_api_key: str = Depends(verify_api_key)):
    API_KEYS_CREDITS[x_api_key] -= 1

    response = ollama.chat("llama2", messages=[{"role": "user", "content": promt}])
    return {"response": response['message']['content']}