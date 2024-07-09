# Group 2: Project 2

## Objective
Create a model that can classify whether or not a near-earth object poses a risk of harm to satellites, interference of natural phenomena, or an impact on Earth. Use data from NASA's Near Earth Object Web Service to create the model and test it.

## Overview

**Data Retrieval and Formatting**

The [create_dataset.py](create_dataset.py) script retrieves data from the NASA Near Earth Object (NEO) Web Service and prepares it for analysis. 

- Inspired by [Kaggle dataset](https://www.kaggle.com/datasets/sameepvani/nasa-nearest-earth-objects), we decided to manually retrieve the data instead of downloading the prepared version
- Queries the NASA API for a week's worth of NEO data at a time (does this for 52 periods)
- Structures the data into a dictionary with attributes like ID, name, magnitude, diameter, velocity, miss distance, orbiting body (Earth), and classification
- Begins preprocessing by removing rows that contain blanks and converting boolean values to 0,1
- Creates a list of dictionaries suitable for a pandas DataFrame
- Provides methods to export the data to local json or csv file

**Early Model Testing**

- Check the value counts of the target variable (potentially hazardous or not)

```
is_potentially_hazardous
0    7666
1     552

The data is imbalanced!
```

- Split data into training and testing sets
- Data scaling was required since we were dealing in many units of measurement and a wide range of values
- Create several models for preliminary evaluation

Example Results:

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

**Model Optimization**

- Try Resampling with random_oversampler. The data for non-hazardous values is good, and we don't want to lose it if possible.

Resampled Value Counts
```
is_potentially_hazardous
0    5761
1    5761
```

Classification Reports For RandomForest with max_depth of 3 using predictions from resampled model using random_oversampler vs. original data:
```
Original Data
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
Did the model improve?

- The second set of metrics represents an improvement for class 1 (hazardous instances) in terms of recall and F1-score. However, this comes at the cost of decreased performance for class 0 (negative instances) and overall accuracy. Let's see if we can get better performance overall at picking both classes.

- Try synthesizing minority class data using SMOTE

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
- Resampling with SMOTE improved the model’s performance on the minority class (class 1) by significantly increasing recall and the F1-score. Again, this came at the cost of a drop in precision for class 1. The overall accuracy is slightly reduced, but the macro averages suggest a more balanced model. Let's try to balance the model further and continue to improve the recall score on class 1, since false negatives could have catastrophic consequences.

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

- The new data helped the model show significant improvement in recall (from 0.14 to 0.98) and F1-score (from 0.24 to 0.77) for the minority class. This means that the new model is much better at identifying the minority class, which is the primary goal.
- While there is a slight drop in overall accuracy and weighted average F1-score, the improvement in the minority class detection far outweighs these losses, especially since identifying the minority class correctly could save the world.
- Given the importance of correctly identifying the minority class, the new data model represents a substantial improvement over the original model.

Let's see what happens if we try to balance the dataset using SMOTE. 
```
Testing data accuracy score: 0.8991049633848658
Training data accuracy score: 1.0
Balanced Accuracy Score: 0.9068038944238931

---------
Classification Report - Resampled and Added Data - SMOTE
              precision    recall  f1-score   support

           0       0.97      0.89      0.93      1902
           1       0.71      0.92      0.80       556

    accuracy                           0.89      2458
   macro avg       0.84      0.90      0.86      2458
weighted avg       0.91      0.89      0.90      2458
```
- The **Resampled and Added Data - SMOTE** model provides slightly better overall performance metrics, indicating a more balanced and effective model. Precision and the f1-score improved for the hazardous class, with recall dropping from 98% to 92%. Further improvements could definitely be made to the model with more time and data.

## Conclusion

We were able to significantly increase the model's ability to classify potentially hazardous asteroids by providing it more real data to analyze and synthesizing data to try and balance the data set. Although there is evidence of overfitting and room for overall improvement, this major increase of recall and f1-score is satisfactory for the scope of the project.

NASA likely has a more detailed data set behind the scenes that might allow for further feature engineering that could help improve the model. It would be very interesting to see their full method for identifying which asteroids are potentially harmful. 

### Key Files

- [neo_model.py](neo_model.py): Contains the model creation and optimization
- [create_dataset.py](create_dataset.py): Script for retrieving and formatting NASA data
- resources/neo_data.json: Parsed data set used to create the first models
- resources/additional_neo_data.json: Additional parsed data
- Final Grp 2 Presentation w simulation 7.8.24.pptx: Presentation slides
- working_copies directory: Free experiments before moving code to neo_model jupyter notebook
