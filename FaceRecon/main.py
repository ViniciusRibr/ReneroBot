import cv2
import time
import os

classific = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

if not os.path.exists('fotos2'):
    os.makedirs('fotos2')

amostra = 1
numAmostra = 25
id = input("Digite seu identificador: ")
largura, altura = 220, 220
print("Capturando a face...")

lastmes = time.time()
intervalo = 2

#Funções principais
while amostra <= numAmostra:
    conectado, imagem = camera.read()
    if not conectado:
        print("Erro ao capturar imagem.")
        break
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesdetec = classific.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

    # Desenha um retângulo ao rosto
    if len(facesdetec) > 0:
        for (x, y, l, a) in facesdetec:
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,255,0),2)
            #Verifica se o rosto está sendo marcado
            margem_x = largura * 0.1
            margem_y = altura * 0.1

            if x > margem_x and (x + l) < (largura - margem_x) and y > margem_y and (y + a) < (altura - margem_y):
                imagem = imagemCinza[y:y + a, x:x + l]
                imagem = cv2.resize(imagem, (largura, altura))
               
        sucesso = cv2.imwrite(f"fotos2/auto_fotos_{amostra}.jpg", imagem)
        if sucesso:
            print(f"[foto {amostra}] capturada com sucesso.")
            amostra += 1
        else:
            print(f"Falha ao salvar a foto {amostra}.")

    cv2.imshow("Face_recon", imagem) 

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break


print("Faces capturadas com sucesso!")
camera.release()
cv2.destroyAllWindows()
