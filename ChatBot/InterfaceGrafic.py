"""
InterfaceGrafic.py - CustomTkinter Graphical User Interface for ReneroBot.

This module builds the desktop GUI for ReneroBot using CustomTkinter, OpenCV for
the animated background video, PIL for image processing, and multithreading to keep
the GUI non-blocking during Gemini API calls.
"""

import os
import sys
import json
import ctypes
import threading
from typing import Optional
from PIL import Image
import cv2
import customtkinter as ctk

from ChatBot.chatbot import GerarConteudo
from ChatBot.Perguntas import InteracaoChatBot

# Initialize global AI generator and greeting helper
gerador_conteudo = GerarConteudo()
chat_interaction = InteracaoChatBot()

# Application Appearance Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Global UI state
tema_atual = "dark"
USO_PATH = "usuario.json"
hello = ""


def toggle_theme() -> None:
    """Toggles the GUI appearance mode between dark and light themes."""
    global tema_atual
    if tema_atual == "dark":
        ctk.set_appearance_mode("light")
        tema_atual = "light"
    else:
        ctk.set_appearance_mode("dark")
        tema_atual = "dark"


def salvar_nome(nome: str) -> None:
    """
    Saves the user's name to a local JSON file for session persistence.

    :param nome: The username to save.
    """
    try:
        with open(USO_PATH, "w", encoding="utf-8") as arquivo:
            json.dump({"nome": nome}, arquivo)
        print(f"Nome '{nome}' salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar nome: {e}")


def carregar_nome() -> Optional[str]:
    """
    Loads saved username from local JSON file if present.

    :return: Username string or None if not found.
    """
    try:
        with open(USO_PATH, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados.get("nome", None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def display_dynamic_text(chat_box: ctk.CTkTextbox, text: str, tag: str, delay: int = 2) -> None:
    """
    Renders text in the chat textbox with a typewriter effect.

    :param chat_box: The CustomTkinter CTkTextbox widget.
    :param text: Text string to insert.
    :param tag: Text formatting tag ('Usuário' or 'ChatBot').
    :param delay: Milliseconds delay between each character.
    """
    index = 0

    def type_next_character() -> None:
        nonlocal index
        if index < len(text):
            chat_box.insert("end", text[index], tag)
            chat_box.see("end")
            index += 1
            app.after(delay, type_next_character)

    type_next_character()


def send_message(chat_box: ctk.CTkTextbox, user_input: ctk.CTkEntry, send_button: ctk.CTkButton) -> None:
    """
    Handles sending user message, updating chat box, and fetching AI response asynchronously.

    :param chat_box: The chat box widget.
    :param user_input: The entry widget containing user prompt.
    :param send_button: The submit button to disable/enable during requests.
    """
    mensagem = user_input.get().strip()
    if not mensagem:
        return

    # Display user input in chat box
    chat_box.insert("end", f"Você: {mensagem}\n", "Usuário")
    chat_box.see("end")
    user_input.delete(0, "end")

    # Disable send button while generating response
    send_button.configure(state="disabled")

    def worker():
        resposta = gerador_conteudo.gerar_texto(mensagem)
        # Schedule response display on the main GUI thread
        app.after(0, lambda: on_response_ready(resposta))

    def on_response_ready(resposta: str):
        display_dynamic_text(chat_box, f"🤖 ReneroBot: {resposta}\n\n", "ChatBot")
        send_button.configure(state="normal")

    # Execute API call in a background daemon thread to avoid freezing GUI
    threading.Thread(target=worker, daemon=True).start()


def clear_chat() -> None:
    """Clears the chat box and re-displays an initial greeting."""
    global hello, chat_box
    if 'chat_box' in globals():
        chat_box.delete("1.0", "end")
        chat_interaction.saudacao_enviada = False
        hello = chat_interaction.obter_saudacao()
        display_dynamic_text(chat_box, f"🤖 ReneroBot: {hello}\n\n", "ChatBot")


def iniciar_chat() -> None:
    """Initializes and displays the main chatbot conversational screen."""
    global chat_box, user_input, send_button, hello

    # Clear initial screen widgets
    for widget in app.winfo_children():
        widget.destroy()

    app.geometry("500x650")
    app.resizable(False, False)

    hello = chat_interaction.obter_saudacao()

    # Main Container Frame
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(fill="both", expand=True)

    # Chat Text Display Box
    chat_box = ctk.CTkTextbox(
        main_frame,
        width=440,
        height=520,
        font=fonte_2,
        corner_radius=16,
        border_width=2,
        border_color="#343541"
    )
    chat_box.tag_config("Usuário", background="#444444", foreground="white", lmargin1=5, rmargin=20, justify="right")
    chat_box.tag_config("ChatBot", background="#202123", foreground="white", lmargin1=5, rmargin=5)
    chat_box.pack(padx=20, pady=(20, 0))

    # Display welcome greeting
    display_dynamic_text(chat_box, f"🤖 ReneroBot: {hello}\n\n", "ChatBot")

    # User Input Entry Widget
    user_input = ctk.CTkEntry(
        app,
        placeholder_text="Digite sua mensagem aqui...",
        width=350,
        font=fonte_2,
        corner_radius=20,
        border_color="#202123"
    )
    user_input.pack(side="left", padx=(20, 10), pady=10)

    # Load Send Icon
    try:
        send_image = Image.open("imagens/Sendimage.png").resize((35, 35), Image.Resampling.LANCZOS)
        send_image_tk = ctk.CTkImage(light_image=send_image, size=(35, 35))
    except Exception as e:
        print(f"Icon missing: {e}")
        send_image_tk = None

    # Send Button Widget
    send_button = ctk.CTkButton(
        app,
        text="➤" if not send_image_tk else "",
        image=send_image_tk,
        command=lambda: send_message(chat_box, user_input, send_button),
        fg_color=app.cget('bg'),
        hover_color="#343541",
        width=40,
        height=40
    )
    send_button.pack(side="left", padx=(10), pady=10)

    # Bind Return Key to Send Message
    user_input.bind("<Return>", lambda event: send_message(chat_box, user_input, send_button))

    # Sidebar Icon Frame
    frame_icones = ctk.CTkFrame(main_frame, width=50, fg_color="transparent")
    frame_icones.place(relx=0, rely=0)

    # Theme Toggle Button
    btn_tema = ctk.CTkButton(
        frame_icones,
        text="🌗",
        font=fonte_emoji,
        command=toggle_theme,
        fg_color="transparent",
        hover_color="#444444",
        width=40,
        height=40
    )
    btn_tema.pack(pady=(5, 5))

    # Clear Chat Button
    clear_icon = ctk.CTkButton(
        frame_icones,
        text="🗑",
        font=fonte_emoji,
        command=clear_chat,
        fg_color="transparent",
        hover_color="#444444",
        width=40,
        height=40
    )
    clear_icon.pack(pady=(5, 10))


def exibir_mensagem_erro(mensagem: str) -> None:
    """Displays temporary validation error message on initial screen."""
    error_label = ctk.CTkLabel(app, text=mensagem, font=ctk.CTkFont(size=12), text_color="red")
    error_label.pack(pady=(10, 0))
    app.after(3000, error_label.destroy)


def confirmar_nome() -> None:
    """Validates user name input on splash screen and proceeds to chat."""
    if 'entry_nome' in globals():
        nome = entry_nome.get().strip()
        if nome:
            salvar_nome(nome)
            iniciar_chat()
        else:
            exibir_mensagem_erro("Por favor, insira um nome válido.")


# Initialize Root Window
app = ctk.CTk()
app.geometry("640x480")
app.title("ReneroBot - Assistant")

# Windows specific AppUserModelID configuration safely wrapped
if sys.platform == "win32":
    try:
        myappid = "meuNome.meuChatbot.interface.v1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        print(f"Notice: Unable to set AppUserModelID: {e}")

# Favicon configuration if exists
if os.path.exists("imagens/favicon.ico"):
    try:
        app.iconbitmap("imagens/favicon.ico")
    except Exception:
        pass

app.resizable(False, False)

# Fonts definition
fonte_1 = ctk.CTkFont(family="COCOMAT", size=14)
fonte_2 = ctk.CTkFont(family="Inter", size=13)
fonte_3 = ctk.CTkFont(family="Michroma", size=15)
fonte_emoji = ctk.CTkFont(family="Inter", size=24)

# Video Background Stream setup
video_path = "imagens/Background.mp4"
cap = cv2.VideoCapture(video_path) if os.path.exists(video_path) else None
video_frame = ctk.CTkLabel(app, text="")
video_frame.place(x=0, y=0)


def exibir_frame() -> None:
    """Continuously reads video frames and updates background label."""
    if cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame)
            frame_image_tk = ctk.CTkImage(light_image=frame_image, size=(640, 480))
            video_frame.configure(image=frame_image_tk)
            video_frame.image = frame_image_tk
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    app.after(33, exibir_frame)


if cap:
    exibir_frame()

# Initial Splash / Name Registration Screen
frame_central = ctk.CTkFrame(app, corner_radius=30, fg_color="transparent")
frame_central.pack(expand=True)

user_name = carregar_nome()
if user_name:
    iniciar_chat()
else:
    label_nome = ctk.CTkLabel(frame_central, text="Digite seu nome:", font=(fonte_2, 16))
    label_nome.pack(pady=(20, 5))
    entry_nome = ctk.CTkEntry(frame_central, placeholder_text="Seu nome", font=(fonte_1, 14), corner_radius=15)
    entry_nome.pack(pady=10, padx=20)
    button_confirmar_nome = ctk.CTkButton(
        frame_central,
        text="Iniciar",
        font=(fonte_3, 14),
        command=confirmar_nome,
        corner_radius=20,
        fg_color="#2812b2",
        hover_color="#160969"
    )
    button_confirmar_nome.pack(pady=20)


def main():
    try:
        app.mainloop()
    finally:
        if cap and cap.isOpened():
            cap.release()


if __name__ == "__main__":
    main()
