import cv2
import time
import os

# Inicializando o classificador e a câmera
classific = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

# Criando diretório para armazenar as fotos, se não existir
if not os.path.exists('fotos/fotos2'):
    os.makedirs('fotos/fotos2')

# Configurações de captura
amostra = 1
numAmostra = 25
id = input("Digite seu identificador: ")
largura, altura = 220, 220
print("Capturando a face...")

# Variáveis de controle de tempo
lastmes = time.time()
intervalo = 2

# Loop principal de captura
while amostra <= numAmostra:
    conectado, imagem = camera.read()
    if not conectado:
        print("Erro ao capturar imagem.")
        break

    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesdetec = classific.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

    # Desenha o retângulo ao redor do rosto e salva a imagem
    for (x, y, l, a) in facesdetec:
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 2)

        # Condição para garantir que a captura ocorra no intervalo desejado
        if time.time() - lastmes >= intervalo:
            imagemRosto = imagemCinza[y:y + a, x:x + l]
            imagemRosto = cv2.resize(imagemRosto, (largura, altura))
            sucesso = cv2.imwrite(f"fotos/fotos2/auto_fotos_{amostra}.jpg", imagemRosto)

            if sucesso:
                print(f"[foto {amostra}] capturada com sucesso.")
                amostra += 1
                lastmes = time.time()  # Atualiza o tempo da última captura
            else:
                print(f"Falha ao salvar a foto {amostra}.")

    # Exibição da imagem com o retângulo ao redor do rosto
    cv2.imshow("Face_recon", imagem)

    # Encerra o loop ao pressionar "q"
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Finalizando a captura
print("Faces capturadas com sucesso!")
camera.release()
cv2.destroyAllWindows()
