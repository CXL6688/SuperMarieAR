# -*- coding: utf-8 -*

import cv2
import numpy
 
font_face_casecade=cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

profile_face_casecade=cv2.CascadeClassifier('haarcascade_profileface.xml')
cap = cv2.VideoCapture(0)
while 1:
    ret, frame = cap.read()
    #转换为灰度图
    gray_img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		#人脸检测
    face=font_face_casecade.detectMultiScale(gray_img,1.3,5)
    if len(face):
    	print("检测到正脸")
    else:
    	face=profile_face_casecade.detectMultiScale(gray_img,1.3,5)
    	if len(face):
    		print("检测到侧脸")
    	else:
    		print("没有检测到脸")
    for (x,y,w,h) in face:
        #在原图上绘制矩形
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imshow("cap", frame)
    if cv2.waitKey(100) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()