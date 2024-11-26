import os
import json
import google.generativeai as genai

class GerarConteudo:
    def __init__(self, memory_path="memorias.json"):
        self.conversa = []
        self.memory = {}

        self.memory_dir = "memoria_bot" 
        self.memory_path = os.path.join(self.memory_dir, memory_path)    
        os.makedirs(self.memory_dir, exist_ok=True)
        self.load_memory()

        genai.configure(api_key="AIzaSyCGK_PmoCAdrYB02td27SPoeK7ZrnQ5pUM")
        self.model = genai.GenerativeModel("gemini-1.5-flash")


    def save_memory(self):
        try:
            with open(self.memory_path, "w") as file:
                json.dump(self.memory, file, indent=4)
            print("Memoria salva com sucesso.")
        except Exception as e:
            print("Erro ao salvar Memória.")

    def load_memory(self):
        try:
            with open(self.memory_path, "r") as file:
                self.memory = json.load(file)
        except FileNotFoundError:
            self.memory = {}


    def gerarTexto(self, entrada):
        self.conversa.append(f"Usuário: {entrada}")

        context_max = 20
        context = ' '.join(self.conversa[-context_max:])
        memory_context = "\n".join(
            [f"{chave}: {valor}" for chave, valor in self.memory.items()]
        )
        prompt = f"""Você é um assistente virtual amigável e profissional chamado ReneroBot. Responda de forma direta e sem saudações nas respostas,
        Concentre-se em responder o conteúdo da mensagem, considerando o contexto de conversas anteriores.
        Considere o seguinte contexto: {context}
        Se o usuário pedir para lembrar de algo, registe explicitamente no formato "Memoria: chave=valor",
        Memorias importantes do usuário : {memory_context}
        Idioma padrão: Português Brasileiro. Traduza o texto se necessário. Evite repetir saudações; não utilize muitos emojis ou gírias.

        Se a resposta for complexa, pergunte ao final se o usuário necessita de algo mais."""

   
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=2000,
                temperature=1.0,
            )
        )
        texto_resposta = response.text
        self.conversa.append(f"Assistente: {texto_resposta}")

        #Irá processar a memória duradoura e retornar a resposta
        self.process_memory(texto_resposta)
        return texto_resposta
    
    def process_memory(self, texto_resposta, ):
        """Processa e salva memórias indicadas pelo bot."""
        if "Memória:" in texto_resposta:
            linhas = texto_resposta.splitlines()
            for linha in linhas:
                if linha.startswith("Memória:"):
                    _, dados = linha.split("Memória:", 1)
                    chave, valor = dados.split("=", 1)
                    self.memory[chave.strip()] = valor.strip()
            self.save_memory()