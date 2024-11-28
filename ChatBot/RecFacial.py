import cv2
import os
import numpy as np

# Função para capturar a face do usuário e associar ao nome
def capturar_face(nome):
    # Criação de diretório para salvar a face
    face_dir = "faces"
    if not os.path.exists(face_dir):
        os.makedirs(face_dir)

    # Captura de imagens da face do usuário
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    face_id = nome  # Usar o nome do usuário como ID para salvar as imagens

    contador = 0
    largura, altura = 220, 220  # Tamanho da imagem da face
    faces = []

    print(f"Capturando rosto para {nome}...")
    while contador < 30:
        ret, imagem = camera.read()
        if not ret:
            print("Erro ao capturar a imagem da câmera.")
            break

        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faces_detectadas = face_cascade.detectMultiScale(imagem_cinza, scaleFactor=1.1, minSize=(100, 100))

        for (x, y, l, a) in faces_detectadas:
            imagem_face = cv2.resize(imagem_cinza[y:y + a, x:x + l], (largura, altura))
            caminho_arquivo = os.path.join(face_dir, f"{face_id}_{contador + 1}.jpg")
            cv2.imwrite(caminho_arquivo, imagem_face)
            faces.append(imagem_face)
            contador += 1

            # Exibir o rosto capturado
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 2)
            cv2.imshow("Captura de Rosto", imagem)

            if contador >= 30:
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    print(f"Captura de rosto para {nome} concluída.")

    # Treinar o modelo com as imagens capturadas
    reconhecedor = cv2.face.EigenFaceRecognizer_create()
    reconhecedor.train(faces, np.array([0] * len(faces)))  # Usando 0 como o ID para todas as faces

    # Salvar o modelo treinado
    modelo_path = "modelo_face.yml"
    reconhecedor.save(modelo_path)
    print(f"Modelo de reconhecimento facial salvo em: {modelo_path}")

# Função para reconhecer a face do usuário
def reconhecer_face():
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    reconhecedor = cv2.face.EigenFaceRecognizer_create()

    # Carregar o modelo de reconhecimento facial
    modelo_path = "modelo_face.yml"
    if not os.path.exists(modelo_path):
        print("Modelo de reconhecimento facial não encontrado.")
        return None

    reconhecedor.read(modelo_path)
    while True:
        ret, imagem = camera.read()
        if not ret:
            print("Erro ao capturar a imagem da câmera.")
            break

        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faces_detectadas = face_cascade.detectMultiScale(imagem_cinza, scaleFactor=1.1, minSize=(100, 100))

        for (x, y, l, a) in faces_detectadas:
            imagem_face = cv2.resize(imagem_cinza[y:y + a, x:x + l], (220, 220))
            id_face, confianca = reconhecedor.predict(imagem_face)

            # Exibir feedback visual
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 2)
            cv2.putText(imagem, f"ID: {id_face} ({confianca:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if confianca < 100:  # Se a confiança for baixa, podemos considerar a face reconhecida
                camera.release()
                cv2.destroyAllWindows()
                return id_face  # Retorna o ID reconhecido

        cv2.imshow("Reconhecimento Facial", imagem)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    return None
