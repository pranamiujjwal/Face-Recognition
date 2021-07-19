#Program to create a file full of known faces encodes
import os
import re
import cv2
import pickle
import face_recognition

path='D:/VS code/opencvprojects/faces'  #path of the file containing known faces
images=os.listdir(path) #collect all files inside that dir
i=0
data={}
for image in images:
    name=re.sub(r'\.jpg','',image)
    image=face_recognition.load_image_file(path+'/'+image)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    encode=face_recognition.face_encodings(image)[0]
    print(i)
    data[i]=[encode,name]   #generating a dictionary with key value 'i' and value a list[encode,name]
    i+=1

f=open('D:/VS code/opencvprojects/knownfaces/known','wb')
f.write(pickle.dumps(data))
f.close()