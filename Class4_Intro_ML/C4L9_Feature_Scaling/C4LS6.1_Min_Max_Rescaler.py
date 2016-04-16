""" quiz materials for feature scaling clustering """

### FYI, the most straightforward implementation might
### throw a divide-by-zero error, if the min and max
### values are the same
### but think about this for a second--that means that every
### data point has the same value for that feature!
### why would you rescale it?  Or even use it at all?
def featureScaling(arr):
    len1 = len(arr)
    min1 = min(arr)
    max1 = max(arr)
    print len1
    data = []
    if min1 == max1:
        data = [0.5 for i in range(len1)]
    else:
        for i in arr:
            val = float((i - min1)) / float((max1 - min1))
            data.append(val)
    return data

# tests of your feature scaler--line below is input data
data = [115, 140, 175]
print featureScaling(data)

## Doing this in SKLEARN
from sklearn.preprocessing import MinMaxScaler
import numpy as np
weights = np.array([[115.],[140.],[175.]]) # input data - one feature ([]) with 3 training points
scaler = MinMaxScaler()
# Next does two things:
# 1. FIT - Finds the mins and maxs
# 2. TRANSFORM - Actually applies the formula to all the elements in the set of data
rescaled_weight = scaler.fit_transform(weights)