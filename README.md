# Group 2: Project 2

### Objective
Create a model that can classify whether or not a near-earth object poses a risk of harm to satellites, interference of natural phenomena, or an impact on Earth. Use data from NASA's Near Earth Object Web Service to create the model and test it.

### Walkthrough

- Run script to retrieve NASA data from NEOwS API
  - Start preprocessing in this step by removing rows that contain blanks and converting boolean values to 0,1.
- Create features set and target vector
- Check value counts of the target data (1 = hazardous)

```
is_potentially_hazardous
0    7666
1     552
```

- Split data into training and testing sets
- Data scaling was required since we were dealing in many units of measurement and a wide range of values
- Create several models for preliminary evaluation

Example Results (I'll summarize all results better throughout the week):

SVC - rbf (StandardScaler)
```
Train Accuracy: 0.940
Test Accuracy: 0.931
```

SVC - rbf (MinMaxScaler)
```
Train Accuracy: 0.935
Test Accuracy: 0.927
```

- Create and plot scores_df to determine appropriate max depth for Random Forest
- Create Random Forest using Standard Scaled data

RandomForest (max_depth=3)
```
Train Accuracy: 0.9436962518254097
Balanced Accuracy Score: 0.5689501312335958
```

- This suggests the model is not great at identifying hazardous asteroids potentially due to the extent to which the data is imbalanced. This false negative (saying it's not hazardous when it is) could be potentially catastrophic. 
- Efforts must be taken to improve model performance at detecting hazardous asteroids. 

- Try Resampling with random_oversampler. The data for non-hazardous values is good, and we don't want to lose it if possible.

Resampled Value Counts
```
is_potentially_hazardous
0    5761
1    5761
```

Classification Reports For RandomForest with max_depth of 3 using predictions from resampled model using random_oversampler vs. original data:
```
original_data
                precision    recall  f1-score   support

           0       0.94      1.00      0.97      1905
           1       0.84      0.14      0.24       150

    accuracy                           0.94      2055
   macro avg       0.89      0.57      0.60      2055
weighted avg       0.93      0.94      0.91      2055

using random_oversampler
                precision    recall  f1-score   support

           0       1.00      0.83      0.91      1905
           1       0.31      0.99      0.48       150

    accuracy                           0.84      2055
   macro avg       0.66      0.91      0.69      2055
weighted avg       0.95      0.84      0.88      2055
```

- The resampled data showed a significant improvement in recall score (up to 94%), which shows it performs much better in detecting the presence of a hazardous asteroid.
- The precision score suffered 

...more interpretation and discussion is required here...

- Tried to improve model performance by retrieving more real data from NASA that showed only hazardous asteroids
- Wrote script to get additional records
- Extracted only records showing hazardous asteroids
- Created new RandomForest Model 

Target value counts with new data
```
is_potentially_hazardous
0    7666
1    2164
```

RandomForest Accuracy Scores with new data
```
Testing data accuracy score: 0.8677786818551668
Training data accuracy score: 0.8700488334237656
Balanced Accuracy Score: 0.9088360226645182
```

Classification Report with New Data
```
              precision    recall  f1-score   support

           0       0.99      0.83      0.91      1902
           1       0.63      0.98      0.77       556

    accuracy                           0.87      2458
   macro avg       0.81      0.91      0.84      2458
weighted avg       0.91      0.87      0.88      2458
```

- ...need to finish interpretation...

### TODO

[x] Build model v 0.1

  [x] Summarize all test scores from existing models
  [x] Optimize Random Forest Model (including addressing Overfitting)
  [x] Create data retrieval script for new NASA
  [x] Concatenate new NASA data to base dataset

So far: Random Forest is in the lead.
- Badly imbalanced data
- Model is not so good at picking the "hazardous" outcome (minority)
- Optimization work will be to lower the occurrences of "false positives"

[x] Preprocess Data
- Ensuring data is numerical and not string
- Scale using StandardScaler and MinMaxScaler (Standard performed better - only just)
- True/False outcomes were turned in 0,1 outcomes when the data was pulled from the API

[x] Create json file from NASA API that can be used to create the model
- Create script (create_dataset.py) that makes a request to NASA NEOwS API for data in 1 week intervals. Do this for 52 weeks beginning from June 1st.
- Format the data into something we can use for machine learning models (inspired by Kaggle dataset: https://www.kaggle.com/datasets/sameepvani/nasa-nearest-earth-objects)

FYI:
- [Script for retrieving and formatting data from NASA](create_dataset.py)
