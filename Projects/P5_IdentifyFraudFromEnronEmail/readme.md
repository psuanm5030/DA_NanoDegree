## P5: Identify Fraud from Enron Email
Student: Andy Miller 
Udacity's [Data Analyst Nanodegree](https://www.udacity.com/course/nd002), 

### Background

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, there was a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for to executives.

Utilizing `scikit-learn` and machine learning methodologies, I built a "person of interest" (POI) identifier to detect and predict culpable persons, using features from financial data, email data, and labeled data--POIs who were indicted, reached a settlement or plea deal with the government, or testified in exchange for prosecution immunity.

### Free-Response Questions

> Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: “data exploration”, “outlier investigation”]

I may repeat some of the detail from the project submission page, but I feel it rings especially true.  The 
primary goal of this project was to "play detective" and  put our new machine learning skills to the test, in an
 effort to create a classification model that would, as accurately as possible, predict whether a person was a 
 "person of interest" (POI) based upon that data available.  This meant taking the learnings from the 15 Udacity lessons, 
 covering various classifier algorithms and machine learning techniques (such as feature selection, validation 
 and evaluation), then applying these to a real dataset.  I found that the Udacity courses gave a very wide 
 ranging introduction to each algorithm and technique, but required that we do our own learning.  I captured 
 most of my learning from the sklearn documentation and the Udacity forum.  
 
There is no doubt that this data set is a unique blend, consisting of both financial information for 145 
individuals (collated from public filings and the Enron trial) and emails that were made public from the trial. 
 This dataset allows us to answer our project question because it contains the actual POI labels.  Therefore, we
  had to create our classifiers, review the accuracy metrics, then go back and do the following: 
  - Check for outliers that affected our accuracy in a negative way (while being careful not to remove too much 
  data),
  - Create new features that would help the classifier make better predictions, and 
  - Tune the classifer parameters based on iterative accuracy results.
  
Concerning outliers, I removed exactly three observations (rows) of data: 
- "TOTAL" - which was an arbitrary observation imported with the based data,
- "THE TRAVEL AGENCY IN THE PARK" - a non-person observation that has no related meaning / importance, and  
- "LOCKHART EUGENE E" - an actual person observation that had 20 of 21 fields with 'NaN' values (95% of 
features), making this person a very poor observation to use for classification purposes.
 
As a note, I noticed significant increase in accuracy, precision and recall after removing these outliers.  
Using a naive bayes classifier, I noted: 

| With / Without Outliers | Accuracy↑ | Precision↑ | Recall↑ |
|-------------------------|----------:|-----------:|--------:|
| With                    |   0.83329 |    0.11697 | 0.02550 |
| Without                 |   0.87714 |    0.61628 | 0.37100 |

> What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “properly scale features”, “intelligently select feature”]

What features did I use and how did I pick them?
I utilized the univariate feature selection method of SelectKBest, embedded within my pipelines, to select the 
most relevant features.  This method selects the K best features that are the most powerful.  Prior to the 
pipeline, I evaluated the best 15 features found through this method and the associated scores.  

| Feature                 | Score↑ |
|-------------------------|-------:|
| exercised_stock_options | 24.815 |
| total_stock_value       | 24.183 |
| bonus                   | 20.792 |
| salary                  | 18.290 |
| deferred_income         | 11.458 |
| long_term_incentive     |  9.922 |
| restricted_stock        |  9.212 |
| total_payments          |  8.772 |
| shared_receipt_with_poi |  8.589 |
| loan_advances           |  7.184 |
| Ratio_from_POI          |  5.123 |
| other                   |  4.187 |
| Ratio_to_POI            |  4.095 |
| director_fees           |  2.163 |
| deferral_payments       |  0.225 |

As you can see, the two fields that I created, Ratio_from_POI and Ratio_to_POI were scored in the bottom third, 
meaning they were likely typically not used by any of my models.  I did test my NB classifier with 15 features 
as the selectKbest parameter and found that recall was substantially reduced (precision was still moderately 
acceptable at .441). 

Within my pipelines I set the k value parameter, typically, to be any integer between 2 and 7 on average.  I found 
that the best classifer chosen by gridsearchCV was typically 4-5 features.  For my chosen classifer, Naive Bayes, 
gridsearchCV suggested that I use the following 5 features:
- salary 
- exercised_stock_options
- bonus
- total_stock_value
- deferred_income

Further more, for many of my classifiers, I did employ a normalization technique, using the sklearn MinMaxScaler
.  This re-scaled the financial features to be values between 0 and 1. For my chosen algorithm, this was very 
important, as many of the features were on vastly different scales.  For example, salary and from_messages, are 
two features that represent two different types of numeric data, one being currency and one being a count of 
messages, where salary is on a much broader scale than from_messages.  This requires normalization to ensure 
that the algorithm is not inappropriately swayed by the fact that one feature is on a different scale.  For my 
Naive Bayes classifier, I found that the scaling significantly improved all my evaluation metrics (see table 
below).   

| With / Without Scaling  | Accuracy↑ | Precision↑ | Recall↑ |
|-------------------------|----------:|-----------:|--------:|
| Without                 |   0.86514 |    0.55273 | 0.29350 |
| With                    |   0.87714 |    0.61628 | 0.37100 |

Overall, it should be noted that I did not use normalization tactics, MinMaxScaler, in all my classifier 
pipelines, as scaling doesn't have an affect for  some algorithms.  I did not use the scaling for my decision tree
 or logistic regression classifiers.  With regards to decision trees, they do not produce a diagonal line, but 
 rather give you a series of vertical and horizontal lines, meaning the scaling will not have an effect.  Further, 
 regarding logistic / linear regression, my coefficients indicate the effect of a one-unit change in my 
 predictor variable, meaning that the effect of 
scaling does not affect the classifer as my raw data and scaled data varied across the same number of units in 
both scenerios.

What features I made / engineered and the rationale.

Feature Selection - did i use SelectKBest?  What were the feature scores?  What were my reasons for parameter 
values?

> What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  [relevant rubric item: “pick an algorithm”]

I iteratively tested many classifiers, taking the approach of building code that allowed me to define a single 
function for the pipeline execution, taking an argument as to what classifier and related parameters to utilize.
  I tested the following: 
  - Support Vector Machines (SVM)
  - Decision Tree
  - Naive Bayes
  - Random Forest
  - K Nearest Neighbors (KNN)
  - ADA Boost
  - Logistic Regression

Generally I found that performance ranged fairly widely between these.  I ultimately choose the Naive Bayes 
classifier, as I found that it produced the best results

I tried several algorithms, with a K-means clustering algorithm performing reasonably sufficient. Unsurprisingly, K-means clustering performed well, as the objective was to segregate the dataset into POI/non-POI groups. I also tested, with marginal success, an AdaBoost classifier, a support vector machine, a random forest classifier, and stochastic gradient descent (using logistic regression).

> What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).  [relevant rubric item: “tune the algorithm”]

xxx

> What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  [relevant rubric item: “validation strategy”]

xxx

> Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]

xxx