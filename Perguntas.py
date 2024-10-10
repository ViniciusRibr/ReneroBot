import random
class interacaoChatBot:
    def __init__(self):
        self.saudacoes = [
            "Olá! Como posso te ajudar hoje?",
            "Oi! Que bom ver você por aqui!",
            "Bem-vindo! O que você gostaria de conversar?"
        ]
        self.despedidas = [
            "Foi um prazer falar com você, até logo!",
            "Espero que tenha um ótimo dia! Volte sempre!",
            "Se precisar de mais alguma coisa, estou aqui. Até a próxima!"
        ]

    def iteracao_ram(self):
        return random.choice(self.saudacoes)

    def say_goodbye(self):
        return random.choice(self.despedidas)
