import random
class interacaoChatBot:
    def __init__(self):
        self.saudacoes = [
            "Olá! Como posso te ajudar hoje?",
            "Oi! Que bom ver você por aqui!",
            "Bem-vindo! O que você gostaria de conversar?"
            "Oi! Que bom te ver por aqui!"
            "Bem-vindo! O que gostaria de conversar hoje?"
            "Olá! Estou pronto para responder suas perguntas!"
            "Oi, como você está? Vamos conversar!"
            "Bem-vindo! O que você gostaria de saber hoje?"
            "Olá! Como posso ser útil hoje?"
            "Oi! Precisa de alguma ajuda? Estou aqui!"
            "Bem-vindo ao chat! No que posso te auxiliar?"
            "Olá! Que tal começarmos uma conversa?"
            "Oi! Como posso te ajudar nesta jornada?"
            "Bem-vindo! Estou à disposição para suas perguntas!"
            "Olá! Vamos resolver suas dúvidas hoje?"
            "Oi! Como você está? Posso te ajudar em algo?"
            "Bem-vindo ao chat! Qual é a sua pergunta?"
            "Olá! Pronto para te ajudar com o que precisar!" 
        ]
        self.despedidas = [
            "Foi um prazer falar com você, até logo!",
            "Espero que tenha um ótimo dia! Volte sempre!",
            "Se precisar de mais alguma coisa, estou aqui. Até a próxima!"
            "Foi um prazer falar com você, até logo!"
            "Espero que tenha um ótimo dia! Volte sempre!"
            "Se precisar de mais alguma coisa, estarei por aqui. Até a próxima!"
            "Obrigado por conversar! Até breve!"
            "Que bom ter ajudado, até a próxima!"
            "Foi bom falar com você! Tenha um ótimo dia!"
            "Volte sempre que precisar! Até logo!"
            "Obrigado pela conversa! Espero que tenha uma ótima semana!"
            "Fico feliz em ter ajudado! Até a próxima!"
            "Estarei por aqui se precisar, volte quando quiser! Até mais!"
            "Foi um prazer ajudar! Até a próxima!"
            "Tenha um ótimo dia e até mais!"
            "Volte sempre que precisar, ficarei à disposição!"
            "Que bom que pude te ajudar! Até a próxima conversa!"
            "Espero que você tenha uma ótima semana! Até logo!"
            "Sempre bom falar com você! Até a próxima!"
        ]

    def iteracao_ram(self):
        return random.choice(self.saudacoes)

    def say_goodbye(self):
        return random.choice(self.despedidas)
