import os
import re
import cv2
import pickle
import face_recognition
import numpy

with open('D:/VS code/opencvprojects/knownfaces/known','rb') as file:
    data=pickle.loads(file.read())  #extract all nown encodes from the file
    file.close()

#comparing both image encodes for similarities
knownfacesencodes=[]
name=[]
for i in data.values():
    knownfacesencodes.append(i[0])
    name.append(i[1])

video=cv2.VideoCapture(0)
while True:
    rate,frame=video.read()
    image=cv2.resize(frame,(0,0),None,0.25,0.25)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    faces=face_recognition.face_locations(image)
    encodes=face_recognition.face_encodings(image)
    for face, encode in zip(faces, encodes):
        result=face_recognition.compare_faces(knownfacesencodes,encode)    
        facedistance=face_recognition.face_distance(knownfacesencodes,encode)
        matchindex=numpy.argmin(facedistance)
        if result[matchindex]:
            y1,x2,y2,x1=face
            cv2.rectangle(frame, (face[3]*4,face[0]*4), (face[1]*4,face[2]*4),(0,255,0),2)
            cv2.putText(frame, name[matchindex],(face[3]*4,face[0]*4),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
        else:
            cv2.rectangle(frame, (face[3]*4,face[0]*4), (face[1]*4,face[2]*4),(0,0,255),2)
    cv2.imshow("Output",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
