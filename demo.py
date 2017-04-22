#!/usr/bin/env python
# -- coding:utf-8 --
#@Time  : 2017/4/21  
#@Author: Jee
import cv2
import sys
import code
import os
# cv2.imshow("origin",img)
#
# def lighter(img):
#     b,g,r = cv2.split(img)
#
#     bAvg = cv2.mean(b)[0]
#     gAvg = cv2.mean(g)[0]
#     rAvg = cv2.mean(r)[0]
#
#     K = (bAvg+gAvg+rAvg)/3
#     Kb = K/bAvg
#     Kg = K/gAvg
#     Kr = K/rAvg
#
#     cv2.addWeighted(b,Kb,0,0,0,b)
#     cv2.addWeighted(g,Kg,0,0,0,g)
#     cv2.addWeighted(r,Kr,0,0,0,r)
#
#     img_new = cv2.merge([b,g,r])
#     return img_new
#     # cv2.imshow("img_new",img_new)
#
#     # cv2.waitKey()
#     # cv2.destroyAllWindows()
#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
#一个小应用，判断一段文本中是否包含简体中：
contents='一个小应用，判断一段文本中是否包含简体中：'
match = zhPattern.search(contents)
if match:
    print (u'有中文：%s' % (match.group(0),))
else:
    print (u'没有包含中文')
