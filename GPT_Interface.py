import customtkinter as ctk
from Chatbot import GerarConteudo  # Importa o chatbot real
from Perguntas import interacaoChatBot  # Importa a classe de interações do chatbot

# Cria uma instância da classe de interações
chat_interaction = interacaoChatBot()

def iniciar_chat():
    # Limpa a tela inicial
    for widget in app.winfo_children():
        widget.destroy()

    # Cria uma nova interface para o chat
    app.geometry("500x700")

    # Exibe uma saudação aleatória
    saudacao = chat_interaction.iteracao_ram()
    chat_box = ctk.CTkTextbox(app, width=400, height=500)
    chat_box.pack(padx=20, pady=20)
    chat_box.insert("end", f"Chatbot: {saudacao}\n")
    chat_box.see("end")

    # Entrada de texto para o usuário digitar a mensagem
    user_input = ctk.CTkEntry(app, placeholder_text="Digite sua mensagem aqui...", width=350)
    user_input.pack(padx=20, pady=10, side="left")

    # Botão de enviar mensagem
    send_button = ctk.CTkButton(app, text="Enviar", command=lambda: enviar_mensagem(chat_box, user_input))
    send_button.pack(padx=10, pady=10, side="left")

def enviar_mensagem(chat_box, user_input):
    # Pega o texto digitado pelo usuário
    mensagem = user_input.get()

    if mensagem:
        # Exibe a mensagem na caixa de texto
        chat_box.insert("end", f"Você: {mensagem}\n")
        chat_box.see("end")  # Faz a rolagem para o final da caixa de texto
        user_input.delete(0, "end")  # Limpa a entrada de texto

        # --- Integração com o chatbot real ---
        # Gera uma resposta usando a Gemini API
        conversa = GerarConteudo(mensagem)
        resposta = conversa.gerarTexto()

        # Exibe a resposta do chatbot na caixa de texto
        chat_box.insert("end", f"Chatbot: {resposta}\n")
        chat_box.see("end")

# Função para sair do chat
def sair_chat():
    despedida = chat_interaction.say_goodbye()
    chat_box.insert("end", f"Chatbot: {despedida}\n")
    chat_box.see("end")

    # Limpa a interface de chat
    for widget in app.winfo_children():
        widget.destroy()
    
    # Retorna à tela inicial ou faz outras ações necessárias

# Janela principal do app
app = ctk.CTk()
app.geometry("400x600")
app.title("ReneroBot")

# Botão de iniciar chat
button = ctk.CTkButton(app, text="Iniciar Chat", command=iniciar_chat)
button.pack(expand=True)

# Para adicionar a funcionalidade de sair do chat, você pode criar um botão separado.
exit_button = ctk.CTkButton(app, text="Sair do Chat", command=sair_chat)
exit_button.pack(pady=10)

app.mainloop()
