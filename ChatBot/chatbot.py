"""
chatbot.py - Core AI Content Generation and Memory Management for ReneroBot.

This module encapsulates communication with the Google Gemini API (gemini-1.5-flash)
and manages user conversation context and persistent long-term memory.
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file if available
load_dotenv()


class GerarConteudo:
    """
    Manages chatbot responses using Google Gemini API and maintains persistent memory.
    """

    def __init__(self, memory_filename: str = "memorias.json") -> None:
        """
        Initializes the content generator, loads persistent memories, and configures Gemini API.

        :param memory_filename: Filename for storing persistent user memories.
        """
        self.conversa: list[str] = []
        self.memory: Dict[str, str] = {}

        self.memory_dir = "memoria_bot"
        self.memory_path = os.path.join(self.memory_dir, memory_filename)
        os.makedirs(self.memory_dir, exist_ok=True)
        self.load_memory()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY is not set in environment variables.")

        genai.configure(api_key=api_key or "DUMMY_KEY")
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def save_memory(self) -> None:
        """Saves current long-term user memories to a JSON file."""
        try:
            with open(self.memory_path, "w", encoding="utf-8") as file:
                json.dump(self.memory, file, indent=4, ensure_ascii=False)
            print("Memory saved successfully.")
        except Exception as e:
            print(f"Error saving memory: {e}")

    def load_memory(self) -> None:
        """Loads long-term user memories from JSON file if present."""
        try:
            with open(self.memory_path, "r", encoding="utf-8") as file:
                self.memory = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.memory = {}

    def gerar_texto(self, entrada: str) -> str:
        """
        Generates a chatbot response based on user input, context history, and saved memories.

        :param entrada: User input string.
        :return: Bot response text.
        """
        if not os.getenv("GEMINI_API_KEY"):
            return "Erro: GEMINI_API_KEY não configurada. Por favor, adicione sua chave de API no arquivo .env."

        self.conversa.append(f"Usuário: {entrada}")

        context_max = 20
        context = ' '.join(self.conversa[-context_max:])
        memory_context = "\n".join(
            [f"{chave}: {valor}" for chave, valor in self.memory.items()]
        )
        prompt = f"""Você é um assistente virtual amigável e profissional chamado ReneroBot.
        Concentre-se em responder o conteúdo da mensagem, considerando o contexto de conversas anteriores.
        Considere o seguinte contexto: {context}
        Se o usuário pedir para lembrar de algo, registe explicitamente no formato "Memória: chave=valor",
        Memórias importantes do usuário : {memory_context}
        Idioma padrão: Português Brasileiro. Traduza o texto se necessário. Evite repetir saudações; não utilize muitos emojis ou gírias.

        Se a resposta for complexa, pergunte ao final se o usuário necessita de algo mais."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=2000,
                    temperature=0.7,
                )
            )
            texto_resposta = response.text
        except Exception as err:
            texto_resposta = f"Desculpe, ocorreu um erro ao se comunicar com o modelo de IA: {err}"

        self.conversa.append(f"Assistente: {texto_resposta}")

        # Process long-term memory keywords if present
        self.process_memory(texto_resposta)
        return texto_resposta

    # Alias for backward compatibility
    def gerarTexto(self, entrada: str) -> str:
        return self.gerar_texto(entrada)

    def process_memory(self, texto_resposta: str) -> None:
        """
        Processes and stores long-term memory key-values mentioned in bot responses.

        :param texto_resposta: Bot output response text.
        """
        if "Memória:" in texto_resposta or "Memoria:" in texto_resposta:
            linhas = texto_resposta.splitlines()
            for linha in linhas:
                marker = "Memória:" if "Memória:" in linha else ("Memoria:" if "Memoria:" in linha else None)
                if marker and marker in linha:
                    _, dados = linha.split(marker, 1)
                    if "=" in dados:
                        chave, valor = dados.split("=", 1)
                        self.memory[chave.strip()] = valor.strip()
            self.save_memory()
