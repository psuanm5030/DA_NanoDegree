import sys
sys.path.append("/Users/Miller/GitHub/DAnanodegree/Class4_Intro_ML/C1L1_NaiveBayes/C1L1.1_TerrainClassifier")
from class_vis import prettyPicture
from prep_terrain_data import makeTerrainData

import matplotlib.pyplot as plt
import copy
import numpy as np
import pylab as pl


features_train, labels_train, features_test, labels_test = makeTerrainData()


########################## SVM #################################
### we handle the import statement and SVC creation for you here
from sklearn.svm import SVC
clf = SVC(kernel="linear")

#### now your job is to fit the classifier
#### using the training features/labels, and to
#### make a set of predictions on the test data
clf.fit(features_train,labels_train)


#### store your predictions in a list named pred
pred = clf.predict(features_test) # Storing a listing of predictions




from sklearn.metrics import accuracy_score
acc = accuracy_score(pred, labels_test) # 92%

def submitAccuracy():
    return acc