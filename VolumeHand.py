import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################################
wCam, hCam = 640, 480
######################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
##volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
minHand = 35
maxHand = 210
vol = maxVol
volBar = maxHand + 200
while True:
    success, img = cap.read()
    img = detector.findHands(img, True)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:


        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)
        lenght = math.hypot(x2 - x1, y2 - y1)
       # print(lenght)

        # Диапозон пальцов 35 - 210
        # Диапозон громкости -64 - 0
        vol = np.interp(lenght, [minHand, maxHand], [minVol + 50, maxVol])

        volBar = np.interp(lenght, [minHand, maxHand], [maxHand + 180, minHand + 180 ])
        volume.SetMasterVolumeLevel(vol, None)
        print(int(lenght), vol)
        if lenght < 35:
            cv2.circle(img, (cx, cy), 13, (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (minHand,maxHand), (85,400), (0,255,0), 3)
    cv2.rectangle(img, (minHand,int(volBar)), (85,400), (0,255,0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                (0, 255, 0), 1)
    cv2.imshow("Img", img)

    cv2.waitKey(1)
