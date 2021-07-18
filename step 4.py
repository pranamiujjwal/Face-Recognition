#Program to compare two images to compare the faces in both the images
import cv2
import face_recognition

image='john wick.jpg'   #saves/known image path
image=face_recognition.load_image_file(image)   #load the image
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #convert it
imagefaceencoding=face_recognition.face_encodings(image)[0] #finding encodes for the known images

testimage='obama.jpg'   #test image to compare
testimage=face_recognition.load_image_file(testimage)   #load testimage
testimage=cv2.cvtColor(testimage,cv2.COLOR_BGR2RGB) #convert testimage
testimagefacelocation=face_recognition.face_locations(testimage)[0] #testface location
testimagefaceencoding=face_recognition.face_encodings(testimage)[0] #test face encodes

#comparing both image encodes for similarities
result=face_recognition.compare_faces([imagefaceencoding],testimagefaceencoding)    
facedistance=face_recognition.face_distance([imagefaceencoding],testimagefaceencoding)
print(result,facedistance)
#if matc then show them in rectangles
if result[0] == True and round(facedistance[0])<0.5:
    cv2.rectangle(testimage,(testimagefacelocation[3],testimagefacelocation[0]),(testimagefacelocation[1],testimagefacelocation[2]),(0,255,0),2)
    cv2.putText(testimage,"John wick",(testimagefacelocation[3],testimagefacelocation[0]),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)

else:
    cv2.rectangle(testimage,(testimagefacelocation[3],testimagefacelocation[0]),(testimagefacelocation[1],testimagefacelocation[2]),(0,0,255),2)
    cv2.putText(testimage,"Unknown",(testimagefacelocation[3],testimagefacelocation[0]),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

cv2.imshow("Saved image",testimage)

cv2.waitKey(0)
cv2.destroyAllWindows