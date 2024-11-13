import customtkinter as ctk
from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot
from PIL import Image

gerador_conteudo = GerarConteudo()
chat_interaction = interacaoChatBot()

# Tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def iniciar_chat():
    for widget in app.winfo_children():
        widget.destroy()
    app.geometry("500x700")
    hello = chat_interaction.iteracao_ram()

    # Caixa de chat
    chat_box = ctk.CTkTextbox(app, width=400, height=500, font=fonte_2)
    chat_box.tag_config("Usuário", background="#444444", foreground="white", lmargin1=5, rmargin=20, justify="right")
    chat_box.tag_config("ChatBot", background="#222222", foreground="white", lmargin1=5, rmargin=5)
    chat_box.pack(padx=20, pady=(20, 0))

    # Saudações
    chat_box.insert("end", "🤖 ChatBot: ", "ChatBot")
    chat_box.insert("end", f"{hello}\n", "ChatBot")

    # Campo de entrada do usuário
    user_input = ctk.CTkEntry(app, placeholder_text="Digite sua mensagem aqui..", width=350, font=fonte_2)
    user_input.pack(side="left", padx=(20, 10), pady=10)

    # Botão de envio
    send_image = Image.open("imagens/Sendimage2.png").resize((35, 35), Image.Resampling.LANCZOS)
    send_image_tk = ctk.CTkImage(light_image=send_image, size=(35, 35))
    send_button = ctk.CTkButton(app, text="", image=send_image_tk, command=lambda: send_message(chat_box, user_input),
                                fg_color=app.cget('bg'), hover_color=app.cget('bg'), width=40, height=40)
    send_button.pack(side="left", padx=(35), pady=10)


    # Envia a mensagem após apertar "Enter"
    user_input.bind("<Return>", lambda event: send_message(chat_box, user_input))


    # Envia a mensagem após apertar "Enter"
    user_input.bind("<Return>", lambda event: send_message(chat_box, user_input))


def send_message(chat_box, user_input):
    mensagem = user_input.get()

    # Exibe a mensagem do usuário na caixa de texto
    if mensagem:
        chat_box.insert("end", f"Você: {mensagem}\n", "Usuário")
        chat_box.see("end")
        user_input.delete(0, "end")

        # Integração com a API
        resposta = gerador_conteudo.gerarTexto(mensagem)

        #Exibe a mensagem do ChatBot
        label_img = ctk.CTkLabel(chat_box)
        label_img.pack(side="left", padx=5) 
        chat_box.insert("end", f"Chatbot: {resposta}\n", )      

        # Exibe a mensagem do bot
        chat_box.insert("end", "🤖 ChatBot: ", "ChatBot")
        chat_box.insert("end", f"{resposta}\n", "ChatBot")

        chat_box.see("end")

app = ctk.CTk()
app.geometry("800x600")
app.title("ReneroBot")
app.iconbitmap("imagens/favicon.ico")

# Fontes
fonte_1 = ctk.CTkFont(family="COCOMAT", size=14)
fonte_2 = ctk.CTkFont(family="Inter 18pt Medium", size=12)

# Imagem de fundo
original_image = Image.open("imagens/1_.png").resize((800, 600), Image.Resampling.LANCZOS)
bg_image = ctk.CTkImage(light_image=original_image, size=(800, 600))
# Label com a imagem de fundo
bg_label = ctk.CTkLabel(app, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Botão para iniciar o chat
button = ctk.CTkButton(app, text="Iniciar Chat", command=iniciar_chat, font=fonte_2)
button.pack(expand=True)

app.mainloop()
