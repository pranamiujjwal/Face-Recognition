import cv2
import face_recognition

video=cv2.VideoCapture(0)
while True:
    rate,frame=video.read()
    image=cv2.resize(frame,(0,0),None,0.25,0.25)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=face_recognition.face_locations(image)
    for face in faces:
        x1,y1,x2,y2=face
        cv2.rectangle(frame,(y2*4,x1*4),(y1*4,x2*4),(0,255,0),2)
        cv2.imshow("Output",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
video.release()
cv2.destroyAllWindows