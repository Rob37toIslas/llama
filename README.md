# llama
- *Paso 1 Instalar Ollama*:curl -fsSL https://ollama.com/install.sh | sh 
- *Paso 2 Mostrar lista de comandos*:ollama
- *Paso 4 Correr servidor*:ollama serve
- *Paso 5 Mostrar modelos Descargados*:ollama list

### modelo: tiny o llama
- *Paso 6 Descargar Modelos*:ollama pull tinyollama
- *Pregunta lo que quieras*: ollama run tinyllama [pregunta]
- *Activa modo chat*: ollama run 
## Consultas mediante api:tinyllama 
```
curl http://localhost:11434/api/generate -d '{
  "model": "tinyllama",
  "prompt":"Por que el cielo es azul?",
  "system":"Responde con 5 palabras y como vegeta",
  "stream": false
}'
```
### llama2
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"Por que el cielo es azul?",
  "system":"Responde con 5 palabras y como vegeta",
  "stream": false
}'
```
### Modelos 
- crear modelo: ollama create [nombre_de_modelo] -f ./Modelfile
- Eliminar Modelo: ollama rm [nombre_de_modelo]