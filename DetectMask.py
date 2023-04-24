import os
import cv2
import numpy as np
import face_recognition

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

class MaskDetection:
    def __init__(self):
        if os.path.isdir("Found")==0:
            os.mkdir("Found")
        self.haar_data = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.pca = PCA(n_components=3)
        self.size=800
    
    def GetFace(self):
        image = face_recognition.load_image_file("D:/VS code/python/MinorProject/faces/0126CS191117.jpg")  
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = self.haar_data.detectMultiScale(image)
        i=len(os.listdir("Found"))
        for x, y, width, height in faces:            
            face = image[y:y+height, x:x+width, :]
            face = cv2.resize(face, (50, 50))
            name="Found/p{}.png".format(i)
            i+=1
            cv2.imwrite(name,face)
            # cv2.imshow("Result image", face)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows

    def CreateDataSet(self):
        """Create dataset"""           
        c=int(input("1. From WebCam \n2. From Folder \nYour choice: "))
        if c==1: 
            print("Collecting Data for Without mask face")
            data=self.CollectSample()
            np.save("without_mask.npy", data)
            input("press any key to continue.....")

            print("Collecting Data for With mask face")
            data=self.CollectSample()
            np.save("with_mask.npy", data)
            input("press any key to continue.....")
        elif c==2:
            print("Collecting Data for With mask face from Folder")
            print("Collecting Data for Without mask face from Folder")

    def CollectSample(self):
        data = []
        LiveVideo = cv2.VideoCapture(0)
        i=0
        while True:
            flag, image = LiveVideo.read()
            if flag:
                faces = self.haar_data.detectMultiScale(image)
                for x, y, width, height in faces:                    
                    face = image[y:y+height, x:x+width, :]
                    face = cv2.resize(face, (50, 50))
                    print("Photos saved:", len(data))
                    if i == 200:
                        i=0
                        input("Press any key to continue.")
                    if len(data) < self.size:
                        i+=1
                        data.append(face)
                if len(data) >= self.size:
                    break
        LiveVideo.release()
        return data

    def LoadDataset(self):
        try:
            without_mask = np.load("without_mask.npy")
            with_mask = np.load("with_mask.npy")
        except:
            print("Dataset not found Collect data again")
            input("press anything to continue..........")
            self.CollectSample()
            without_mask = np.load("without_mask.npy")
            with_mask = np.load("with_mask.npy")         
        finally:        
            with_mask = with_mask.reshape(self.size, 50*50*3)
            without_mask = without_mask.reshape(self.size, 50*50*3)
            dataset=np.r_[with_mask, without_mask]
            return dataset

    def TrainModel(self):
        """Create """
        dataset=self.LoadDataset()        
        labels=np.zeros(dataset.shape[0])
        labels[self.size:] = 1
        
        x_train, x_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.25)
        x_train = self.pca.fit_transform(x_train)
        model = SVC()
        model.fit(x_train, y_train)
        # Find Accuracy
        x_test = self.pca.fit_transform(x_test)
        y_pred=model.predict(x_test)
        print("accuracy:", accuracy_score(y_test, y_pred))
        return model

    def Start(self):
        """start"""
        model = self.TrainModel()
        names={0:"mask", 1:"no mask"}
        # Starting Webcam
        capture = cv2.VideoCapture(0)
        while True:
            flag, image = capture.read()
            if flag:
                faces = self.haar_data.detectMultiScale(image)
                for x, y, width, height in faces:
                    face = image[y:y+height, x:x+width, :]
                    face = cv2.resize(face, (50, 50))
                    face1 = face.reshape(1, -1)
                    face1 = self.pca.transform(face1)
                    pred = model.predict(face1)[0]
                    if pred == 1:
                        name="Found/p{}.png".format(len(os.listdir("Found")))
                        cv2.imwrite(name,face)
                        print(names[int(pred)])
                cv2.imshow("result", image)    
                if cv2.waitKey(2)==27:
                    break
        cv2.destroyAllWindows()
        capture.release()
    
    def Model(self):
        model = self.TrainModel()
        names={0:"mask", 1:"no mask"}
        # Starting webcam
        capture = cv2.VideoCapture(0)
        while True:
            flag, image = capture.read()
            if flag:
                faces = self.haar_data.detectMultiScale(image)
                for x, y, width, height in faces:
                    cv2.rectangle(image, (x, y), (x+width, y+height), (0,0,255), 4)
                    face = image[y:y+height, x:x+width, :]
                    face = cv2.resize(face, (50, 50))
                    face=face.reshape(1, -1)
                    face=self.pca.transform(face)
                    pred = model.predict(face)[0]
                    print(names[int(pred)])
                cv2.imshow("result", image)
                if cv2.waitKey(2)==27:
                    break
        cv2.destroyAllWindows()
        capture.release()                

    def __del__(self):
        input("Press anything to continue.....")


if __name__=="__main__":
    T=MaskDetection()
    # T.CollectSample()
    # T.CreateDataSet()
    
    T.LoadDataset()
    T.TrainModel()
    # T.Model()
    T.Start()
    del T