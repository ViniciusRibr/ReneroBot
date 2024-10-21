from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot

gerador_conteudo = GerarConteudo()
teste = interacaoChatBot()
print(teste.iteracao_ram())

while True:
    prompt = input("Digite sua pergunta, (Ou digite 'sair' para encerrar.): ")
  
    #Gera resposta do chatbot
    try:
        textogerado = gerador_conteudo.gerarTexto(prompt)
        print(textogerado)

        # Verifica se há uma resposta válida antes de imprimir
        if textogerado:
            print(textogerado)
        else:
            print("Não foi possível gerar uma resposta.")
    except Exception as e:
        print(f"Ocorreu um erro ao gerar a resposta: {e}")
    