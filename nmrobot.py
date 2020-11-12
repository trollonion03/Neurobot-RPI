##nmrobot
##thank you for General Vision
##thankufor Greenman
## Learn an example extracted from the center region of a first frame
## Monitor this region in subsequent frames
## and report its category and distance to the learned example

import sys
import ctypes
import NeuroMem as nm
import GVcomm_SPI as comm

from picamera.array import PiRGBArray
from picamera import picamera
import time
import cv2 as cv
from random import random

#to communicate arduino
import serial

ser = serial.Serial(timeout=3)
ser.port = '/dev/tttyS0'
ser.open()

LENGTH=256
bytearray = ctypes.c_int * LENGTH
vector=bytearray()

#-----------------------------------------------------
# Extract a subsample of the ROI at the location X,Y
# using a block size bW*bH and amplitude normalization on or off
# return the length of the output vector
#-----------------------------------------------------
for y in range(Top, Top + Height, bH):
    for x in range(Left, Left + Width, bW):
      Sum=0	
      for yy in range(0, bH):
        for xx in range (0, bW):
          # to adjust if monochrome versus rgb image array
          Sum += image[y+yy, x+xx]
      vector[p] = (int)(Sum / (bW*bH))

      #log the min and max component
      min = 255
      max = 0
      if (max < vector[p]):
        max = vector[p]
      if (min > vector[p]):
        min = vector[p]
      p=p+1
    
  if ((normalize == 1) & (max > min)):
    for i in range (0, p):
      Sum= (vector[i] - min) * 255
      vector[i] = (int)(Sum / (max - min))

  # return the length of the vector which must be less or equal to 256
  return p, vector
if (comm.Connect()!=2):
  print ("Cannot connect to NeuroShield\n")
  sys.exit()
#------------------------------------------------- 
# Select a NeuroMem platform
# 0=simu, 1=NeuroStack, 2=NeuroShield, 4=Brilliant
#-------------------------------------------------
nm.ClearNeurons()

# initialize the camera and grab a reference image
camera = PiCamera()
camera.resolution=(600,400)
time.sleep(2) # camera warm up
rawCapture = PiRGBArray(camera)

# grab an image from the camera
camera.capture(rawCapture, format="bgr")
imsrc = rawCapture.array

# define center of image
imW=imsrc.shape[1]
imH=imsrc.shape[0]
print("Image = " + repr(imW) + " x " + repr(imH))

# define the Region of Interest (roi) to learn
roiW = 128
roiH = 128
roiL= int(imW/2 - roiW/2)
roiT= int(imH/2 - roiH/2)

print("Learning center Region Of Interest")
cv.rectangle(imsrc,(roiL, roiT),(roiL+roiW, roiT+roiH),(255,0,0),1)
cv.imshow('Video', imsrc)
cv.waitKey(3)

# convert to grey-level for the analytics
imgl = cv.cvtColor(imsrc, cv.COLOR_BGR2GRAY)
bW = int(8)
bH = int(8)
normalize = int(1)

print("Type a target # when ready between[1-9]")

font                   = cv.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (255,0,0)
lineType               = 1
while (1==1):
  rawCapture = PiRGBArray(camera)
  camera.capture(rawCapture, format="bgr")
  imsrc = rawCapture.array
  imgl = cv.cvtColor(imsrc, cv.COLOR_BGR2GRAY)
  vlen, vector =GetGreySubsample(imgl, roiL, roiT, roiW, roiH, bW, bH, normalize)
  dist, cat, nid = nm.BestMatch(vector, vlen)
  if cat==65535:
    roiLabel=""
  else:
    roiLabel= "Cat " + str(cat) + " @ Distance " + str(dist)
    if str(cat) == 1: #1번 카테고리는 무조건 피해야할 장애물로 학습 
      print("object detected")
      #uart 코드작성
      #test코드
      print("cat1 decetced") #테스트 완료 시, 삭제바람
      int_value = randint(0, 1)
      int_v = 0
      ser.readline().strip().decode('utf-8')
      if int_v = 0:
        ser.write('a\n')
        int_v = int_v + 1
      elif int_v > 0:
        if int_value == 0:
          ser.write('R\n')
        elif int_value == 1:
          ser.write('L\n')
      
  cv.rectangle(imsrc,(roiL, roiT),(roiL+roiW, roiT+roiH),(255,0,0),1)
  cv.putText(imsrc,roiLabel, (roiL, roiT - 10), font, fontScale, fontColor,lineType)
  cv.imshow('Video', imsrc)
  c=cv.waitKey(1)
  if (c > 48) & (c < 57):
    catL= c-48
    print("Learning target " + str(catL))
    # Learn ROI at center of the image
    vlen, vector=GetGreySubsample(imgl, roiL, roiT, roiW, roiH, bW, bH, normalize)
    nm.Learn(vector,vlen,catL)
    # Learn a counter example ROI at an offset of roi/2 right and down
    vlen, vector=GetGreySubsample(imgl, roiL + roiW/2, roiT + roiT/2, roiW, roiH, bW, bH, normalize)
    ncount = nm.Learn(vector,vlen,0)
    print("ncount =" + repr(ncount))

