import json
import requests
from supabase import create_client, Client

url: str = "https://qpmehpmdyqbrfcltdlvs.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFwbWVocG1keXFicmZjbHRkbHZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY2Nzk3NzQsImV4cCI6MjAzMjI1NTc3NH0.X5t2joTAF-7MtIsgncKChhcb_o-tl4gRLwvzJjaiQqI"
supabase: Client = create_client(url, key)

model = "psicologo"

def chat(messages):
    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
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

def update_message_status(message_id, status, content=None):
    # Actualiza el estado del mensaje en Supabase
    data = {'status': status}
    if content:
        data['content'] = content
    supabase.table('messages').update(data).eq('id', message_id).execute()

def main():
    while True:
        # Obtener mensajes pendientes
        messages = get_pending_messages()
        if not messages:
            continue

        for message in messages:
            user_input = message['content']
            print(f"Processing message ID {message['id']}: {user_input}")
            
            # Envía el mensaje al modelo de chat
            chat_messages = [{"role": "user", "content": user_input}]
            response_message = chat(chat_messages)
            
            # Actualiza el estado del mensaje en Supabase con la respuesta
            update_message_status(message['id'], 'processed', response_message['content'])
            print("\n\n")

if __name__ == "__main__":
    main()
