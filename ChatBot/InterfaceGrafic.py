import customtkinter as ctk
import ctypes
from PIL import Image

from Chatbot import GerarConteudo
from Perguntas import interacaoChatBot
gerador_conteudo = GerarConteudo()
chat_interaction = interacaoChatBot()

# Tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def iniciar_chat():
    global chat_box
    global user_input
    global send_button
    for widget in app.winfo_children():
        widget.destroy()
    app.geometry("500x700")
    hello = chat_interaction.iteracao_ram()

    # Botão de lixeira
    clear_icon = ctk.CTkButton(app, text="🗑", font=fonte_emoji, command=clear_chat,
                               fg_color="transparent", hover_color="#444444", width=40, height=40)
    clear_icon.pack(pady=(10, 0)) 

    # Caixa de chat
    chat_box = ctk.CTkTextbox(app, width=400, height=500, font=fonte_2)
    chat_box.tag_config("Usuário", background="#444444", foreground="white", lmargin1=5, rmargin=20, justify="right")
    chat_box.tag_config("ChatBot", background="#222222", foreground="white", lmargin1=5, rmargin=5)
    chat_box.pack(padx=20, pady=(20, 0))

    # Saudações
    display_dynamic_text(chat_box, f"🤖 ChatBot: {hello}\n", "ChatBot")

    # Campo de entrada do usuário
    user_input = ctk.CTkEntry(app, placeholder_text="Digite sua mensagem aqui..", width=350, font=fonte_2)
    user_input.pack(side="left", padx=(20, 10), pady=10)

    # Botão de envio
    send_image = Image.open("imagens/Sendimage.png").resize((35, 35), Image.Resampling.LANCZOS)
    send_image_tk = ctk.CTkImage(light_image=send_image, size=(35, 35))
    send_button = ctk.CTkButton(app, text="", image=send_image_tk, command=lambda: send_message(chat_box, user_input),
                                fg_color=app.cget('bg'), hover_color=app.cget('bg'), width=40, height=40)
    send_button.pack(side="left", padx=(35), pady=10)
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

        # Exibe a mensagem do bot
        display_dynamic_text(chat_box, f"🤖 ChatBot: {resposta}\n", "ChatBot")

# Mostra o texto caractere por caractere
def display_dynamic_text(chat_box, text, tag, delay=3):
    index = 0

    def type_next_character():
        nonlocal index
        if index < len(text):
            chat_box.insert("end", text[index], tag)
            chat_box.see("end")
            index += 1
            app.after(delay, type_next_character)  # Aguarda o delay antes de exibir o próximo caractere

    type_next_character()

# Limpar mensagens
def clear_chat():
    chat_box.delete("1.0", "end")  # Limpa todo o conteúdo da chat_box

app = ctk.CTk()
app.geometry("800x600")
app.title("ReneroBot")
myappid = "meuNome.meuChatbot.interface.v1"  # Exemplo de ID único
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
app.iconbitmap("imagens/favicon.ico")

# Fontes
fonte_1 = ctk.CTkFont(family="COCOMAT", size=14)
fonte_2 = ctk.CTkFont(family="Inter 18pt Medium", size=12)
fonte_emoji = ctk.CTkFont(family="Inter", size=24)  # Fonte maior para o emoji de lixeira

# Imagem de fundo
original_image = Image.open("imagens/Background.png").resize((800, 600), Image.Resampling.LANCZOS)
bg_image = ctk.CTkImage(light_image=original_image, size=(800, 600))
# Label com a imagem de fundo
bg_label = ctk.CTkLabel(app, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Botão para iniciar o chat
button = ctk.CTkButton(app, text="Iniciar Chat", command=iniciar_chat, font=fonte_2)
button.pack(expand=True)

app.mainloop()
