#!/usr/bin/env python
#  -- coding:utf-8 --
# #@Time  : 2017/3/22
# #@Author: Jee
import os
import cv2
import fnmatch
import numpy as np

from configure import config, userManager
from . import face

def walkFiles(walkDir, match = '*'):
    for root, dirs, files in os.walk(walkDir):
        for fileName in fnmatch.filter(files, match):
            yield os.path.join(root, fileName)        

def prepareImage(fileName):
    return face.resize(cv2.imread(fileName, cv2.IMREAD_GRAYSCALE))
#归一化
def normalize(X, low, high, dtype=None):
    X = np.asarray(X)
    minX, maxX = np.min(X), np.max(X)
    # normalize to [0...1].
    X = X - float(minX)
    X = X / float((maxX - minX))
    # scale to [low...high].
    X = X * (high-low)
    X = X + low
    if dtype is None:
        return np.asarray(X)
    return np.asarray(X, dtype=dtype)
#训练
def trainFace(model):
    
    TRAINING_FILE = os.path.join(config.TRAINING_DIR, config.TRAINING_FILE) 
    faces = []
    labels = []
    
    manager = userManager.UserManager()
    
    persons = os.listdir(config.FACES_DIR)
    for person in persons:
        manager.addUser(person)
        user = manager.getUserByName(person)
        label = int(user['id'])
        personDir = os.path.join(config.FACES_DIR, person)
        for fileName in walkFiles(personDir, '*.pgm'):
            faces.append(prepareImage(fileName))
            labels.append(label)
        
    # Start training model
    model.train(np.asarray(faces), np.asarray(labels))
    # Save model results
    model.save(TRAINING_FILE)
    

