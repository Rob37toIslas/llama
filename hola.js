import {Ollama} from "@langchain/community/llms/ollama";


const ollama = new Ollama({
  baseUrl: "http://localhost:11434",
  model: "psico",
});

const answer = await ollama.invoke(`Hola como te llamas`);
console.log(answer);