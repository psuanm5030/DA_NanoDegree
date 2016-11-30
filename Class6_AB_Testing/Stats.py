from scipy import stats
import scipy as sp
import numpy as np

s = np.array([87029, 113407, 84843, 104994, 99327, 92052, 60684])

n, min_max, mean, var, skew, kurt = stats.describe(s)
std=math.sqrt(var)
print std

#note these are sample standard deviations
#and sample variance values
#to get population values s.std() and s.var() will work

#The location (loc) keyword specifies the mean.
#The scale (scale) keyword specifies the standard deviation.

# We will assume a normal distribution
# Taking the 95% CI with the mean and
R = stats.norm.interval(0.95,loc=mean,scale=std/math.sqrt(len(s)))
print R

# Getting the Standard Error for the Sample
se = std / math.sqrt(n)
print se