import sys

import preprocess
import numpy as np
import pandas as pd

import joblib

def test(raw_df):
    
    df_processed = preprocess.preprocess_data(raw_df, 'test')
    
    df_ml = df_processed
    target = 'price'
    if target in df_ml.columns:
        
        #features = list(set(df_ml.columns) - set(target))
        X_test = np.array(df_ml.drop(columns=[target]))
    else:
        X_test = np.array(df_ml)


    # Standardizing each feature using the train mean and standard deviation
    if 0:
        # Get mean and standard deviation from training set (per feature)
        idx=0

        mean = np.mean(X_test[:,idx])
        stdev = np.std(X_test[:,idx])

        X_test[:,idx] = (X_test[:,idx] - mean)/stdev
  

    regressor = joblib.load('xgboost.pkl')
    #print(f'\nPredicted price for your property is:{regressor.predict(X_test)}\n')
    #raw_df['price'] = regressor.predict(X_test)
    predictions = regressor.predict(X_test)
    predict_prices = predictions.tolist()

    return predict_prices[0]
