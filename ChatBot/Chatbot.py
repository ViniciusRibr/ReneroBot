import google.generativeai as genai

class GerarConteudo:
    def __init__(self):
        self.conversa = []
        genai.configure(api_key="AIzaSyC2Or3aeQYbH_OSzLxqs-Yd0nRmMYTjNsQ")
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def gerarTexto(self, entrada):
        self.conversa.append(f"Usuário: {entrada}")

        context_max = 15
        context = ' '.join(self.conversa[-context_max:])

        prompt = f"""Você é um assistente virtual amigável e profissional. Responda de forma direta e sem saudações ou introduções nas respostas, exceto na primeira interação do usuário. Concentre-se em responder o conteúdo da mensagem, considerando o contexto de conversas anteriores.
        Considere o seguinte contexto: {context}
        Idioma padrão: Português Brasileiro. Traduza o texto se necessário. Evite repetir saudações e introduções; seja amigável, mas sem utilizar muitos emojis ou gírias.

        Se a resposta for complexa, pergunte ao final se o usuário necessita de algo mais."""

   
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=[""],
                max_output_tokens=2000,
                temperature=1.0,
            )
        )
        self.conversa.append(f"Assistente: {response.text}")
        return response.text
    