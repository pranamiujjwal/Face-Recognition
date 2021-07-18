#Program to locate a face in an image
import cv2
import face_recognition

image='john wick.jpg'
image=face_recognition.load_image_file(image)   #load the image
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #convert it to RGB from BGR
imagefacelocation=face_recognition.face_locations(image)[0] #finding the coodinates of face[0] in the image
#encoodings are the various measurements of a different parts of a faces
imagefaceencoding=face_recognition.face_encodings(image)[0] #finding the encodes of face[0]] in the image
#creating an rectangle around the face 
cv2.rectangle(image,(imagefacelocation[3],imagefacelocation[0]),(imagefacelocation[1],imagefacelocation[2]),(0,255,0),2)
cv2.imshow("Result image",image)    #Displaying the image
cv2.waitKey(0)  
