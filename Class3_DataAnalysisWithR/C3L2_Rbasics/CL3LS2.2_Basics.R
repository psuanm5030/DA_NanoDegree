getwd()
setwd('/Users/Miller/GitHub/DAnanodegree/Class3_DataAnalysisWithR/C3L2_Rbasics/')

statesInfo <- read.csv('stateData.csv')

# Predominant way to subset
stateSubset <- subset(statesInfo, state.region == 1)
head(stateSubset,2)
dim(stateSubset)

# Other way to subset
stateSubsetBracket <-statesInfo[statesInfo$state.region == 1, ] 
head(stateSubsetBracket,2)
dim(stateSubsetBracket)