import customtkinter as ctk
from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot
from PIL import Image

gerador_conteudo = GerarConteudo()
chat_interaction = interacaoChatBot()


def iniciar_chat():
    #Limpa a tela inicial
    for widget in app.winfo_children():
        widget.destroy()
    app.geometry("500x700")
    hello = chat_interaction.iteracao_ram()
    chat_box = ctk.CTkTextbox(app, width=400, height=500, font=fonte_2)
    chat_box.pack(padx=20, pady=20)
    chat_box.insert("end", f"ChatBot: {hello}\n")
    chat_box.see("end")

    #Estrada de texto
    user_input = ctk.CTkEntry(app, placeholder_text="Digite sua mensagem aqui..", width=350, font=fonte_2)
    user_input.pack(padx=20, pady=10, side="left")

    send_image = Image.open("imagens/Sendimage2.png")  
    send_image_tk = ctk.CTkImage(light_image=send_image)

    #Botão de envio
    send_button = ctk.CTkButton(app, image=send_image_tk, command=lambda: send_message(chat_box , user_input),
                                text= "", fg_color=app.cget('bg'), hover_color=app.cget('bg'), border_width=0)
                                #Ajustar tamanho
    send_button.pack(padx=10, pady=10)
    send_button.pack(padx=10 , pady=10, side="left")
    user_input.bind("<Return>", lambda event: send_message(chat_box, user_input))


def send_message(chat_box, user_input):
    # Pega o texto digitado pelo usuário
    mensagem = user_input.get()

    #Exibe a mensagem na caixa de texto
    if mensagem:
        chat_box.insert("end", f"Você : {mensagem}\n")
        chat_box.see("end")
        user_input.delete(0 , "end")

        #Integração com a API
        resposta = gerador_conteudo.gerarTexto(mensagem)

        #Exibe a mensagem do ChatBot
        chat_box.insert("end", f"Chatbot: {resposta}\n")        
        chat_box.see("end")


app = ctk.CTk()
app.geometry("800x600")
app.title("ReneroBot")
app.iconbitmap("imagens/favicon.ico")

#Fontes
fonte_1 = ctk.CTkFont(family="COCOMAT", size=14)
fonte_2 = ctk.CTkFont(family="Inter 18pt Medium", size=12)

#Imagens
original_image = Image.open("imagens/1_.png")
resized_image = original_image.resize((800, 600), Image.Resampling.LANCZOS)

bg_image = ctk.CTkImage(light_image=resized_image, size=(800, 600))

#Criar um label com a imagem de fundo
bg_label = ctk.CTkLabel(app, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#Botão de iniciar Chat
button = ctk.CTkButton(app, text="Iniciar Chat", command=iniciar_chat, font=fonte_2)
button.pack(expand=True)

app.mainloop()
