import cv2

classific =  cv2.CascadeClassifier("haarcascade_frontalface_default.xml")#Classificador para encontrar faces
reconhecedor = cv2.face.EigenFaceRecognizer_create()
reconhecedor.read("classificadorEigen.yml")#Classificador treinado para identificar a face do estudante
largura, altura = 220, 220
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
camera = cv2.VideoCapture(0)


while (True):
#Detecção das faces
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesdetec = classific.detectMultiScale(imagemCinza, scaleFactor=1.5,minSize=(150,150))
#Criação de um retangulo onde foi encontrada a face do estudante
    for (x, y, l, a) in facesdetec:
        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
        cv2.rectangle(imagem, (x,y), (x + l, y + a), (0,0,255))
        id, confianca = reconhecedor.predict(imagemFace)
        cv2.putText(imagem, str(id), (x,y + (a+30)), font, 2, (0,0,255))
    cv2.imshow("Face", imagem)
    if cv2.waitKey(1) == ord('q'):
        break


camera.release()
cv2.destroyAllWindowns()