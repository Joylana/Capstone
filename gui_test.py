#getting data/model
from joblib import load
import pandas as pd

# Load the lr model back into a variable
loaded_model = load('lrmodel.joblib') # load model
preprocessor = load('preprocessor.joblib') # load pipeline

test = pd.read_csv('datasets/life_expectancy_test_data.csv')# load test data 
test = test[10:11] # get one row of data to test the GUI with

X = preprocessor.transform(test) # transform test data

# predict
prediction = loaded_model.predict(X,)


#running a quick test of the GUI to make sure it is working.
#import tkinter as tk
