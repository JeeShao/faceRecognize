#!/usr/bin/env python
# -- coding:utf-8 --
#@Time  : 2017/4/21  
#@Author: Jee
import cv2

img = cv2.imread("2.jpg")
cv2.imshow("origin",img)

def lighter(img):
    b,g,r = cv2.split(img)

    bAvg = cv2.mean(b)[0]
    gAvg = cv2.mean(g)[0]
    rAvg = cv2.mean(r)[0]

    K = (bAvg+gAvg+rAvg)/3
    Kb = K/bAvg
    Kg = K/gAvg
    Kr = K/rAvg

    cv2.addWeighted(b,Kb,0,0,0,b)
    cv2.addWeighted(g,Kg,0,0,0,g)
    cv2.addWeighted(r,Kr,0,0,0,r)

    img_new = cv2.merge([b,g,r])
    return img_new
    # cv2.imshow("img_new",img_new)

    # cv2.waitKey()
    # cv2.destroyAllWindows()
