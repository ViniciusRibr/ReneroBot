// URL do backend
const apiUrl = "http://127.0.0.1:5000/chat";

// Enviar mensagem para o Flask
async function enviarMensagem(mensagemUsuario) {
    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: mensagemUsuario })
        });

        if (response.ok) {
            const data = await response.json();
            return data.response; // Resposta do Flask
        } else {
            throw new Error("Erro ao se conectar ao servidor.");
        }
    } catch (error) {
        console.error(error);
        return "Desculpe, ocorreu um erro.";
    }
}

// Manipular envio de mensagem no frontend
document.getElementById("sendButton").addEventListener("click", async () => {
    const userMessage = document.getElementById("userInput").value;
    if (userMessage.trim() !== "") {
        adicionarMensagemNaTela("Você", userMessage); // Adiciona no chat
        const botResponse = await enviarMensagem(userMessage); // Chama o Flask
        adicionarMensagemNaTela("ChatBot", botResponse); // Exibe resposta
        document.getElementById("userInput").value = ""; // Limpa campo
    }
});

// Função para adicionar mensagens na tela
function adicionarMensagemNaTela(autor, mensagem) {
    const chatBox = document.getElementById("chatBox");
    const mensagemDiv = document.createElement("div");
    mensagemDiv.textContent = `${autor}: ${mensagem}`;
    mensagemDiv.classList.add(autor === "Você" ? "user-message" : "bot-message");
    chatBox.appendChild(mensagemDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Rola para a última mensagem
}
