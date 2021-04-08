import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]


minHand = 35
maxHand = 210

while True:
    success, img = cap.read()
    img = detector.findHands(img, True)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:


        # print(lmList[4], lmList[8])
        x1, y1 = lmList[12][1], lmList[12][2]

        cv2.circle(img, (x1,y1), 8, (0,255,0),cv2.FILLED)
        print(x1,y1)
        if y1 < 150:
            volume.SetMasterVolumeLevel(maxVol, None)
        else:
            volume.SetMasterVolumeLevel(minVol, None)
        # if lenght < 35:
        #     cv2.circle(img, (cx, cy), 13, (255, 255, 255), cv2.FILLED)
    else:
        volume.SetMasterVolumeLevel(maxVol, None)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'КВС:{int(fps)}', (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                (0, 255, 0), 1)
    cv2.imshow("Img", img)

    cv2.waitKey(1)
