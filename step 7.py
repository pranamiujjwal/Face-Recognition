#Program to recognize face in given image with known face encodes from the file
import os
import re
import cv2
import pickle
import face_recognition
import numpy
with open('D:/VS code/opencvprojects/knownfaces/known','rb') as file:
    data=pickle.loads(file.read())  #extract all nown encodes from the file
    file.close()

testimage='D:/VS code/opencvprojects/johntest.jpg'   #test image to compare
testimage=face_recognition.load_image_file(testimage)   #load testimage
testimage=cv2.cvtColor(testimage,cv2.COLOR_BGR2RGB) #convert testimage
testimagefacelocation=face_recognition.face_locations(testimage) #testface location
testimagefaceencoding=face_recognition.face_encodings(testimage) #test face encodes

#comparing both image encodes for similarities
knownfacesencodes=[]
name=[]
for i in data.values():
    knownfacesencodes.append(i[0])
    name.append(i[1])

for encodes,face in zip(testimagefaceencoding,testimagefacelocation):
    result=face_recognition.compare_faces(knownfacesencodes,encodes)    
    facedistance=face_recognition.face_distance(knownfacesencodes,encodes)
    matchindex=numpy.argmin(facedistance)
    if result[matchindex]:
        y1,x2,y2,x1=face
        cv2.rectangle(testimage,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(testimage,name[matchindex],(),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
        print('found')
        cv2.imshow("Result image",testimage)    #Displaying the image
        cv2.waitKey(0)
        cv2.destroyAllWindows
    else:
        print('not found')