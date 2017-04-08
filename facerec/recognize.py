#!/usr/bin/env python
#  -- coding:utf-8 --
# #@Time  : 2017/3/22
# #@Author: Jee
from . import face
from PyQt4.QtCore import QThread

class Recognizer(QThread):
    
    faceImage = None
    model = None
    result = None
    label = None
    confidence = None
    
    def __init__(self):
        super(Recognizer, self).__init__()
        
    def run(self):
        if self.faceImage is None:
            # print 'face Image is None'
            return

        self.result = face.detectSingleFace(self.faceImage)
        
        if self.result is None:
            # print 'Could not detect single face!'
            return

        if self.model is None:
            print("model==None")
            # only return result when model is None
            return
        else:
            # print 'face detected'
            x, y, w, h = self.result
            # crop
            crop = face.resize(face.crop(self.faceImage, x, y, w, h))
            self.label =self.model.predict(crop)[0]
            self.confidence =round(self.model.predict(crop)[1],5)

    def startRec(self, image, model):
        self.faceImage = image
        self.model = model
        
        self.start()
 