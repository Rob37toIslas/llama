import json
import requests
from supabase import create_client, Client

url: str = "https://qpmehpmdyqbrfcltdlvs.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFwbWVocG1keXFicmZjbHRkbHZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY2Nzk3NzQsImV4cCI6MjAzMjI1NTc3NH0.X5t2joTAF-7MtIsgncKChhcb_o-tl4gRLwvzJjaiQqI"
supabase: Client = create_client(url, key)

model = "gemma2"

def chat(messages):
    prompt = "Proporciona una respuesta corta y detallada:\n"
    for message in messages:
        prompt += f"{message['role']}: {message['content']}\n"
    
    prompt += "Respuesta:"

    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={
            "model": model,
            "messages": [{"role": "system", "content": prompt}], 
            "num_predict": 20,
            "top_k": 10,
            "top_p": 0.7,
            "repeat_penalty": 1.0,
            "mirostat": 0,
            "mirostat_eta": 0.1,
            "num_ctx": 1000
        },
        stream=True
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message

def get_pending_messages():
    response = supabase.table('messages').select('*').eq('status', 'pending').execute()
    return response.data

def insert_message(content, status):
    # Inserta un nuevo mensaje en Supabase y devuelve el ID del nuevo mensaje
    data = {'content': content, 'status': status}
    response = supabase.table('messages').insert(data).execute()
    return response.data[0]['id']  # Devuelve el ID del nuevo mensaje

def update_message_status(message_id, status):
    # Actualiza el estado del mensaje en Supabase
    data = {'status': status}
    supabase.table('messages').update(data).eq('id', message_id).execute()

def main():
    while True:
        # Obtener mensajes pendientes
        messages = get_pending_messages()
        if not messages:
            continue

        for message in messages:
            # Usar el contenido del mensaje para la entrada
            user_input = message['content']
            print(f"Processing message ID {message['id']}: {user_input}")
            
            # Envía el mensaje al modelo de chat
            chat_messages = [{"role": "user", "content": user_input}]
            response_message = chat(chat_messages)
            
            # Inserta el mensaje procesado como nuevo registro en Supabase
            new_message_id = insert_message(response_message['content'], 'processed')

            # Actualiza el estado del último mensaje pendiente a 'processed'
            last_pending_message = messages[-1]  # Asume que el último mensaje en la lista es el más reciente
            update_message_status(last_pending_message['id'], 'processed')
            
            print("\n\n")

if __name__ == "__main__":
    main()
