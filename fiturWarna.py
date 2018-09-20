# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 23:49:20 2018

@author: USER
"""

import cv2
import numpy as np
#import os

def resizeImg(image):
    #img = cv2.imread(filename)
    small = cv2.resize(image, (0,0),fx=0.1,fy=0.1)
    return small

def normalize(channel):
    for i in range(len(channel)):
        for j in range(len(channel[i])):
            channel[i][j] = channel[i][j] / 255
    return channel

def func(t):
    if(t > th):
        return np.cbrt(t)
    else:
        return 7.787*t + np.divide(16.0,116.0)

def visualize(LabImg):
    for i in range(len(LabImg)):
        for j in range(len(LabImg[i])):
            LabImg[i][j][0] = LabImg[i][j][0] * 255/100
            LabImg[i][j][1] += 128
            LabImg[i][j][2] += 128
    return LabImg

def meanMoment(channel):
    sumValue = 0
    countValue = 0
    for i in range(len(channel)):
        for j in range(len(channel[i])):
            if(channel[i][j] < 99):
                sumValue += channel[i][j]
                countValue += 1
    return sumValue/countValue

def varianceMoment(channel, meanChannel):
    sumValue = 0
    countValue = 0
    for i in range(len(channel)):
        for j in range(len(channel[i])):
            if(channel[i][j] < 99):
                sumValue += np.power(channel[i][j] - meanChannel,2)
                countValue += 1
    return np.sqrt(sumValue/countValue)

def skewnessMoment(channel, meanChannel):
    sumValue = 0
    countValue = 0
    for i in range(len(channel)):
        for j in range(len(channel[i])):
            if(channel[i][j] < 99):
                sumValue += np.power(channel[i][j] - meanChannel,3)
                countValue += 1
    return np.cbrt(sumValue/countValue)


strFile = 'D:\\KULIAH\\SEMESTER VII\\SKRIPSI - OFFLINE\\Ahmad Fauzi A _ Akhmad Muzanni S\\Segmentasi\\1.jpg'
rgbImg = cv2.imread(strFile)

rgbImgFloat = rgbImg.astype(np.float64)
blueNorm = np.zeros_like(rgbImgFloat[:,:,0])
greenNorm = np.zeros_like(rgbImgFloat[:,:,1])
redNorm = np.zeros_like(rgbImgFloat[:,:,2])
#blueNorm = 0
#greenNorm = 0
#redNorm = 0
#blueNorm = normalize(rgbImgFloat[:,:,0])
cv2.normalize(rgbImgFloat[:,:,0],  blueNorm, 0, 1, cv2.NORM_MINMAX)
cv2.normalize(rgbImgFloat[:,:,1],  greenNorm, 0, 1, cv2.NORM_MINMAX)
cv2.normalize(rgbImgFloat[:,:,2],  redNorm, 0, 1, cv2.NORM_MINMAX)


#CONVERT BGR TO RGB
merged = cv2.merge((redNorm,greenNorm,blueNorm))


#matriksKonv = [[0.412453,0.212671,0.019334],[0.357580,0.715160,0.119193],[0.180423,0.072169,0.950227]]
matriksKonv = np.array([[0.412453,0.357580,0.180423],[0.212671,0.715160,0.072169],[0.019334,0.119193,0.950227]])
#matriksKonv = np.array([[0.180423,0.072169,0.950227],[0.357580,0.715160,0.119193],[0.412453,0.212671,0.019334]])
Xn = 0.950456
Zn = 1.088754
th = 0.008856
print(matriksKonv)
#np.matmul(matriksKonv)

#b = np.array([[1,2,3],[4,5,6]])
#c = np.array([[1,2],[3,4],[5,6]])
b = np.array([0,0,0])
#print(np.matmul(matriksKonv,b))

# CONVERT BGR TO XYZ
xyz = merged.copy()
for i in range(len(xyz)):
    for j in range(len(xyz[i])):
        xyz[i][j] = np.matmul(matriksKonv, xyz[i][j])
        xyz[i][j][0] = xyz[i][j][0]/Xn
        xyz[i][j][2] = xyz[i][j][2]/Zn

count = 0
Lab = np.zeros_like(xyz)
for i in range(len(Lab)):
    for j in range(len(Lab[i])):
        if(xyz[i][j][1] > th):
            Lab[i][j][0] = (116*np.cbrt(xyz[i][j][1]))-16
        else:
            Lab[i][j][0] = 903.3 * xyz[i][j][1]
            count+=1
        #Lab[i][j][0] = np.cbrt(xyz[i][j][0])
        #Lab[i][j][1] = np.cbrt(xyz[i][j][1])
        #Lab[i][j][2] = np.cbrt(xyz[i][j][2])
        Lab[i][j][1] = 500 * (func(xyz[i][j][0]) - func(xyz[i][j][1]))
        Lab[i][j][2] = 200 * (func(xyz[i][j][1]) - func(xyz[i][j][2]))
print(count)

#Lab = visualize(Lab)


            


labLibrary = cv2.cvtColor(rgbImg, cv2.COLOR_BGR2Lab)
xyzLibrary = cv2.cvtColor(rgbImg, cv2.COLOR_BGR2XYZ)
#test = cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)

meanL = meanMoment(Lab[:,:,0])
varL = varianceMoment(Lab[:,:,0], meanL)
skewL = skewnessMoment(Lab[:,:,0], meanL)

meanLLib = meanMoment(labLibrary[:,:,0])
varLLib = varianceMoment(labLibrary[:,:,0], meanLLib)
skewLLib = skewnessMoment(labLibrary[:,:,0], meanLLib)

print(meanL)
print(varL)
print(skewL)
print(meanLLib)
print(varLLib)
print(skewLLib)

#meanA = meanMoment(Lab[:,:,1])
#meanB = meanMoment(Lab[:,:,2])




#cv2.imshow('HASIL',lab)
#cv2.waitKey(0)