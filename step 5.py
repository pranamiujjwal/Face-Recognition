#Program to save encodings of a known face to file
import re
import cv2
import pickle
import face_recognition

image='D:/VS code/opencvprojects/faces/john wick.jpg'   #image
name=re.search(r'\w+\.jpg',image)   #extract name of image
name=name[0].replace('.jpg','')
image=face_recognition.load_image_file(image)   #loading image
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #converting image
face=face_recognition.face_locations(image) #extracting face location
faceencodes=face_recognition.face_encodings(image,face) #extracting face encodes
data = {"encodings": faceencodes, "names": name}    #creating a dictionary to hold hold with image name
with open('opencvprojects/knownfaces/johnwick','wb') as f:
    f.write(pickle.dumps(data)) #saves dictionary
    print('sucess')
    f.close()