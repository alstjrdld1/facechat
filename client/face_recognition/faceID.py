from View.dialogs.AlertBox import AlertBox
from os import listdir
from os.path import isfile, join
import os 

import cv2
import numpy as np

class FaceID:

    def __init__(self):
        print("FaceRecognition class created")
        
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.data_path = 'client/face_recognition/faces/'
        self.model = cv2.face.LBPHFaceRecognizer_create()

    def removeAllFile(self, filePath):
        if os.path.exists(filePath):
            for file in os.scandir(filePath):
                os.remove(file.path)
            return 'Remove All File'
        else:
            return 'Directory Not Found'

    def train(self):
        
        onlyfiles = [f for f in listdir(self.data_path) if isfile(join(self.data_path,f))]
        Training_Data, Labels = [], []

        for i, files in enumerate(onlyfiles):
            image_path = self.data_path + onlyfiles[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)

        Labels = np.asarray(Labels, dtype=np.int32)


        self.model.train(np.asarray(Training_Data), np.asarray(Labels))

        print("Model Training Complete!!!!!")

    def face_extractor(self, img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray,1.3,5)

        if faces is():
            return None

        for(x,y,w,h) in faces:
            cropped_face = img[y:y+h, x:x+w]
            
        return cropped_face
    
    def register(self, Id):
        print(self.removeAllFile(self.data_path))
        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if self.face_extractor(frame) is not None:
                count+=1
                face = cv2.resize(self.face_extractor(frame),(200,200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                file_name_path = self.data_path + Id +"_"+str(count)+'.jpg'
                cv2.imwrite(file_name_path,face)

                cv2.putText(frame,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.putText(frame,"Face Found!",(200,300),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
                cv2.imshow('Face Cropper',frame)
            else:
                cv2.putText(frame,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.putText(frame,"Face not Found",(200,300),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.imshow('Face Cropper',frame)
                        
            if cv2.waitKey(1)==13 or count==100:
                break
            
        cap.release()
        cv2.destroyAllWindows()
        print('Colleting Samples Complete!!!')

        self.train()

        
    def face_detector(self, img, size = 0.5):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray,1.3,5)

        if faces is():
            return img,[]

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
            roi = img[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200,200)) 

        return img,roi

    def login(self):
        loginState = False

        try:
            self.train()
        except:
            return loginState
        count = 0
        cap = cv2.VideoCapture(0)
        print("login method called ")

        while True:
            count += 1 

            if count > 200:
                break

            ret, frame = cap.read()
            image, face = self.face_detector(frame)

            try:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                result = self.model.predict(face)

                if result[1] < 500:
                    confidence = int(100*(1-(result[1])/300))
                    display_string = str(confidence)+'% Confidence it is user'
                cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)


                if confidence > 75:
                    cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face ID LOGIN', image)
                    print("face check")
                    loginState = True
                    break

                else:
                    cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face ID LOGIN', image)


            except:
                cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('Face ID LOGIN', image)
                pass
            
            if cv2.waitKey(1)==13:
                break
        
            
        cap.release()
        cv2.destroyAllWindows()

        return loginState