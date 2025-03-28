# Use uma imagem base do Python
FROM python:3.13.2-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Defina o comando para executar o aplicativo
CMD ["python", "InterfaceGrafic.py"]
