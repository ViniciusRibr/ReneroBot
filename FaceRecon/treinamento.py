import cv2
import os
import numpy as np

# Configuração do classificador Haar
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # Carrega o classificador Haar Cascade padrão
reconhecedor = cv2.face.EigenFaceRecognizer_create()


# Caminho para salvar o classificador treinado
caminho_arquivo = "classificadorEigen.yml"

# Diretório onde as imagens de treinamento estão armazenadas
diretorio_imagens = "fotos"  # ou qualquer outro diretório que você tenha

# Função para capturar imagens para treinamento
def coletar_imagens():
    """Captura imagens para treinamento e retorna os dados necessários"""
    faces = []
    ids = []

    for diretorio in os.listdir(diretorio_imagens):
        caminho_imagens = os.path.join(diretorio_imagens, diretorio)
        if os.path.isdir(caminho_imagens):
            for arquivo in os.listdir(caminho_imagens):
                if arquivo.endswith(".jpg") or arquivo.endswith(".png"):
                    caminho_imagem = os.path.join(caminho_imagens, arquivo)
                    imagem = cv2.imread(caminho_imagem)
                    imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

                    # Detecta faces na imagem
                    faces_detectadas = face_cascade.detectMultiScale(imagem_gray, scaleFactor=1.1, minNeighbors=5)

                    for (x, y, w, h) in faces_detectadas:
                        imagem_face = cv2.resize(imagem_gray[y:y+h, x:x+w], (220, 220))
                        faces.append(imagem_face)
                        ids.append(int(diretorio))  # A pasta do usuário será o ID

    return np.array(faces), np.array(ids)

# Treina o modelo
faces, ids = coletar_imagens()
reconhecedor.train(faces, ids)

# Salva o classificador treinado
reconhecedor.write(caminho_arquivo)
print(f"Classificador treinado e salvo em: {caminho_arquivo}")

