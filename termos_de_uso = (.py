termos_de_uso = (
    "Termos de Uso do Chatbot: \n\n"
    "1. Este chatbot é fornecido para fins informativos e entretenimento.\n"
    "2. Ao utulizar este chatbot, você concorda em não compartilhar informações pessoais.\n"
    "3. O uso deste chatbot deve estar em conformidade com leis e regulamnetos aplicáveis.\n"
    "4. Nós não nos responsabilizamos por quaisquer danos ou perdas decorrentes do uso desse serviço.\n"
    "5. O uso inadequado do chatbot poderá resultar na interrupção do serviço.\n"
    "Você aceita os Termos?(sim/não)"
)

def aceitar_termos():
    while True:
        print(termos_de_uso)
        resposta = input("Digite 'sim' para aceitar ou 'não' para sair: ").strip().lower()
        
        
        if resposta =='sim':
            print("Você aceitou os Termos de Uso. Bem-Vindo ao chatbot!")
            return True
        elif resposta == 'não':
            print("Você não aceitou os Termos de Uso. Encerrando a interação.")
            return False
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")
            
            
def chatbot():
    if aceitar_termos():
        print("Como posso te ajudar hoje?")
        while True:
            mensagem = input("Você:").strip().lower()
            if mensagem == 'sair':
                print("Encerrando a interação. Até a próxima!")
                break
            else:
                print(f"Chatbot: Você disse '{mensagem}'")
        else:
            print("Tchau!")
chatbot()