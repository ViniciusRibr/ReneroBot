import customtkinter as ctk
from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot
chat_interaction = interacaoChatBot()

def iniciar_chat():
    #Limpa a tela inicial
    for widget in app.winfo_children():
        widget.destroy()
    app.geometry("500x700")
    hello = chat_interaction.iteracao_ram()
    chat_box = ctk.CTkTextbox(app, width=400, height=500)
    chat_box.pack(padx=20, pady=20)
    chat_box.insert("end", f"ChatBot: {hello}\n")
    chat_box.see("end")

    #Estrada de texto
    user_input = ctk.CTkEntry(app, placeholder_text="Digite sua mensagem aqui..", width=350)
    user_input.pack(padx=20, pady=10, side="left")

    #Botão de envio
    send_button = ctk.CTkButton(app, text="Enviar", command=lambda: send_message(chat_box , user_input))
    send_button.pack(padx=10 , pady=10, side="left")

def send_message(cha_box, user_input):
    # Pega o texto digitado pelo usuário
    mensagem = user_input.get()

    #Exibe a mensagem na caixa de texto
    if mensagem:
        chat_box.insert("end", f"Você : {mensagem}\n")
        chat_box.see("end")
        user_input.delete(0 , "end")

        #Integração com a API
        conversa = GerarConteudo(mensagem)
        resposta = conversa.gerarTexto()

        #Exibe a mensagem do ChatBot
        chat_box.insert("end", f"Chatbot: {resposta}\n")        
        chat_box.see("end")

def button_callback():
    print("Button pressed")

app = ctk.CTk()
app.geometry("400x600")
app.title("Meu WhatsApp")
app.title("ReneroBot")

button = ctk.CTkButton(app, text="my button", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)
button.pack(expand=True)

app.mainloop()
