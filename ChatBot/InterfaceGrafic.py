import json
import customtkinter as ctk
import ctypes
from PIL import Image

from chatbot import GerarConteudo
from Perguntas import interacaoChatBot
gerador_conteudo = GerarConteudo()
chat_interaction = interacaoChatBot()

# Tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Alternar temas
tema_atual = "dark"
def theme():
    global tema_atual
    if tema_atual == "dark":
        ctk.set_appearance_mode("light")
        tema_atual = "light"
    else:
        ctk.set_appearance_mode("dark")
        tema_atual = "dark"

def maximizar():
    app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")

def iniciar_chat():
    global chat_box
    global user_input
    global send_button
    global hello
    for widget in app.winfo_children():
        widget.destroy()
    app.geometry("500x700")
    app.resizable(False, False)
    hello = chat_interaction.iteracao_ram()

    # Main Frame
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(fill="both", expand=True)
    # Caixa de chat
    chat_box = ctk.CTkTextbox(main_frame, width=400, height=520, font=fonte_2)
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

    # Frame para icones a esquerda
    frame_icones = ctk.CTkFrame(main_frame, width=50)
    frame_icones.place(relx=0, rely=0)  # Sobreposição total
    frame_icones.pack_propagate(True)
    # Botão de maximizar tela
    maximizar_btn = ctk.CTkButton(frame_icones, text="🗖", font=fonte_emoji, command=maximizar,
                                fg_color="transparent", hover_color="#444444", width=40, height=40)
    maximizar_btn.pack(pady=(10, 5))
    # Botão de trocar tema                   
    btn_tema = ctk.CTkButton(frame_icones, text="🌗", font=fonte_emoji, command=theme,
                         fg_color="transparent", hover_color="#444444", width=40, height=40)
    btn_tema.pack(pady=(5, 5))

    # Botão de lixeira
    clear_icon = ctk.CTkButton(frame_icones, text="🗑", font=fonte_emoji, command=clear_chat,
                               fg_color="transparent", hover_color="#444444", width=40, height=40)
    clear_icon.pack(pady=(5, 10)) 


def send_message(chat_box, user_input):
    mensagem = user_input.get()

    # Exibe a mensagem do usuário na caixa de texto
    if mensagem:
        chat_box.insert("end", f"{mensagem}\n", "Usuário")
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
    display_dynamic_text(chat_box, f"🤖 ChatBot: {hello}\n", "ChatBot")

def salvar_nome(nome):
    try:
        with open("usuario.json", "w") as arquivo:
            json.dump({"nome": nome}, arquivo)
        print(f"Nome '{nome}' salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar nome {e}")


# Função para verificar se o nome já foi salvo
def carregar_nome():
    try:
        with open("usuario.json", "r") as arquivo:
            dados = json.load(arquivo)
            return dados.get("nome", None)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo JSON.")
        return None

def confirmar_nome():
    nome = entry_nome.get().strip()
    if nome:  # Verifica se o nome foi inserido
        global user_name
        user_name = nome
        salvar_nome(user_name)
        label_nome.pack_forget()  # Remove a entrada de nome
        entry_nome.pack_forget()
        button_confirmar_nome.pack_forget()
        iniciar_chat()  # Inicia o chat com o nome definido
    else:
        # Exibe uma mensagem de erro se o nome estiver vazio
        error_label = ctk.CTkLabel(app, text="Por favor, insira um nome válido.", font=(fonte_2, 12), text_color="red")
        error_label.pack(pady=(10, 0))
        app.after(3000, error_label.destroy)  # Remove a mensagem após 3 segundos


app = ctk.CTk()
app.geometry("700x700")
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


# Tela inicial
frame_central = ctk.CTkFrame(app) 
frame_central.pack(expand=True)
user_name = carregar_nome()
# Definir nome de usuário
if user_name:
    iniciar_chat()
else:
    label_nome = ctk.CTkLabel(frame_central, text="Digite seu nome:", font=(fonte_2, 16))
    label_nome.pack(pady=(20, 5))
    entry_nome = ctk.CTkEntry(frame_central, placeholder_text="Seu nome", font=(fonte_2, 14))
    entry_nome.pack(pady=10, padx=20)
    button_confirmar_nome = ctk.CTkButton(frame_central, text="Iniciar", font=(fonte_2, 14), command=confirmar_nome)
    button_confirmar_nome.pack(pady=20)

app.mainloop()