from flask import Flask, request, jsonify
from chatbot import GerarConteudo

# Inicializar Flask e ChatBot
app = Flask(__name__)
chatbot = GerarConteudo()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json  # Obter os dados enviados no corpo da requisição
    mensagem = data.get("mensagem")  # Capturar a mensagem do usuário

    if not mensagem:
        return jsonify({"erro": "Nenhuma mensagem fornecida."}), 400

    # Gerar resposta usando o ChatBot
    resposta = chatbot.gerarTexto(mensagem)

    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(debug=True)
