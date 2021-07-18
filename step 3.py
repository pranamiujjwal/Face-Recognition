#Program to find multiple faces in an image
import cv2
import face_recognition

image='multiface.jpg'  #path of the image
image=face_recognition.load_image_file(image)   #load the image
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #convert
face=face_recognition.face_locations(image) #finding face coordinates in the image
#many faces has many face coodinates
for facelocation in face:   
    #create-ing rectangles around every face
    cv2.rectangle(image,(facelocation[3],facelocation[0]),(facelocation[1],facelocation[2]),(0,255,0),1)

cv2.imshow("Result image",image)    #Displaying the image
cv2.waitKey(0)
cv2.destroyAllWindows