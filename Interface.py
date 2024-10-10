from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot

teste = interacaoChatBot()
print(teste.iteracao_ram())

# Entrada do usuário
prompt = input("Digite sua pergunta: ")
    
# Gerar resposta do chatbot
conversa = GerarConteudo(prompt)
textogerado = conversa.gerarTexto()
print(textogerado)
    
# Despedida
print(teste.say_goodbye())