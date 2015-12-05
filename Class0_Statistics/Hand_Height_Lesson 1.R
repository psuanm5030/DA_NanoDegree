

setwd("/Users/Miller/Desktop/NanoDegree/COURSE_Statistics")

data1=read.csv("hand_height_lesson 1.csv")

model = lm(Height ~ Hand + Gender, data = data1)

summary(model)
