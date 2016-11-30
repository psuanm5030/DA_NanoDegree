# P5: Identify Fraud from Enron Email
Student: Andy Miller 
Udacity's [Data Analyst Nanodegree](https://www.udacity.com/course/nd002)

## Background

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, there was a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for to executives.

Utilizing `scikit-learn` and machine learning methodologies, I built a "person of interest" (POI) identifier to detect and predict culpable persons, using features from financial data, email data, and labeled data--POIs who were indicted, reached a settlement or plea deal with the government, or testified in exchange for prosecution immunity.

## Free-Response Questions

### Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: “data exploration”, “outlier investigation”]

I may repeat some of the detail from the project submission page, but I feel it rings especially true.  The primary goal of this project was to "play detective" and  put our new machine learning skills to the test, in an effort to create a classification model that would, as accurately as possible, predict whether a person was a  "person of interest" (POI) based upon that data available.  This meant taking the learnings from the 15 Udacity lessons, covering various classification algorithms and machine learning techniques (such as feature selection, validation and evaluation), then applying these to a real dataset.  I found that the Udacity courses gave a very wide ranging introduction to each algorithm and technique, but required that we do our own learning.  I captured most of my learning from the sklearn documentation and the Udacity forum (refer to references section).  
 
There is no doubt that this data set is a unique blend, consisting of both financial information for 145 individuals (collated from public filings and the Enron trial) and emails that were made public from the trial. This dataset allows us to answer our project question because it contains the actual POI labels.  Therefore, we had to create our classifiers, review the accuracy metrics, then go back and do the following: 
  - Check for outliers that affected our accuracy in a negative way (while being careful not to remove too much data),
  - Create new features that would help the classifier make better predictions, and 
  - Tune the classifier parameters based on iterative accuracy results.
  
Concerning outliers, I removed exactly three observations (rows) of data (there were 146 in total - 18 Labeled POI | 127 Labeled Non-POI): 
- "TOTAL" - which was an arbitrary observation imported with the based data,
- "THE TRAVEL AGENCY IN THE PARK" - a non-person observation that has no related meaning / importance, and  
- "LOCKHART EUGENE E" - an actual person observation that had 20 of 21 fields with 'NaN' values (95% of features), making this person a very poor observation to use for classification purposes.
 
As a note, I noticed significant increase in accuracy, precision and recall after removing these outliers.  Using the Naive Bayes algorithm, I noted: 

Table 1. Outliers

| With / Without Outliers | Accuracy↑ | Precision↑ | Recall↑ |
|-------------------------|----------:|-----------:|--------:|
| With                    |   0.83329 |    0.11697 | 0.02550 |
| Without                 |   0.87714 |    0.61628 | 0.37100 |

### What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “properly scale features”, “intelligently select feature”]

*Selecting Features* 
I utilized the univariate feature selection method of SelectKBest, embedded within my pipelines, to select the most relevant features.  This method selects the K best features that are the most powerful.  Prior to the pipeline, I evaluated the best 15 features found through this method and the associated scores.  

Table 2. Feature Scoring

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

As you can see, the two fields that I created, Ratio_from_POI and Ratio_to_POI were scored in the bottom third, meaning they were likely typically not used by any of my models.  I did test my Naive Bayes classifier with 15 features as the SelectKBest parameter and found that recall was substantially reduced (precision was still moderately acceptable at .441). 

Within my pipelines I set the k parameter, typically, to be any integer between 2 and 7 on average.  I found that the best classifier chosen by GridSearchCV was typically 4-5 features.  For my chosen classifier, Naive Bayes, GridSearchCV suggested that I use the following 5 features:
- salary 
- exercised_stock_options
- bonus
- total_stock_value
- deferred_income

*Selecting Rescaling / Normalization* 
Further more, for many of my classifiers, I did employ a normalization technique, using the sklearn MinMaxScaler.  This re-scaled the financial features to be values between 0 and 1. For my chosen algorithm, this was very important, as many of the features were on vastly different scales.  For example, salary and from_messages, are two features that represent two different types of numeric data, one being currency and one being a count of messages, where salary is on a much broader scale than from_messages.  This requires normalization to ensure that the algorithm is not inappropriately swayed by the fact that one feature is on a different scale.  For my Naive Bayes classifier, I found that the scaling significantly improved all my evaluation metrics (see table below).   

Table 3. Scaling Evaluation

| With / Without Scaling  | Accuracy↑ | Precision↑ | Recall↑ |
|-------------------------|----------:|-----------:|--------:|
| Without                 |   0.86514 |    0.55273 | 0.29350 |
| With                    |   0.87714 |    0.61628 | 0.37100 |

Overall, it should be noted that I did not use normalization tactics, MinMaxScaler, in all my classifier pipelines, as scaling doesn't have an affect for  some algorithms.  I did not use the scaling for my decision tree or logistic regression classifiers.  With regards to decision trees, they do not produce a diagonal line, but rather give you a series of vertical and horizontal lines, meaning the scaling will not have a positive effect.  Further, regarding logistic / linear regression, my coefficients indicate the effect of a one-unit change in my predictor variable, meaning that the effect of scaling does not affect the classifier as my raw data and scaled data varied across the same number of units in both scenerios.

*Feature Engineering*
I felt that the features related to the email data were lacking in their targeting.  Primarily, I felt that the features, such as to_messages and from_messages were not meaningful as standalone features, but rather they should be centered around the relation with the POI.  Therefore, I created two new features, 'Ratio_from_POI' and 'Ratio_to_POI', which gave me a more well rounded glimpse of their relation to POIs.  These features were created to capture the ratio of emails were from / to a POI, with the numerator as the number of messages sent to / received from a poi and the denominator as the total messages for that person that were sent / received.  These help better understand the related interaction (through email communication) with any POI.

These features, as mentioned above, did not score as well as some of the other financial features.  

### What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  [relevant rubric item: “pick an algorithm”]

I iteratively tested many classifiers, taking the approach of building code that allowed me to define a single function for the pipeline execution, taking an argument as to what classifier and related parameters to utilize. I tested the following classifiers.  I am also denoting the achieved evaluation metrics:

Table 4. Algorithm Performance

| Algorithm                     | Accuracy | Precision | Recall |
|-------------------------------|----------|-----------|--------|
| Naive Bayes                   | 0.87714  | 0.61628   | 0.371  |
| Support Vector Machines (SVM) | 0.86529  | 0.82386   | 0.0725 |
| Random Forest                 | 0.85129  | 0.43212   | 0.1305 |
| K-Nearest Neighbors           | 0.84592  | 0.2       | 0.0005 |
| ADA Boost                     | 0.84493  | 0.4156    | 0.2105 |
| Decision Tree                 | 0.80569  | 0.35921   | 0.3355 |
| Logistic Regression           | 0.76371  | 0.24943   | 0.3255 |
| K-Means Clustering            | 0.72977  | 0.2266    | 0.3135 |

Generally, I found that performance ranged widely between these, as you can see.  I spent many hours tinkering with the pipeline parameters and researching the algorithms, running each at least 5-10 times.  I ultimately choose the Naive Bayes classifier, as I found that it produced the best results.  This classifier does not have the variety of parameters to select from (as opposed to others), therefore I focused on getting SelectKBest and PCA setup in my pipeline appropriately.  I ultimately found, with the aid of GridSearchCV that 5 features and 2 PCA components achieved the best results.  

### What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).  [relevant rubric item: “tune the algorithm”]

I understand and believe machine learning to be a powerful tool with the purpose of teaching a machine to methodically ingest and interpret past, labeled data, with the goal of producing a result where the label is unknown.  This is powerful as the model produced by the machine can grow smarter with each new observation and adapt its prediction capabilities in an appropriate way, without the tedious and manual involvement of a human. Tuning an algorithm or machine learning technique can simply be thought of as a process which one goes through in whichthey optimize the parameters that impact the model in order to enable the algorithm to perform optimally.

Through my experience with this project, I found that tuning the algorithm is, in itself, a tedious task, but has the greatest amount of impact on a successful model.  As mentioned above, with my choosen classifier, I did not have many Naive Bayes parameters to tune, but I did have other tecniques in my pipeline that required thought and tuning, such as SelectKBest and PCA.  For other algorithms, I did need to tune the parameters and used GridSearchCV to make this much less laborious.  For instance, with my SVM classifier, I set a variety of parameters for interpretation and selection by GridSearchCV: 
- kernel: ['rbf', 'linear'],
- C: [10.0, 100.0, 1000.0, 10000.0],
- gamma: [0.01, 0.001, 0.0001]

GridSearchCV did much of the work, running all the variations of these parameters and selecting the one that resulted in the best performance.  The final classifier was tuned as follows: 
> Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=5, score_func=<function f_classif at 0x10ca822a8>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=2, random_state=None, whiten=True)), ('NB', GaussianNB())])

### What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  [relevant rubric item: “validation strategy”]

Validation helps us understand how well a classifier generalizes.  Since the classifier based from the data that the classifier is trained on, we need some way to evaluate how the classifier generalizes and predicts labels for new data.  The classic mistake is over-fitting your model, whereby the model is training on too much data (i.e., too many features), such that the model essentially memorizes the relation between training labels and training labels, but new data (or test data) is not generalized adequately. 

I purposefully chose to use the entire dataset for training the model.  The primary reason is that we have such limited data, in fact only 143 observations and approximately 20 features.  This is opposite of a norm of splitting the data into training and test datasets, training the model on the training data and validating that model against the test data that was held out of the data to train the model.  

I should further explain that I used stratified shuffle split, which randomizes the selection of the training and test sets. Therefore, all of the data is used ot both select algorithm parameters as well as to assess the model's performance, and the labels are partitioned into equal ratios in both the training and testing sets.

Using this approach, I am able to come to the best classifier, tuned with the best parameters, which was fed into the tester.py function to give final evaluation of my classifier.

### Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]

I focused on two metrics when evaluating the performance of my classifiers.  As noted in Table 4 above, I found that the metrics varied, and focused on precision and recall, to come to conclusions about their performance.  With regards to precision, with is the number of true positives (predicted POI and the person was a POI) over the number of true positives and false positives (predicted POI and the person was non-POI).  Precision can be summed up as how many selected items are relevant.  Recall looks that the number of true positives over the number of true positives and false negatives (predicted non-POI and was a POI).  Recall can be summed up as how many relevant items are selected.  With relation to our POI identifier, good precision means that when someone is flagged as a POI, we feel confident that it is very likely an accurate prediction, however this sometimes comes as a cost of  missing other POIs that we might have flagged as non-POIs. If we have good recall, this means that I am very likely to identify POIs, but this sometimes comes with the cost of identifying POIs that are really non-POIs.  Therefore, its best to evaluate these metrics in tandem.
  
With regards to my data, I will highlight one of my classifiers: 
  
Table 4. Metrics Comparison

| Algorithm                     | Accuracy | Precision | Recall |
|-------------------------------|----------|-----------|--------|
| Support Vector Machines (SVM) | 0.86529  | 0.82386   | 0.0725 |

With SVM, I noted VERY high precision, but very low recall.  Meaning that I identified many of the true POIs and had a limited number of instances where I flagged a POI that was truly a non-POI.  However, with recall being so low, this means that I flagged many true POIs as non-POIs.

### Conclusion 

In conclusion, I felt like this was a fantastic project that engaged me and forced me to do alot of my own individual research and discovery.  Building the classifier from start to finish allowed me to understand critical aspects of machine learning, such as feature engineering, feature selection, model tuning, validation and evaluation. 

With regards to my classifier, I was pleased with the results of my Naive Bayes classifier, however, still have a yearning to push the other classifiers to produce better results.  This wass an inheritely difficult task to work with limited data to predict something that also is very difficult to do, that is who might be a person of interest.  I found through this project that you must understand your data and classifier, as well as, broaden you scope to other areas that can improve performance.   


#### References: 
- All sklearn documentation pages for each tecnique and alogrithm utilized.
- https://discussions.udacity.com/t/GridSearchCV-and-testingtraining-data/36107
- http://stackoverflow.com/questions/22903267/what-is-tuning-in-machine-learning 