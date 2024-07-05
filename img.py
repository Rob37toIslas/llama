import web
import base64
import requests
import json
import os

urls = (
    '/', 'Index',
    '/upload', 'Upload'
)

render = web.template.render('templates/')

class Index:
    def GET(self):
        return render.index()

class Upload:
    def POST(self):
        x = web.input(myfile={})
        filedir = 'uploads' 
        if not os.path.exists(filedir):
             os.makedirs(filedir)

        filename = os.path.basename(x.myfile.filename)
        filepath = os.path.join(filedir, filename)
        
        with open(filepath, 'wb') as fout:
             fout.write(x.myfile.file.read())

        # # Convertir la imagen a Base64
        imagen_base64 = convertir_imagen_a_base64(filepath)

        #  Obtener el prompt del formulario
        # prompt_usuario = x.prompt
        prompt = f"Analiza la siguiente imagen porfavor"

        #  Generar respuesta usando la API
        respuesta = generar_respuesta(prompt, imagen_base64)

        return render.response(respuesta,imagen_base64)

def convertir_imagen_a_base64(ruta_imagen):
    with open(ruta_imagen, "rb") as imagen:
        datos_imagen = imagen.read()
        datos_base64 = base64.b64encode(datos_imagen)
        cadena_base64 = datos_base64.decode('utf-8')
        return cadena_base64

def generar_respuesta(prompt, imagen_base64):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "fotos",
        "prompt": prompt,
        "images": [imagen_base64],
        "stream": False
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        text = response.text
        json_response = json.loads(text)
        return json_response['response']
    else:
        return f"Error: {response.status_code}, Message: {response.text}"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()