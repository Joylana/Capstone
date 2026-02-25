#getting data/model
from joblib import load
import pandas as pd

# Load the lr model back into a variable
loaded_model = load('/Users/alanajoymorrison/Desktop/Capstone/lrmodel.joblib') # load model
preprocessor = load('/Users/alanajoymorrison/Desktop/Capstone/preprocessor.joblib') # load pipeline

test = pd.read_csv('/Users/alanajoymorrison/Desktop/Capstone/datasets/life_expectancy_test_data.csv')# load test data 
test = test[10:11] # get one row of data to test the GUI with

X = preprocessor.transform(test) # transform test data

# predict
prediction = loaded_model.predict(X,)
print(prediction)


#running a quick test of the GUI to make sure it is working.
import tkinter as tk

root = tk.Tk()

root.title("Life Expectancy Prediction")
label = tk.Label(root, text="Predicted Life Expectancy: " + str(prediction[0]), 
                 font=("Arial", 16))
label.pack(pady=20)

root.mainloop()