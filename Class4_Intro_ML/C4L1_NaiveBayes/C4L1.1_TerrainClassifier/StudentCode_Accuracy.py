import sys
sys.path.insert(0, "/Users/Miller/GitHub/DAnanodegree/Class4_Intro_ML/C1L1_NaiveBayes/C1L1.1_TerrainClassifier")
from class_vis import prettyPicture
from prep_terrain_data import makeTerrainData
from classify import NBAccuracy

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl


features_train, labels_train, features_test, labels_test = makeTerrainData()

def submitAccuracy():
    accuracy = NBAccuracy(features_train, labels_train, features_test, labels_test)
    return accuracy

submitAccuracy()