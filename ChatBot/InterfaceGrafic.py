import json
import customtkinter as ctk
import ctypes
import cv2
import os
from PIL import Image

from chatbot import GerarConteudo
from Perguntas import interacaoChatBot
gerador_conteudo = GerarConteudo()
chat_interaction = interacaoChatBot()

import RecFacial

# Tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

tema_atual = "dark"
# Alternar temas
def theme():
    global tema_atual
    if tema_atual == "dark":
        ctk.set_appearance_mode("light")
        tema_atual = "light"
    else:
        ctk.set_appearance_mode("dark")
        tema_atual = "dark"

def iniciar_chat():
    global chat_box
    global user_input
    global send_button
    global hello
    for widget in app.winfo_children():
        widget.destroy()
    app.geometry("500x650")
    app.resizable(False, False)
    hello = chat_interaction.iteracao_ram()

    # Main Frame
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(fill="both", expand=True)
    # Caixa de chat
    chat_box = ctk.CTkTextbox(main_frame, width=400, height=520, font=fonte_2, corner_radius=16, border_width=10, border_color="#343541")
    chat_box.tag_config("Usuário", background="#444444", foreground="white", lmargin1=5, rmargin=20, justify="right") 
    chat_box.tag_config("ChatBot", background="#202123", foreground="white", lmargin1=5, rmargin=5)
    chat_box.pack(padx=20, pady=(20, 0))


# Saudações
    display_dynamic_text(chat_box, f"🤖 ChatBot: {hello}\n", "ChatBot")

    # Campo de entrada do usuário
    user_input = ctk.CTkEntry(app, placeholder_text="Digite sua mensagem aqui..", width=350, font=fonte_2, corner_radius=20, border_color="#202123")
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
    frame_icones = ctk.CTkFrame(main_frame, width=50, fg_color="transparent")
    frame_icones.place(relx=0, rely=0)  # Sobreposição total

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
def display_dynamic_text(chat_box, text, tag, delay=2):
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
    
def verificar_nome_e_iniciar():
    # Verifica se o nome foi salvo corretamente
    user_name = carregar_nome()
    if user_name:
        # Se o nome já foi carregado, tenta reconhecer a face e iniciar o chat
        if reconhecer_usuario():  # Verifica se o reconhecimento facial foi bem-sucedido
            iniciar_chat()
    else:
        # Se o nome não foi encontrado, solicita para o usuário inserir
        display_nome_input()

def display_nome_input():
    # Função para exibir a tela de inserção do nome
    global label_nome, entry_nome, button_confirmar_nome  # Tornando as variáveis globais
    label_nome = ctk.CTkLabel(frame_central, text="Digite seu nome:", font=(fonte_3, 15))
    label_nome.pack(pady=(20, 5))
    entry_nome = ctk.CTkEntry(frame_central, placeholder_text="Seu nome", font=(fonte_2, 14))
    entry_nome.pack(pady=10, padx=20)
    button_confirmar_nome = ctk.CTkButton(frame_central, text="Iniciar", font=(fonte_1, 14), command=confirmar_nome, corner_radius=70, fg_color="#362580", border_color="#1E163F")
    button_confirmar_nome.pack(pady=20)

def confirmar_nome():
    nome = entry_nome.get().strip()
    if nome:
        global user_name
        user_name = nome
        salvar_nome(user_name)

        # Inicia o reconhecimento facial e salva a face
        face_salva = RecFacial.capturar_face(nome)  # Função para salvar a face do usuário
        if face_salva:
            label_nome.pack_forget()  # Remove a entrada de nome
            entry_nome.pack_forget()
            button_confirmar_nome.pack_forget()

            # Após salvar a face, inicie o chat
            iniciar_chat()
        else:
            error_label = ctk.CTkLabel(app, text="Erro ao capturar a face. Tente novamente.", font=(fonte_2, 12), text_color="red")
            error_label.pack(pady=(10, 0))
            app.after(3000, error_label.destroy)  # Remove a mensagem após 3 segundos
    else:
        # Exibe uma mensagem de erro se o nome estiver vazio
        error_label = ctk.CTkLabel(app, text="Por favor, insira um nome válido.", font=(fonte_2, 12), text_color="red")
        error_label.pack(pady=(10, 0))
        app.after(3000, error_label.destroy)  # Remove a mensagem após 3 segundos

# Função para realizar o reconhecimento facial na segunda vez
def reconhecer_usuario():
    nome = carregar_nome()
    if nome:
        face_reconhecida = RecFacial.reconhecer_face()  # Função de reconhecimento facial
        if face_reconhecida:
            return True  # Retorna True se o reconhecimento for bem-sucedido
        else:
            error_label = ctk.CTkLabel(app, text="Face não reconhecida. Tente novamente.", font=(fonte_2, 12), text_color="red")
            error_label.pack(pady=(10, 0))
            app.after(3000, error_label.destroy)  # Remove a mensagem após 3 segundos
    else:
        # Se o nome não foi salvo
        error_label = ctk.CTkLabel(app, text="Nome não encontrado. Tente inserir novamente.", font=(fonte_2, 12), text_color="red")
        error_label.pack(pady=(10, 0))
        app.after(3000, error_label.destroy)  # Remove a mensagem após 3 segundos
    return False  # Retorna False se o reconhecimento falhar


app = ctk.CTk()
app.geometry("640x480")
app.title("ReneroBot")
myappid = "meuNome.meuChatbot.interface.v1"  # Exemplo de ID único
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
app.iconbitmap("imagens/favicon.ico")
app.resizable(False, False)

# Fontes
fonte_1 = ctk.CTkFont(family="COCOMAT", size=14)
fonte_2 = ctk.CTkFont(family="Inter 18pt Medium", size=13)
fonte_3 = ctk.CTkFont(family="Michroma", size=15)
fonte_emoji = ctk.CTkFont(family="Inter", size=24)  # Fonte maior para o emoji de lixeira

# Background
cap = cv2.VideoCapture("imagens/background.mp4")
# Frame para exibir o vídeo
video_frame = ctk.CTkLabel(app)
video_frame.place(x=0, y=0)  # Tamanho fixo do vídeo

def exibir_frame():
    ret, frame = cap.read()
    if ret:
        # Converte BGR para RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Converte para imagem PIL
        frame_image = Image.fromarray(frame)
        # Cria uma CTkImage a partir da imagem PIL
        frame_image_tk = ctk.CTkImage(light_image=frame_image, size=(640, 480))
        # Atualiza o frame no widget
        video_frame.configure(image=frame_image_tk)
        video_frame.image = frame_image_tk
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia o vídeo

    app.after(33, exibir_frame)  # 30 FPS (aproximado)

exibir_frame()


# Tela inicial
frame_central = ctk.CTkFrame(app) 
frame_central.pack(expand=True)
user_name = carregar_nome()

# Verifica se o nome foi carregado ou se precisa ser inserido
app.after(100, verificar_nome_e_iniciar)  # Atrasando a execução para garantir que a interface esteja pronta

app.mainloop()
cap.release()
