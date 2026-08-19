"""
Perguntas.py - Welcome Greetings Management for ReneroBot.

Provides initial random greeting selection for new chat sessions.
"""

import random
from typing import List


class InteracaoChatBot:
    """Manages initial greetings and interaction triggers for the chatbot UI."""

    def __init__(self) -> None:
        self.saudacoes: List[str] = [
            "Olá! Como posso te ajudar hoje?",
            "Oi! Que bom ver você por aqui!",
            "Bem-vindo! O que você gostaria de conversar?",
            "Oi! Que bom te ver por aqui!",
            "Bem-vindo! O que gostaria de conversar hoje?",
            "Olá! Estou pronto para responder suas perguntas!",
            "Oi, como você está? Vamos conversar!",
            "Bem-vindo! O que você gostaria de saber hoje?",
            "Olá! Como posso ser útil hoje?",
            "Oi! Precisa de alguma ajuda? Estou aqui!",
            "Bem-vindo ao chat! No que posso te auxiliar?",
            "Olá! Que tal começarmos uma conversa?",
            "Oi! Como posso te ajudar nesta jornada?",
            "Bem-vindo! Estou à disposição para suas perguntas!",
            "Olá! Vamos resolver suas dúvidas hoje?",
            "Oi! Como você está? Posso te ajudar em algo?",
            "Bem-vindo ao chat! Qual é a sua pergunta?",
            "Olá! Pronto para te ajudar com o que precisar!"
        ]
        self.saudacao_enviada: bool = False

    def obter_saudacao(self) -> str:
        """
        Returns a randomly selected initial greeting message.

        :return: Greeting string if not sent yet, otherwise empty string.
        """
        if not self.saudacao_enviada:
            self.saudacao_enviada = True
            return random.choice(self.saudacoes)
        return ""

    # Aliases for backward compatibility
    def iteracao_ram(self) -> str:
        return self.obter_saudacao()


# Backward compatibility alias
interacaoChatBot = InteracaoChatBot
