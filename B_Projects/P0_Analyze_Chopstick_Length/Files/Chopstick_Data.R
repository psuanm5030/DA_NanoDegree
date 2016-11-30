

# Chopstick Lentgh
setwd("/Users/Miller/Desktop/NanoDegree/Proj_ChopSticks/")

data1=read.delim("ChopSticksData.txt",sep = ",")
data1$Chopstick.Length = as.factor(data1$Chopstick.Length)
model = lm(Food.Pinching.Efficiency ~  Chopstick.Length, data = data1)

summary(model)
