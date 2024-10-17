from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot

teste = interacaoChatBot()
print(teste.iteracao_ram())

while True:
    # Entrada do usuário
    prompt = input("Digite sua pergunta, (Ou digite 'sair' para encerrar.): ")
    
    if prompt.lower() == 'sair':
        print(teste.say_goodbye())  # Exibe a despedida
        break  # Encerra o loop

    # Gerar resposta do chatbot
    try:
        conversa = GerarConteudo(prompt)
        textogerado = conversa.gerarTexto()
        print(textogerado)

        # Verifica se há uma resposta válida antes de imprimir
        if textogerado:
            print(textogerado)
        else:
            print("Não foi possível gerar uma resposta.")
    except Exception as e:
        print(f"Ocorreu um erro ao gerar a resposta: {e}")
    