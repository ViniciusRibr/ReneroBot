from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot

teste = interacaoChatBot
perguntas = test
prompt = input("Olá, o que vamos aprender hojê?")
conversa = GerarConteudo(prompt)
textogerado = conversa.gerarTexto()

print(textogerado)