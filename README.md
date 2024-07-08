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

Resampled data using random_oversampler
                precision    recall  f1-score   support

           0       1.00      0.83      0.91      1905
           1       0.31      0.99      0.48       150

    accuracy                           0.84      2055
   macro avg       0.66      0.91      0.69      2055
weighted avg       0.95      0.84      0.88      2055
```

Interpretation:

- Class 0 (Not Hazardous): The second set shows 100% precision, but a significant drop in recall, showing that while the model is still very good at predicting class 0, it does so less often, leading to more false negatives.
- Class 1 (Hazardous): The second set shows significant improvement in recall, but a significant decrease in precision. This means the model is now much better at identifying instances of the hazardous class, but it has a higher rate of false positives. We want to improve our f1-score still, since this takes into consideration both precision and recall.
- Overall Accuracy: The accuracy is lower in the second set, reflecting the trade-off between precision and recall.

Did the model improve?

- For class 1, the second set of metrics shows a significant improvement in recall and F1-score, which indicates that the model is now much better at identifying positive instances.
- For class 0, the decrease in recall and F1-score suggests that the model’s performance for negative instances has worsened.

Conclusion:

- The second set of metrics represents an improvement for class 1 (hazardous instances) in terms of recall and F1-score. However, this comes at the cost of decreased performance for class 0 (negative instances) and overall accuracy. Let's see if we can get better performance overall at picking both classes.

- Try adding data in the minority class using SMOTE

```
Classification Report - Original Data
              precision    recall  f1-score   support

           0       0.94      1.00      0.97      1905
           1       0.84      0.14      0.24       150

    accuracy                           0.94      2055
   macro avg       0.89      0.57      0.60      2055
weighted avg       0.93      0.94      0.91      2055

---------
Classification Report - Resampled Data - SMOTE
              precision    recall  f1-score   support

           0       0.98      0.92      0.95      1905
           1       0.41      0.73      0.53       150

    accuracy                           0.90      2055
   macro avg       0.69      0.82      0.74      2055
weighted avg       0.94      0.90      0.92      2055
```
- Resampling with SMOTE has improved the model’s performance on the minority class (class 1) by significantly increasing recall and the F1-score, though at the cost of a drop in precision for class 1. This is a typical trade-off in imbalanced classification problems. The overall accuracy is slightly reduced, but the macro averages suggest a more balanced model. The choice between these models depends on the specific application and whether the focus is on reducing false negatives (improving recall) or maintaining high precision.

- Tried to improve model performance by retrieving more real data from NASA that showed only hazardous asteroids
- Modified create_dataset script to get additional records
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

- Improvement for Minority Class (Class 1): The new data model shows a significant improvement in recall (from 0.14 to 0.98) and F1-score (from 0.24 to 0.77) for the minority class. This means that the new model is much better at identifying the minority class, which is the primary goal.
- Overall Performance Trade-off: While there is a slight drop in overall accuracy and weighted average F1-score, the improvement in the minority class detection far outweighs these losses, especially if identifying the minority class correctly is critical.

Given the importance of correctly identifying the minority class, the new data model represents a substantial improvement over the original model. The significant increase in recall and F1-score for class 1 indicates that the new model is much better suited for tasks where detecting the minority class accurately is crucial.

```
Classification Report - Resampled and Added Data - SMOTE
              precision    recall  f1-score   support

           0       0.97      0.89      0.93      1902
           1       0.71      0.92      0.80       556

    accuracy                           0.89      2458
   macro avg       0.84      0.90      0.86      2458
weighted avg       0.91      0.89      0.90      2458
```
- The **Resampled and Added Data - SMOTE** model is generally better. It shows improvements in precision, recall, and F1-score for class 1 (the minority class), which is crucial for this application. It also provides slightly better overall performance metrics, indicating a more balanced and effective model.

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
