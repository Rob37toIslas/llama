import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para permitir solicitudes desde ciertos orígenes
origins = [
    "http://localhost",  # Permitir localhost para desarrollo
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    'https://8000-rob37toislas-llama-oxqezh01ncu.ws-us115.gitpod.io'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# El modelo de chat predeterminado
model = "gemma2"  

# Modelo para recibir mensajes
class Message(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    messages: list[Message]
    persona: Optional[str] = Field(None)

def chat(messages, persona=None):
    if persona== 'psicologo':
        prompt = "Contesta esto como un psicologo profecional especializado en combatir adicciones tu nombre es Aurora Bot y da una respuesta corta de 50 a 100 palabras y detallada en español:\n"
    elif persona == 'aurora_bro':
        prompt= 'Contesta esto como  el mejor amigo del usuario y da una respuesta corta de 50 a 100 palabras y detallada en español:\n'
    elif persona == None:
        prompt = 'contesta esta pregunta con una respuesta corta de 50 a 100 palabras y detallada en español:\n '
    for message in messages:
        prompt += f"{message.role}: {message.content}\n"
    prompt += "Respuesta:"

    try:
        # Envía la solicitud al endpoint del modelo de chat
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={
                "model": model,  # Asegúrate de que el modelo se pase correctamente
                "messages": [{"role": "system", "content": prompt}], 
            },
            stream=True
        )
        r.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Error en la solicitud al modelo: {e}")

    output = ""
    for line in r.iter_lines():
        if line:
            try:
                body = json.loads(line)
            except json.JSONDecodeError:
                continue

            if "error" in body:
                raise Exception(body["error"])

            if body.get("done") is False:
                message = body.get("message", {})
                content = message.get("content", "")
                output += content
                print(content, end="", flush=True)

            if body.get("done", False):
                message["content"] = output
                return message

@app.post("/api/chat")
async def api_chat(messages: Messages):
    try:
        response_message = chat(
            messages.messages,
            persona=messages.persona,  # Pasa la persona al método `chat`
        )
        return response_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
