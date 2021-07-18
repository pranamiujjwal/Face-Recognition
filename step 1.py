#program to open an image with help of face_recognition library

import cv2
import face_recognition

image='john wick.jpg'  #path of the image
image=face_recognition.load_image_file(image)   #loading image into the program
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #converting it RGB from BGR
cv2.imshow("Saved image",image) #it will display that image
cv2.waitKey(0)