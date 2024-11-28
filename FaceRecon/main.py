import cv2
import os
import numpy as np

diretorio_principal = "FaceRecon"
largura, altura = 220, 220
numero_fotos = 30
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
reconhecedor = cv2.face.EigenFaceRecognizer_create()

# Função para criar as pastas automaticamente
def criar_pastas_automaticamente():
    if not os.path.exists(diretorio_principal):
        os.makedirs(diretorio_principal)
    
    for pessoa_id in range(1, 8):
        pasta = os.path.join(diretorio_principal, f"fotos{pessoa_id}")
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"Pasta '{pasta}' criada.")

# Função para capturar fotos
def capturar_fotos(pasta, pessoa_id):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    print(f"Capturando fotos para a pessoa {pessoa_id}...")
    contador = 0
    while contador < numero_fotos:
        conectado, imagem = camera.read()
        if not conectado:
            print("Erro ao capturar a imagem da câmera.")
            break

        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(imagem_cinza, scaleFactor=1.5, minSize=(150, 150))

        for (x, y, l, a) in faces:
            imagem_face = cv2.resize(imagem_cinza[y:y + a, x:x + l], (largura, altura))
            caminho_arquivo = os.path.join(pasta, f"pessoa_{pessoa_id}_foto_{contador + 1}.jpg")
            cv2.imwrite(caminho_arquivo, imagem_face)
            contador += 1

            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 2)
            cv2.imshow("Captura de Fotos", imagem)

            if contador >= numero_fotos:
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Função para treinar o classificador
def treinar_classificador():
    print("Treinando classificador...")
    faces, ids = [], []

    for pessoa_id in range(1, 8):
        pasta = os.path.join(diretorio_principal, f"fotos{pessoa_id}")
        if not os.path.exists(pasta):
            print(f"Pasta {pasta} não encontrada. Pulando...")
            continue

        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            imagem = cv2.imread(caminho_arquivo, cv2.IMREAD_GRAYSCALE)

            if imagem is None:
                print(f"Erro ao carregar imagem: {caminho_arquivo}. Pulando...")
                continue

            if imagem.shape != (altura, largura):
                print(f"Imagem de tamanho incorreto: {caminho_arquivo}. Pulando...")
                continue

            faces.append(imagem)
            ids.append(pessoa_id)

    print(f"Total de imagens usadas para treinamento: {len(faces)}")

    if len(faces) < 2:
        print("Imagens insuficientes para treinamento. Abortando...")
        return False

    try:
        reconhecedor.train(faces, np.array(ids))
        classificador_path = os.path.join(diretorio_principal, "classificadorEigen.yml")
        reconhecedor.write(classificador_path)
        print(f"Classificador salvo em: {classificador_path}")
        return True
    except cv2.error as e:
        print(f"Erro durante o treinamento: {e}")
        return False

# Criar as pastas automaticamente
criar_pastas_automaticamente()

# Capturar fotos para os IDs
for pessoa_id in range(1, 8):  # IDs de 1 a 7
    pasta = os.path.join(diretorio_principal, f"fotos{pessoa_id}")
    capturar_fotos(pasta, pessoa_id)

# Treinar o classificador
if treinar_classificador():
    print("Treinamento concluído com sucesso!")
else:
    print("O treinamento falhou.")


# Limpar recursos
camera.release()
cv2.destroyAllWindows()
