import json
import requests
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:5173",  # Vue (Vite por defecto)
    "http://127.0.0.1:5173",
    "http://localhost",
    'https://rob37toislas-llama-16q9q28jqog.ws-us121.gitpod.io/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de chat
model = "gemma3"

# -----------------------
# 🔹 Conexión DB
# -----------------------
def get_product_info(product_name: str):
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, descripcion, precio, stock FROM productos WHERE nombre LIKE ?", (f"%{product_name}%",))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None
    return [
        {"nombre": r[0], "descripcion": r[1], "precio": r[2], "stock": r[3]}
        for r in rows
    ]


# -----------------------
# 🔹 Modelos entrada
# -----------------------
class Message(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    messages: list[Message]


# -----------------------
# 🔹 Lógica del chatbot
# -----------------------
def chat(messages):
    prompt = (
        "Eres un asistente de atención al cliente de una tienda online. "
        "Responde siempre en español, de manera clara, breve (50-100 palabras) y profesional. "
        "Si el cliente pregunta por productos, consulta en la base de datos y responde con nombre, precio, stock y descripción. "
        "Si no existe el producto, indica que no está disponible.\n"
    )

    for message in messages:
        prompt += f"{message.role}: {message.content}\n"

    # Último mensaje del cliente
    user_msg = messages[-1].content
    productos = get_product_info(user_msg)

    if productos:
        info = "\n".join(
            [f"{p['nombre']} - {p['descripcion']}. Precio: ${p['precio']}, Stock: {p['stock']}"
             for p in productos]
        )
        prompt += f"\nInformación desde la base de datos:\n{info}\n"

    prompt += "Respuesta:"

    try:
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={
                "model": model,
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


# -----------------------
# 🔹 Endpoint del chatbot
# -----------------------
@app.post("/api/chat")
async def api_chat(messages: Messages):
    try:
        response_message = chat(messages.messages)
        return response_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
