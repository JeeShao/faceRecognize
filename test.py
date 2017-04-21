#!/usr/bin/env python
#  -- coding:utf-8 --
# #@Time  : 2017/3/22
# #@Author: Jee
import cv2
import numpy as np

img = cv2.imread("1.jpg")
cv2.imshow("origin",img)
thresholdco = 0.05
histogram = [0]*256

rows = img.shape[0] #像素点行数
cols = img.shape[1] #像素点列数
for i in img:
    for j in i:
        b,g,r = j
        gray = (r * 299 + g * 587 + b * 114) // 1000
        histogram[gray] += 1

calnum = 0
total = cols * rows
for i in range(256):
    if float(calnum)/total < thresholdco:
        calnum += histogram[255-i]
        num = i
    else:break

calnum = 0
averagegray = 0
for i in reversed(range(255-num,256)):
    averagegray += histogram[i] * i
    calnum += histogram[i]

averagegray /=calnum
co = 255.0/averagegray
for i in range(rows):
    for j in range(cols):
        img[i,j] = [round(co*img[i,j][0]+0.5),round(co*img[i,j][1]+0.5),round(co*img[i,j][2]+0.5)]
cv2.imshow("new",img)

cv2.waitKey()
cv2.destroyAllWindows()
