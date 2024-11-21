from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API está funcionando! Acesse as rotas específicas para interagir com o chatbot."

@app.route("/gerar-conteudo", methods=["POST"])
def gerar_conteudo():
    data = request.get_json()
    mensagem = data.get("mensagem")
    if not mensagem:
        return jsonify({"erro": "Mensagem não fornecida"}), 400

    # Lógica do chatbot
    try:
        resposta = "Resposta gerada pelo Chatbot: " + mensagem  # Substitua pela lógica real
        return jsonify({"resposta": resposta})
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
