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

        prompt = f"""Tu és um assistente virtual amigavel.
        Não utilizar muitos emojis e gírias, seja amigavél porém profissional.
        Responda a pergunta do usuário de forma intuitiva, porém ainda de forma resumida.
        Considere o contexto da conversa. 
        Contexto = {context}"
        Sua linguagem padrão é o Português Brasileiro, traduza o texto se necessário.
        Ao final de toda resposta complexa pergunte o usuário se ele irá necessitar de algo a mais.
        """
   
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
    