# Group 2: Project 2

### Create a model that can classify whether or not a near-earth object poses a risk of harm to satellites, interference of natural phenomena, or an impact on Earth. Use data from NASA's Near Earth Object Web Service to create the model and test it.


TODO:

[-] Build model v 0.1
  [ ] Summarize all test scores from existing models
  [ ] Optimize Random Forest Model (including addressing Overfitting)
  [ ] Create data retrieval script for new NASA
  [ ] 

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
