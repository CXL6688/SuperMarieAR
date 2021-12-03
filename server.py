# -*- coding: utf-8 -*

import asyncio
import websockets
import time
import datetime
import _thread
import cv2
import numpy

command=""
font_face_casecade=cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

profile_face_casecade=cv2.CascadeClassifier('haarcascade_profileface.xml')
cap = cv2.VideoCapture(0)
standerY=-1

# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket):
    while True:
        global command
        command = await websocket.recv()
        ret, frame = cap.read()
        gray_img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        face=font_face_casecade.detectMultiScale(gray_img,1.3,5)
        if len(face):
            print("检测到正脸")
            global standerY
            for (x,y,w,h) in face:
                if(standerY>0):
                    print((x,y,w,h))
                    if(y>standerY+h*0.2):
                        print("开始跳")
                        await websocket.send("jump")
                        break
                else:
                    standerY=y
                await websocket.send("run")
                break
        else:
            face=profile_face_casecade.detectMultiScale(gray_img,1.3,5)
            if len(face):
                print("检测到侧脸")
                await websocket.send("back")
            else:
                print("没有检测到脸")
                await websocket.send("stop")

# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path):
		await recv_msg(websocket)

# 把ip换成自己本地的ip
start_server = websockets.serve(main_logic, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()